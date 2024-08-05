# main.tf

provider "aws" {
  region = var.aws_region
}

provider "github" {
  token        = var.github_token
}

resource "aws_key_pair" "deployer" {
  key_name   = "deployer-key"
  public_key = file(var.public_key_path)
}

resource "aws_security_group" "sg_ssh" {
  name        = "sg_dev_ssh"
  description = "Allow SSH inbound traffic"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
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
  security_groups = [aws_security_group.sg_ssh.name]
  key_name      = aws_key_pair.deployer.key_name

  user_data = <<-EOF
              #!/bin/bash
              # Install Docker
              sudo amazon-linux-extras install docker -y
              sudo service docker start
              sudo usermod -a -G docker ec2-user

              # Install Git
              sudo yum install git -y

              # Download Docker Compose
              sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
              sudo chmod +x /usr/local/bin/docker-compose

              # Setup SSH for Git
              mkdir -p /home/ec2-user/.ssh
              echo var.git_private_key > /home/ec2-user/.ssh/id_rsa
              chmod 600 /home/ec2-user/.ssh/id_rsa
              echo "Host github.com\n\tStrictHostKeyChecking no\n" > /home/ec2-user/.ssh/config
              chown -R ec2-user:ec2-user /home/ec2-user/.ssh

              EOF

  tags = {
    Name = "development"
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

resource "github_actions_secret" "ec2_ip" {
  repository       = var.github_repository
  secret_name      = "EC2_IP"
  plaintext_value  = aws_instance.dev.public_ip
}

resource "github_actions_secret" "ec2_user" {
  repository       = var.github_repository
  secret_name      = "EC2_USER"
  plaintext_value  = "ec2-user"
}

resource "github_actions_secret" "ec2_private_key" {
  repository       = var.github_repository
  secret_name      = "EC2_PRIVATE_KEY"
  plaintext_value  = file(var.private_key_path)
}

resource "github_actions_secret" "aws_region" {
  repository       = var.github_repository
  secret_name      = "AWS_REGION"
  plaintext_value  = var.aws_region
}

resource "github_actions_secret" "ecr_repository" {
  repository       = var.github_repository
  secret_name      = "ECR_REPOSITORY"
  plaintext_value  = var.ecr_repository
}
