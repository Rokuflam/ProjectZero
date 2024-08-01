# main.tf

provider "aws" {
  region = var.region
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

  tags = {
    Name = "development"
  }
}
