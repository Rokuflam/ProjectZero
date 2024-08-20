# Define the AWS provider, using the region specified in the variables
provider "aws" {
  region = var.aws_region
}

# Define the GitHub provider, using the token specified in the variables
provider "github" {
  token = var.github_token
}

# Create an ECS cluster
resource "aws_ecs_cluster" "stage_cluster" {
  name = "stage-cluster"
}

data "aws_iam_role" "ecs_task_execution_role" {
  name = "ecsTaskExecutionRole"  # Replace with your existing role name
}


# Create a security group for the ECS service
resource "aws_security_group" "ecs_service_sg" {
  name        = "ecs_service_sg"
  description = "Allow inbound traffic for ECS services"
  vpc_id      = var.vpc_id

  # Allow HTTP traffic on port 80 from any IP address
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow HTTPS traffic on port 443 from any IP address
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Define an ECS task definition
resource "aws_ecs_task_definition" "stage_task" {
  family                   = "stage-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  execution_role_arn       = data.aws_iam_role.ecs_task_execution_role.arn
  cpu                      = "256"
  memory                   = "512"

  container_definitions = jsonencode([
    {
      name      = "app"
      image     = "${var.ecr_repository}:${var.image_tag}"
      essential = true
      portMappings = [{
        containerPort = 80
        hostPort      = 80
      }]
    }
  ])
}

# Create an ECS service
resource "aws_ecs_service" "stage_service" {
  name            = "stage-service"
  cluster         = aws_ecs_cluster.stage_cluster.id
  task_definition = aws_ecs_task_definition.stage_task.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = var.subnets
    security_groups = [aws_security_group.ecs_service_sg.id]
    assign_public_ip = true
  }
}

# Create an ECR repository for the stage environment's application images
resource "aws_ecr_repository" "stage_app_repo" {
  name = var.ecr_repository

  # Enable image scanning on push
  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "stage-app-repo"
  }
}

# Store the ECS cluster name as a GitHub Actions secret
resource "github_actions_secret" "stage_ecs_cluster" {
  repository       = var.github_repository
  secret_name      = "stage_ECS_CLUSTER"
  plaintext_value  = aws_ecs_cluster.stage_cluster.name
}

# Store the ECS service name as a GitHub Actions secret
resource "github_actions_secret" "stage_ecs_service" {
  repository       = var.github_repository
  secret_name      = "stage_ECS_SERVICE"
  plaintext_value  = aws_ecs_service.stage_service.name
}

# Store the ECS task definition ARN as a GitHub Actions secret
resource "github_actions_secret" "stage_ecs_task_definition" {
  repository       = var.github_repository
  secret_name      = "stage_ECS_TASK_DEFINITION"
  plaintext_value  = aws_ecs_task_definition.stage_task.arn
}

# Store the private key for SSH access to the EC2 instance as a GitHub Actions secret
resource "github_actions_secret" "stage_ec2_private_key" {
  repository       = var.github_repository
  secret_name      = "stage_EC2_PRIVATE_KEY"
  plaintext_value  = file(var.private_key_path)
}

# Store the AWS region as a GitHub Actions secret
resource "github_actions_secret" "stage_aws_region" {
  repository       = var.github_repository
  secret_name      = "stage_AWS_REGION"
  plaintext_value  = var.aws_region
}

# Store the ECR repository name as a GitHub Actions secret
resource "github_actions_secret" "stage_ecr_repository" {
  repository       = var.github_repository
  secret_name      = "stage_ECR_REPOSITORY"
  plaintext_value  = var.ecr_repository
}

# Store the GitHub repository name as a GitHub Actions secret
resource "github_actions_secret" "repository_name" {
  repository       = var.github_repository
  secret_name      = "REPOSITORY_NAME"
  plaintext_value  = var.github_repository
}

# Store the SSH clone link of the GitHub repository as a GitHub Actions secret
resource "github_actions_secret" "ssh_clone_link" {
  repository       = var.github_repository
  secret_name      = "SSH_CLONE_LINK"
  plaintext_value  = var.github_repository_ssh_clone_url
}
