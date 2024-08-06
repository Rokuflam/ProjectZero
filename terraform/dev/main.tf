# main.tf

provider "aws" {
  region = var.aws_region
}

provider "github" {
  token = var.github_token
}

data "local_file" "private_key" {
  filename = var.private_key_path
}

resource "aws_key_pair" "dev_deployer" {
  key_name   = "deployer-dev-key"
  public_key = file(var.public_key_path)
}

resource "aws_security_group" "sg_dev_ssh" {
  name        = "sg_dev_ssh"
  description = "Allow SSH inbound traffic"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "dev" {
  ami           = var.ami_id
  instance_type = var.instance_type
  security_groups = [aws_security_group.sg_dev_ssh.name]
  key_name      = aws_key_pair.dev_deployer.key_name

  user_data = <<-EOF
            #!/bin/bash
            # Install Docker
            sudo amazon-linux-extras install docker -y
            sudo service docker start
            sudo usermod -a -G docker dev-ec2-user

            # Download Docker Compose
            sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
            sudo chmod +x /usr/local/bin/docker-compose

            # Install Git
            sudo yum install git -y

            # Setup SSH for Git
            mkdir -p /home/dev-ec2-user/.ssh
            echo '${data.local_file.private_key.content}' > /home/dev-ec2-user/.ssh/id_rsa
            chmod 600 /home/dev-ec2-user/.ssh/id_rsa
            echo "Host github.com\n\tStrictHostKeyChecking no\n" > /home/dev-ec2-user/.ssh/config
            chown -R dev-ec2-user:dev-ec2-user /home/dev-ec2-user/.ssh
            EOF

  tags = {
    Name = "development"
  }
}

resource "aws_eip" "dev_eip" {
  instance = aws_instance.dev.id
  domain   = "vpc"
  tags = {
    Name = "development-eip"
  }
}

resource "aws_ecr_repository" "development_app_repo" {
  name = var.ecr_repository

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "development-app-repo"
  }
}

resource "github_actions_secret" "dev_ec2_ip" {
  repository       = var.github_repository
  secret_name      = "DEV_EC2_IP"
  plaintext_value  = aws_eip.dev_eip.public_ip
}

resource "github_actions_secret" "dev_ec2_user" {
  repository       = var.github_repository
  secret_name      = "DEV_EC2_USER"
  plaintext_value  = "dev-ec2-user"
}

resource "github_actions_secret" "dev_ec2_private_key" {
  repository       = var.github_repository
  secret_name      = "DEV_EC2_PRIVATE_KEY"
  plaintext_value  = file(var.private_key_path)
}

resource "github_actions_secret" "dev_aws_region" {
  repository       = var.github_repository
  secret_name      = "DEV_AWS_REGION"
  plaintext_value  = var.aws_region
}

resource "github_actions_secret" "dev_ecr_repository" {
  repository       = var.github_repository
  secret_name      = "DEV_ECR_REPOSITORY"
  plaintext_value  = var.ecr_repository
}
