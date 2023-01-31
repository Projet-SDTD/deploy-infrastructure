#!/bin/python3

import os
import platform
import subprocess
from zipfile import PyZipFile
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument('-nda', action='store_true', help="Set this flag to prevent deploying ansible playbook", default=False)
args = parser.parse_args()

filepath = os.path.abspath(__file__)
dirpath = os.path.dirname(filepath)
preferredInstallDirectories = ["/usr/local/sbin","/usr/local/bin","/usr/sbin","/usr/bin"]

def checkFiles():
    os.chdir(os.path.join(dirpath, "terraform-resources"))
    if not(os.path.exists("main.auto.tfvars")):
        print("## Please copy terraform-resources/main.example.tfvars to terraform-resources/main.auto.tfvars and fill it with your variables")
        exit(1)
    if not(os.path.exists("credentials.json")):
        print("## Please retrieve a .json key from gcp account and put it in terraform-resources/credentials.json")
        exit(1)
    if not(os.path.exists("terraform_key.pub")):
        print("## Please copy your ssh public key to terraform-resources/terraform_key.pub")
        exit(1)

def aptInstalled():
    try:
        subprocess.run(["apt", "-v"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except:
        return False

def pythonInstalled():
    try:
        subprocess.run(["python3", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except:
        return False

def pipInstalled():
    try:
        rc = subprocess.run(["python3","-m","pip", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode
        if rc == 0:
            return True
        return False
    except:
        return False

def wgetInstalled():
    try:
        subprocess.run(["wget", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except:
        return False

def terraformInstalled():
    try:
        subprocess.run(["terraform", "version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except:
        return False

def ansibleInstalled():
    try:
        subprocess.run(["ansible","--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except:
        return False

def installTerraform():
    if wgetInstalled():
        try:
            print("## Trying to install terraform ...")
            cpDirectories = os.environ['PATH'].split(":")
            cpDirectory = ""
            for d in cpDirectories:
                if d in preferredInstallDirectories:
                    cpDirectory = d
            assert cpDirectory != ""
            subprocess.run(["wget", "-O", "terraform.zip", "https://releases.hashicorp.com/terraform/1.3.4/terraform_1.3.4_linux_amd64.zip"])
            pzf = PyZipFile("terraform.zip")
            pzf.extractall()
            subprocess.run(["sudo", "mv", "terraform", "/usr/local/bin/"])
            subprocess.run(["sudo", "chmod", "+x", "/usr/local/bin/terraform"])
            os.remove("terraform")
            os.remove("terraform.zip")
            assert terraformInstalled()
            print("## Successfully installed terraform")
        except:
            print("## Installation aborted, a problem occured")
            exit(1)

def installAnsible():
    try:
        if not(pythonInstalled()):
            assert aptInstalled()
            subprocess.run(["sudo", "apt", "install", "-y", "python3"])
        if not(pipInstalled()):
            assert aptInstalled()
            subprocess.run(["sudo", "apt", "install", "-y", "python3-pip"])
        subprocess.run(["python3", "-m", "pip", "install", "ansible"])
        assert ansibleInstalled()
        print("## Ansible installed succesfully !")
    except:
        print("## Ansible failed to install, please install it manually with python3 and pip")
        exit(1)

def deployTerraform():
    os.chdir(os.path.join(dirpath, "terraform-resources"))
    subprocess.run(["terraform", "init"])
    subprocess.run(["terraform", "apply", "-auto-approve"])

def deployAnsible():
    os.chdir(os.path.join(dirpath))
    os.putenv("ANSIBLE_HOST_KEY_CHECKING", "False")
    subprocess.run(["ansible-playbook", "-i", "terraform-resources/inventory", "ansible-playbooks/initial-kubernetes.yaml"])
    subprocess.run(["cp", "ansible-playbooks/fetched/kubeconfig", "./"])

# Check that user uses linux
currentSystem = platform.system()
if currentSystem != 'Linux':
    print("## This script is intended for Linux only !")
    exit(1)

checkFiles()

if not(terraformInstalled()):
    print("## Terraform not installed")
    installTerraform()

if not(ansibleInstalled()):
    print("## Ansible not installed, trying to install ...")
    installAnsible()

deployTerraform()

if not(args.nda):

    for i in range(25,0,-1):
        print("## Waiting "+str(i*10)+" seconds for changes to propagate")
        time.sleep(10)

    deployAnsible()