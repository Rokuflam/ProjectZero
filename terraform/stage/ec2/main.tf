# Define the AWS provider using the specified region
provider "aws" {
  region = var.aws_region
}

# Define the GitHub provider using the token specified in the variables
provider "github" {
  token = var.github_token
}

# Read the local private key file and store its contents for later use
data "local_file" "private_key" {
  filename = var.private_key_path
}

# Create an AWS key pair for deployment using the public key specified in the variables
resource "aws_key_pair" "staging_deployer" {
  key_name   = "deployer-staging-key"
  public_key = file(var.public_key_path)
}

# Define a security group for the staging environment allowing SSH, HTTP, HTTPS, and PostgreSQL inbound traffic
resource "aws_security_group" "sg_staging_ssh" {
  name        = "sg_staging_ssh"
  description = "Allow SSH, HTTP, HTTPS, and PostgreSQL inbound traffic"
  vpc_id      = var.vpc_id

  # Allow SSH traffic on port 22 from any IP address
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

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

  # Allow PostgreSQL traffic on port 5432 from any IP address (adjust as needed for security)
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # For better security, replace with specific IP ranges
  }

  # Allow all outbound traffic from the instance
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Define an EC2 instance for the staging environment
resource "aws_instance" "staging" {
  ami           = var.ami_id
  instance_type = var.instance_type
  security_groups = [aws_security_group.sg_staging_ssh.name]
  key_name      = aws_key_pair.staging_deployer.key_name

  # Set up the instance with Docker, Docker Compose, Git, and configure SSH for GitHub access
  user_data = <<-EOF
            #!/bin/bash
            # Install Docker
            sudo amazon-linux-extras install docker -y
            sudo service docker start
            sudo usermod -a -G docker ec2-user

            # Download Docker Compose
            sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
            sudo chmod +x /usr/local/bin/docker-compose

            # Install Git
            sudo yum install git -y

            # Setup SSH for Git
            mkdir -p /home/ec2-user/.ssh
            echo '${data.local_file.private_key.content}' > /home/ec2-user/.ssh/id_rsa
            chmod 600 /home/ec2-user/.ssh/id_rsa
            echo "Host github.com\n\tStrictHostKeyChecking no\n" > /home/ec2-user/.ssh/config
            chown -R ec2-user:ec2-user /home/ec2-user/.ssh
            ssh-keyscan github.com >> ~/.ssh/known_hosts
            EOF

  # Tag the instance as "staging"
  tags = {
    Name = "staging"
  }
}

# Allocate and associate an Elastic IP address to the staging EC2 instance
resource "aws_eip" "staging_eip" {
  instance = aws_instance.staging.id
  domain   = "vpc"
  tags = {
    Name = "staging-eip"
  }
}

# Create an ECR repository for the staging environment's application images
resource "aws_ecr_repository" "staging_app_repo" {
  name = var.ecr_repository

  # Enable image scanning on push
  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "staging-app-repo"
  }
}

# Store the staging EC2 instance's public IP as a GitHub Actions secret
resource "github_actions_secret" "staging_ec2_ip" {
  repository       = var.github_repository
  secret_name      = "STAGING_EC2_IP"
  plaintext_value  = aws_eip.staging_eip.public_ip
}

# Store the EC2 user name as a GitHub Actions secret
resource "github_actions_secret" "staging_ec2_user" {
  repository       = var.github_repository
  secret_name      = "STAGING_EC2_USER"
  plaintext_value  = "ec2-user"
}

# Store the private key for SSH access to the EC2 instance as a GitHub Actions secret
resource "github_actions_secret" "staging_ec2_private_key" {
  repository       = var.github_repository
  secret_name      = "STAGING_EC2_PRIVATE_KEY"
  plaintext_value  = file(var.private_key_path)
}

# Store the AWS region as a GitHub Actions secret
resource "github_actions_secret" "staging_aws_region" {
  repository       = var.github_repository
  secret_name      = "STAGING_AWS_REGION"
  plaintext_value  = var.aws_region
}

# Store the ECR repository name as a GitHub Actions secret
resource "github_actions_secret" "staging_ecr_repository" {
  repository       = var.github_repository
  secret_name      = "STAGING_ECR_REPOSITORY"
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

# Define an RDS instance for the staging environment (PostgreSQL)
resource "aws_db_instance" "staging_rds" {
  identifier              = "staging-rds"
  allocated_storage       = 20
  storage_type            = "gp2"
  engine                  = "postgres"
  engine_version          = "16.3"
  instance_class          = "db.t3.micro"
  db_name                 = var.db_name
  username                = var.db_username
  password                = var.db_password
  parameter_group_name    = "default.postgres16"
  publicly_accessible     = true
  skip_final_snapshot     = true
  vpc_security_group_ids  = [aws_security_group.sg_staging_ssh.id]

  tags = {
    Name = "staging-rds"
  }
}

# Define an ElastiCache Redis cluster for the staging environment
resource "aws_elasticache_cluster" "staging_redis" {
  cluster_id           = "staging-redis"
  engine               = "redis"
  node_type            = "cache.t3.micro"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis7"
  port                 = 6379
  subnet_group_name    = aws_elasticache_subnet_group.staging.name
  security_group_ids   = [aws_security_group.sg_staging_ssh.id]

  tags = {
    Name = "staging-redis"
  }
}

# Create a subnet group for ElastiCache
resource "aws_elasticache_subnet_group" "staging" {
  name       = "staging-subnet-group"
  subnet_ids = var.subnet_ids

  tags = {
    Name = "staging-subnet-group"
  }
}
