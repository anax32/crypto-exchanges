# Terraform for AWS setup

Requirements:
+ tfvars file containing:
    + `aws_access_key_id`
    + `aws_secret_access_key`
    + `aws_region`  aws region to host the infrastructure
    + `whitelist_ips`  array of IP address which can access the instance
    + `public_key` key/value pair of [name, map] containing the name and ssh key to access the instance


## SSH Key Access

+ generate a key as usual
    + `ssh-keygen`
+ extract the public key string
    + `ssh-add -L`
+ add the public key string to the `.tfvars` file in the `public_key` variable
+ `terraform apply`
+ create the pem file
    + `ssh-keygen -f <ssh key filename> -e -m pem > <pem filename>`
+ connect to the instance
    + `ssh -i <pem filename> <username>@<instance name>`
