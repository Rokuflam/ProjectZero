# ProjectZero


A DRF project to start new projects faster and better.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Terraform Setup](#terraform-setup)
- [Acknowledgments](#acknowledgments)

## Features

- Django 5.0+
- Django REST Framework for building APIs
- User authentication and authorization
- Social authentication
- Token-based authentication
- Serialization of models
- CRUD operations
- Testing with `unittest`
- Continuous Integration with GitHub Actions
- Linting using Pylint
- Sending email with Anymail
- HealthCheckMiddleware
- SQLProfilerMiddleware

## Prerequisites

Make sure you have the following installed on your machine:

- Docker
- Python 3.12
- pip
- poetry (optional but recommended)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Rokuflam/ProjectZero.git
    ```

2. Navigate to the project directory:

    ```bash
    cd ProjectZero
    ```
   If you are using Pycharm, [follow documentation to set up poetry env](https://www.jetbrains.com/help/pycharm/poetry.html), otherwise follow next steps

3. Open Poetry shell:

    ```bash
    poetry shell
    ```

4. Generate Poetry lock file

   ```bash
    poetry lock
   ```

5. Install or Update project dependencies:

    ```bash
    poetry install
    ```
    ```bash
    poetry update
    ```

## Configuration

1. Create a copy of the `.env.example` file and name it `.env`. Update the values as needed.

2. If you need a Social Auth, go to `backend/apps/user/fixtures/social-auth.json`,
and change client_id for the app you are about to use.

3. If you need Anymail, fill variables from example.env into your env file,
and choose `EMAIL_BACKEND` in `backend/config/settings/{env you use}.py`

## Usage
- Run the development server:
    ```bash
    docker-compose -f docker/docker-compose-local.yml up
    ```

- Run tests
    ```bash
    docker-compose -f docker/docker-compose-local.yml run --rm app sh -c "python manage.py test apps"
    ```

- Pylint check
    ```bash
    docker-compose -f docker/docker-compose-local.yml run --rm app sh -c "pylint apps --rcfile=.pylintrc"
    ```

## API Documentation

1.   [Swagger](http://localhost:8000/api/docs/) /api/docs/
2.   [Admin panel](http://localhost:8000/admin/) /admin/

## Terraform Setup

Terraform is used to manage and provision your cloud infrastructure. Here are the steps to set up a free-tier EC2 instance for dev-env:

### Prerequisites

- Terraform installed on your machine. [Download Terraform](https://www.terraform.io/downloads.html)

AWS only:
- AWS CLI installed and configured with your AWS credentials.
- Create branch with name: `development`, for CI/CD to work
- Create an IAM user with next permissions:

```bash
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


### Configuration


1. Open Terminal and go to terraform\dev:

    ```bash
    cd .\terraform\dev\
    ```

2. Create a `terraform.tfvars` file to provide the actual values for the variables:

    ```hcl
    vpc_id       = "vpc-xxxxxxxx"            # Replace with your actual VPC ID
    aws_region       = "us-east-1"           # You can change this if needed
    ami_id       = "ami-0c02fb55956c7d316"   # Replace with your actual AMI ID
    instance_type = "t2.micro"               # Free tier instance type
    public_key_path = "replace-me "          # Ensure Windows path is properly escaped
    private_key_path = "replace-me"          # Ensure Windows path is properly escaped
    github_token    = "replace-me"           # user github token with next permissions:
                                               #  1. **Actions**: Access Read and write
                                               #  2. **Contents**: Access Read and write
                                               #  3. **Deployments**: Access Read and write
                                               #  4. **Environments**: Access Read-only
                                               #  5. **Metadata**: Access Read-only
                                               #  6. **Pull Requests**: Access Read-only
                                               #  7. **Secrets**: Access Read and write
                                               #  8. **Variables**: Access Read and write
                                               #  9. **Workflows**: Access Read and write
    github_owner    = "replace-me"           # username of github repository owner or just a user
    github_repository = "replace-me"         # Just the repository name
    github_repository_ssh_clone_url = ""     # URL to clone repository via ssh
    ecr_repository  = "replace-me"           # Just the ECR repository name
    ```


3. Initialize Terraform:

    ```bash
    terraform init
    ```

4. Create an execution plan:

    ```bash
    terraform plan
    ```

5. Apply the configuration to create the resources:

    ```bash
    terraform apply
    ```

    Confirm the action by typing `yes` when prompted.

### Destroying Resources

To destroy the resources created by Terraform, run the following command:

```bash
terraform destroy
```

Confirm the action by typing `yes` when prompted.

## Acknowledgments

- [Django](https://www.djangoproject.com/)
- [Django REST framework](https://www.django-rest-framework.org/)
- [Docker](https://www.docker.com/)
- [Poetry](https://python-poetry.org/)
- [Sentry](https://docs.sentry.io/)
- [Pylint](https://pypi.org/project/pylint/)
- [Anymail](https://anymail.dev/en/)
- [Django Extensions](https://pypi.org/project/django-extensions/)
- [Terraform](https://www.terraform.io/)