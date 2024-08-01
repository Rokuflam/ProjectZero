# variables.tf

variable "vpc_id" {
  description = "The VPC ID where the security group will be created"
  type        = string
}

variable "region" {
  description = "The AWS region to create resources in"
  type        = string
  default     = "us-east-1"  # Cheapest AWS region
}

variable "ami_id" {
  description = "The AMI ID for the EC2 instance"
  type        = string
  default     = "ami-0c02fb55956c7d316"  # Valid Amazon Linux 2 AMI ID for us-east-1
}

variable "instance_type" {
  description = "The EC2 instance type"
  type        = string
  default     = "t2.micro"
}
