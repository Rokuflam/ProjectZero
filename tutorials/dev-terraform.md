## Tutorial Guide: Deploying a Development Environment with Terraform

This guide will walk you through the process of deploying a development environment using Terraform. The tutorial assumes you are using AWS as your cloud provider. By the end of this guide, you'll have a basic infrastructure set up, and you'll understand how to manage it using Terraform.

### Prerequisites

Before starting, ensure that you have the following:

- **Terraform installed** on your machine. You can download it [here](https://www.terraform.io/downloads.html).
- A Git branch named `development`, which is necessary for CI/CD integration.

**For AWS deployments:**

- **AWS CLI installed** and configured with your AWS credentials. You can follow the installation instructions from the [official AWS documentation](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html).
- An **IAM user** with the following permissions:

  ```json
  {
      "Version": "2012-10-17",
      "Statement": [
          {
              "Effect": "Allow",
              "Action": [
                  "ec2:CreateSecurityGroup",
                  "ec2:DeleteSecurityGroup",
                  "ec2:DescribeSecurityGroups",
                  "ec2:AuthorizeSecurityGroupIngress",
                  "ec2:RevokeSecurityGroupIngress",
                  "ec2:RevokeSecurityGroupEgress",
                  "ec2:AuthorizeSecurityGroupEgress",
                  "ec2:CreateKeyPair",
                  "ec2:DeleteKeyPair",
                  "ec2:RunInstances",
                  "ec2:DescribeInstances",
                  "ec2:TerminateInstances",
                  "ec2:CreateTags",
                  "ec2:DeleteTags",
                  "ec2:DescribeInstanceTypes",
                  "ec2:DescribeTags",
                  "ec2:DescribeInstanceAttribute",
                  "ec2:DescribeVolumes",
                  "ec2:DescribeNetworkInterfaces",
                  "ec2:DescribeInstanceCreditSpecifications",
                  "ec2:ImportKeyPair",
                  "ec2:DescribeKeyPairs",
                  "ecr:CreateRepository",
                  "ecr:DeleteRepository",
                  "ecr:DescribeRepositories",
                  "ecr:TagResource",
                  "ecr:ListTagsForResource",
                  "ecr:GetAuthorizationToken",
                  "ecr:BatchCheckLayerAvailability",
                  "ecr:GetDownloadUrlForLayer",
                  "ecr:GetRepositoryPolicy",
                  "ecr:DescribeRepositories",
                  "ecr:ListImages",
                  "ecr:DescribeImages",
                  "ecr:BatchGetImage",
                  "ecr:InitiateLayerUpload",
                  "ecr:UploadLayerPart",
                  "ecr:CompleteLayerUpload",
                  "ecr:PutImage",
                  "ec2:AllocateAddress",
                  "ec2:DescribeAddresses",
                  "ec2:DescribeAddressesAttribute",
                  "ec2:ReleaseAddress",
                  "ec2:AssociateAddress",
                  "ec2:DisassociateAddress"
              ],
              "Resource": "*"
          }
      ]
  }
  ```

### Step-by-Step Configuration

#### Step 1: Navigate to Your Terraform Directory

Open your terminal and navigate to the Terraform `dev` directory:

```bash
cd .\terraform\dev\
```

#### Step 2: Create the `terraform.tfvars` File

The `terraform.tfvars` file is where you provide the actual values for the variables defined in your Terraform configuration. Create this file with the following content, replacing the placeholder values with your actual data:

```hcl
vpc_id       = "vpc-xxxxxxxx"            # Replace with your actual VPC ID
aws_region       = "us-east-1"           # You can change this if needed
ami_id       = "ami-0c02fb55956c7d316"   # Replace with your actual AMI ID
instance_type = "t2.micro"               # Free tier instance type
public_key_path = "replace-me"           # Ensure Windows path is properly escaped
private_key_path = "replace-me"          # Ensure Windows path is properly escaped
github_token    = "replace-me"           # GitHub token with appropriate permissions (as listed)
github_owner    = "replace-me"           # GitHub repository owner username
github_repository = "replace-me"         # Name of the GitHub repository
github_repository_ssh_clone_url = ""     # URL to clone repository via SSH
ecr_repository  = "replace-me"           # Name of the ECR repository
```

#### Step 3: Initialize Terraform

Before using Terraform to manage your infrastructure, you need to initialize your working directory, which contains the Terraform configuration files:

```bash
terraform init
```

This command downloads the necessary provider plugins and prepares your working directory.

#### Step 4: Create an Execution Plan

The `terraform plan` command creates an execution plan, showing you what Terraform will do when you apply the configuration:

```bash
terraform plan
```

This step is crucial as it allows you to review the changes that Terraform will make before applying them.

#### Step 5: Apply the Configuration

To create the resources as defined in your Terraform files, use the `terraform apply` command:

```bash
terraform apply
```

Terraform will ask you to confirm that you want to apply these changes. Type `yes` to proceed. Terraform will then start creating the resources in your AWS account.

### Destroying Resources

If you need to destroy the resources created by Terraform, you can do so with the following command:

```bash
terraform destroy
```

As with the `apply` command, Terraform will prompt you to confirm the action by typing `yes`. This command will remove all resources defined in your Terraform configuration from your AWS account.

### Conclusion

By following these steps, you've successfully deployed a development environment using Terraform. This setup is now ready for development and CI/CD processes. Terraform’s infrastructure as code approach not only simplifies the setup but also makes it easier to manage and scale your environments.
