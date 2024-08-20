# AWS region where the ECR repository is located.
# The default region is set to "us-east-1".
variable "aws_region" {
  description = "The AWS region where the ECR repository is located"
  default     = "us-east-1"
}

# The ID of the VPC where the security group will be created.
# This value must be provided by the user.
variable "vpc_id" {
  description = "The ID of the VPC where the security group will be created"
}

# The Amazon Machine Image (AMI) ID to be used for the EC2 instance.
# This value must be provided by the user.
variable "ami_id" {
  description = "The AMI ID for the EC2 instance"
}

# The instance type for the EC2 instance.
# The default instance type is set to "t2.micro".
variable "instance_type" {
  description = "The instance type for the EC2 instance"
  default     = "t2.micro"
}

# Path to the public key file used for SSH access to the EC2 instance.
variable "public_key_path" {
  description = "The path to the public key for SSH access"
}

# Path to the private key file used for SSH access to the EC2 instance.
variable "private_key_path" {
  description = "The path to the private key for SSH access"
}

# The GitHub token used for authenticating API requests.
# This variable is marked as sensitive to ensure it is not accidentally exposed.
variable "github_token" {
  description = "The GitHub token for authentication"
  type        = string
  sensitive   = true
}

# The GitHub owner, which can be a user or organization.
# This must be provided by the user.
variable "github_owner" {
  description = "The GitHub owner (user or organization)"
}

# The name of the GitHub repository where secrets and other configurations will be stored.
variable "github_repository" {
  description = "The GitHub repository name"
}

# The SSH URL used to clone the GitHub repository.
variable "github_repository_ssh_clone_url" {
  description = "URL to clone repository via ssh"
  type        = string
}

# The name of the Amazon Elastic Container Registry (ECR) repository.
# The default value is set to "app-repo".
variable "ecr_repository" {
  description = "The name of the ECR repository"
  default     = "app-repo"
}

variable "subnets" {
  description = "The subnets where the ECS service will be deployed"
  type        = list(string)
}

# The Docker image tag to be used in the ECS task definition.
# This variable allows specifying the version of the image to deploy.
variable "image_tag" {
  description = "The Docker image tag to use in the ECS task definition"
  default     = "latest"
}

# The ARN of the ECS task execution role.
# This role allows the ECS tasks to interact with AWS services like ECR.
variable "ecs_task_execution_role_arn" {
  description = "The ARN of the ECS task execution role"
  type        = string
}

# The ECS cluster name.
# This variable specifies the name of the ECS cluster where the service will run.
variable "ecs_cluster_name" {
  description = "The name of the ECS cluster"
  default     = "development-cluster"
}

# The name of the ECS service.
# This variable specifies the name of the ECS service within the cluster.
variable "ecs_service_name" {
  description = "The name of the ECS service"
  default     = "development-service"
}
