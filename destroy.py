#!/bin/python3
import os
import platform
import subprocess
from google.cloud import compute_v1
import json
import time
import threading

filepath = os.path.abspath(__file__)
dirpath = os.path.dirname(filepath)
CRED_FILE = 'credentials.json'
REGION = 'europe-west9'

def destroyRoutesAndRules(ttw=180):

    # Wait for terraform to have started destroying the cluster
    time.sleep(ttw)

    # Create requested elements to interact with GCP API
    os.chdir(os.path.join(dirpath, "terraform-resources"))
    clientRoutes = compute_v1.RoutesClient.from_service_account_file(CRED_FILE)
    clientRules = compute_v1.FirewallsClient.from_service_account_file(CRED_FILE)
    forwardingClient = compute_v1.ForwardingRulesClient.from_service_account_file(CRED_FILE)
    with open(CRED_FILE) as f:
        cr = json.load(f)
    PROJECT_ID = cr['project_id']
    
    # List resources
    request = clientRoutes.list(project=PROJECT_ID)
    request2 = clientRules.list(project=PROJECT_ID)
    request3 = forwardingClient.list(project=PROJECT_ID, region=REGION)

    routes_to_destroy = []
    rules_to_destroy = []
    frules_to_destroy = []

    # Determine resources to delete
    for i in request:
        if i.description == "k8s-node-route":
            routes_to_destroy.append(i.name)

    for i in request2:
        if "kubernetes.io" in i.description:
            rules_to_destroy.append(i.name)

    for i in request3:
        if "kubernetes.io" in i.description:
            frules_to_destroy.append(i.name)

    print("Destroying additional routes: ", routes_to_destroy)
    print("Destroying additional rules: ", rules_to_destroy)
    print("Destroying additional FW resources: ", frules_to_destroy)

    # Delete the additional resources
    for r in routes_to_destroy:
        clientRoutes.delete(project=PROJECT_ID, route=r)

    for r in rules_to_destroy:
        clientRules.delete(project=PROJECT_ID, firewall=r)

    for f in frules_to_destroy:
        forwardingClient.delete(project=PROJECT_ID, region=REGION, forwarding_rule=f)

def destroyTerraform():
    os.chdir(os.path.join(dirpath, "terraform-resources"))
    subprocess.run(["terraform", "destroy", "-auto-approve"])

currentSystem = platform.system()
if currentSystem != 'Linux':
    print("## This script is intended for Linux only !")
    exit(1)

t = threading.Thread(target=destroyRoutesAndRules)
t.start()
destroyTerraform()
t.join()

# Verify that additional rules have been deleted
try:
    destroyRoutesAndRules(0)
except:
    pass