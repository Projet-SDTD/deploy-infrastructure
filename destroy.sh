cd  terraform-resources
terraform destroy || (echo "Now, go delete the k8s-related routes in the GCP console" && echo "Press ENTER when done" && read -s && terraform destroy)