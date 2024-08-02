# deploy.tpl
name: Deploy to EC2

on:
  push:
    branches:
      - development

jobs:
  build_and_deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Log in to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v1
        with:
          region: secrets.AWS_REGION

      - name: Build, tag, and push image to ECR
        run: |
          docker build -t steps.login-ecr.outputs.registry/secrets.ECR_REPOSITORY:github.sha .
          docker push steps.login-ecr.outputs.registry/secrets.ECR_REPOSITORY:github.sha
        env:
          AWS_REGION: secrets.AWS_REGION
          ECR_REPOSITORY: secrets.ECR_REPOSITORY
          IMAGE_TAG: github.sha

      - name: Set up SSH
        run: |
          mkdir -p ~/.ssh
          echo "secrets.EC2_PRIVATE_KEY" > ~/.ssh/id_rsa
          chmod 600 ~/.ssh/id_rsa
          ssh-keyscan -H secrets.EC2_IP >> ~/.ssh/known_hosts

      - name: Deploy to EC2
        run: |
          ssh -o StrictHostKeyChecking=no secrets.EC2_USER@secrets.EC2_IP << 'EOF'
            aws ecr get-login-password --region secrets.AWS_REGION | docker login --username AWS --password-stdin steps.login-ecr.outputs.registry
            docker pull steps.login-ecr.outputs.registry/secrets.ECR_REPOSITORY:github.sha
            cd /path/to/your/app
            docker-compose down
            docker-compose up -d --build
          EOF
