#!/bin/bash

echo "## Applying terraform"
cd terraform-resources
terraform init && terraform apply

echo "## Waiting 1m for cluster creation"
sleep 2m

echo "## Executing ansible"
cd ../
ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i terraform-resources/inventory ansible-playbooks/initial-kubernetes.yaml
cp ansible-playbooks/fetched/kubeconfig ./