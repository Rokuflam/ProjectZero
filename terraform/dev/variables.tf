# variables.tf

variable "aws_region" {
  description = "The AWS region where the ECR repository is located"
  default     = "us-east-1"
}

variable "vpc_id" {
  description = "The ID of the VPC where the security group will be created"
}

variable "ami_id" {
  description = "The AMI ID for the EC2 instance"
}

variable "instance_type" {
  description = "The instance type for the EC2 instance"
  default     = "t2.micro"
}

variable "public_key_path" {
  description = "The path to the public key for SSH access"
}

variable "private_key_path" {
  description = "The path to the private key for SSH access"
}

variable "github_token" {
  description = "The GitHub token for authentication"
  type        = string
  sensitive   = true
}

variable "github_owner" {
  description = "The GitHub owner (user or organization)"
}

variable "github_repository" {
  description = "The GitHub repository name"
}

variable "ecr_repository" {
  description = "The name of the ECR repository"
  default     = "app-repo"
}
