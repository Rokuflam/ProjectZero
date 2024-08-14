## Tutorial Guide: Deploying a Development Environment with AWS Console

This guide will walk you through the process of deploying a development environment using AWS Console. The tutorial assumes you are using AWS as your cloud provider. By the end of this guide, you'll have a basic infrastructure set up.

### **Prerequisites**

Before starting, make sure you have:

- An AWS account with appropriate permissions.
- A GitHub account with a repository where you want to store secrets and configurations.
### **Step 1: Create an IAM User with Specific Permissions**

#### **1.1 Navigate to IAM in the AWS Management Console**

1. **Login to AWS Console**: Go to the [AWS Management Console](https://aws.amazon.com/console/) and log in.
2. **Search for IAM**: In the search bar at the top, type "IAM" and select "IAM" from the dropdown options.

#### **1.2 Create a New IAM User**

1. **Go to Users**:
   - In the left-hand menu, click on "Users."
   - Click "Add users."
2. **Set User Details**:
   - **User Name**: Enter a user name, for example, `dev-deployer`.
   - **Access Type**: Select "Programmatic access" to allow the user to interact with AWS via the CLI, SDKs, or APIs.
   - Click "Next: Permissions."

#### **1.3 Attach Policies to the User**

1. **Create a Custom Policy** (for specific permissions not covered by the existing policies):
   - Click on "Create policy" in the "Set permissions" page.
   - Go to the "JSON" tab and replace the default JSON with the following custom policy:

    ```json
   {
      "Version": "2012-10-17",
      "Statement": [
         {
               "Effect": "Allow",
               "Action": [
                  "ec2:DescribeInstances",
                  "ec2:DescribeInstanceStatus",
                  "ec2:StartInstances",
                  "ec2:StopInstances",
                  "ec2:RebootInstances",
                  "ec2:DescribeInstanceAttribute",
                  "ec2:ModifyInstanceAttribute",
                  "ec2:DescribeSecurityGroups",
                  "ec2:DescribeImages",
                  "ec2:DescribeKeyPairs",
                  "ssm:SendCommand",
                  "ssm:ListCommands",
                  "ssm:ListCommandInvocations"
               ],
               "Resource": "*"
         },
         {
               "Effect": "Allow",
               "Action": [
                  "ecr:GetAuthorizationToken",
                  "ecr:BatchCheckLayerAvailability",
                  "ecr:GetDownloadUrlForLayer",
                  "ecr:BatchGetImage",
                  "ecr:PutImage",
                  "ecr:InitiateLayerUpload",
                  "ecr:UploadLayerPart",
                  "ecr:CompleteLayerUpload",
                  "ecr:CreateRepository",
                  "ecr:DeleteRepository",
                  "ecr:DescribeRepositories"
               ],
               "Resource": "*"
         },
         {
               "Effect": "Allow",
               "Action": [
                  "s3:GetObject",
                  "s3:PutObject",
                  "s3:ListBucket"
               ],
               "Resource": "*"
         }
      ]
   }
    ```
   - Click "Review policy."
   - **Name the Policy**: Give it a name like `CustomEC2ECRPolicy`.
   - Click "Create policy."

3. **Attach the Custom Policy**:
   - After creating the custom policy, go back to the "Attach policies" page, search for your custom policy by name, and select it.
   - Click "Next: Tags."

#### **1.4 Review and Create the User**

1. **Review**: On the "Review" page, ensure that all selected policies are attached.
2. **Create User**: Click "Create user."

#### **1.5 Save Access Keys**

1. **Download the Credentials**:
   - After the user is created, AWS will display the user's access key ID and secret access key.
   - Click "Download .csv" to save these credentials securely. You'll need these for configuring the AWS CLI.

### **Step 2: Setting Up AWS Resources Using AWS Management Console**

#### **2.1 Create an EC2 Key Pair**

1. **Navigate to EC2 Dashboard**: Use the search bar at the top to search for "EC2" and select the EC2 service.
2. **Create a Key Pair**:
   - In the left-hand menu, select "Key Pairs" under "Network & Security."
   - Click on "Create Key Pair."
   - Name your key pair (e.g., `deployer-dev-key`).
   - Choose the key pair file format (`.pem` for Linux/Mac, `.ppk` for Windows).
   - Click "Create Key Pair." The file will download automatically; keep it secure.

#### **2.2 Set Up a Security Group**

1. **Navigate to Security Groups**:
   - Still in the EC2 dashboard, select "Security Groups" under "Network & Security."
   - Click "Create security group."
2. **Configure Security Group**:
   - **Name**: Give it a name, e.g., `sg_dev_ssh`.
   - **Description**: Add a description like "Allow SSH, HTTP, and HTTPS traffic."
   - **VPC**: Select the VPC where your instances will be deployed.
3. **Add Inbound Rules**:
   - Click "Add Rule" and configure the following:
     - **Type**: SSH | **Protocol**: TCP | **Port Range**: 22 | **Source**: 0.0.0.0/0
     - **Type**: HTTP | **Protocol**: TCP | **Port Range**: 80 | **Source**: 0.0.0.0/0
     - **Type**: HTTPS | **Protocol**: TCP | **Port Range**: 443 | **Source**: 0.0.0.0/0
   - Click "Create security group."

#### **2.3 Launch an EC2 Instance**

1. **Navigate to EC2 Instances**:
   - In the EC2 dashboard, click "Instances" in the left-hand menu, then "Launch Instance."
2. **Configure Instance**:
   - **Name**: Add a name like `development`.
   - **AMI**: Choose an appropriate Amazon Machine Image (e.g., Amazon Linux 2 AMI).
   - **Instance Type**: Select `t2.micro` (eligible for free tier).
   - **Key Pair**: Select the key pair you created earlier (`deployer-dev-key`).
   - **Network Settings**: Choose the security group (`sg_dev_ssh`).
3. **Configure Storage**: Adjust storage if needed, but the default should suffice.
4. **Launch Instance**: Click "Launch Instance" to start the EC2 instance.

#### **2.4 Allocate and Associate an Elastic IP**

1. **Navigate to Elastic IPs**:
   - In the EC2 dashboard, scroll down to "Elastic IPs" under "Network & Security."
   - Click "Allocate Elastic IP address."
   - Choose the "Amazon pool" and click "Allocate."
2. **Associate Elastic IP**:
   - After allocation, select "Actions" and then "Associate Elastic IP address."
   - Choose your EC2 instance (`development`) and click "Associate."

#### **2.5 Set Up an ECR Repository**

1. **Navigate to ECR**:
   - Use the search bar to find and select "ECR" (Elastic Container Registry).
   - Click "Create repository."
2. **Create Repository**:
   - **Repository Name**: Enter a name like `development-app-repo`.
   - **Scan on Push**: Enable this to scan images for vulnerabilities.
   - Click "Create repository."

### **Step 3: Configuring GitHub Secrets**

#### **3.1 Add GitHub Secrets**

1. **Navigate to Your Repository**:
   - Go to [GitHub](https://github.com/) and navigate to the repository where you want to store the secrets.
2. **Go to Settings**:
   - Click on "Settings" in your repository.
   - Select "Secrets and variables" from the left-hand menu, then "Actions."
   - Click "New repository secret."
3. **Add Secrets**:
   - **DEV_EC2_IP**: Enter the public IP of your EC2 instance.
   - **DEV_EC2_USER**: Enter `ec2-user`.
   - **DEV_EC2_PRIVATE_KEY**: Open your private key file, copy its contents, and paste it here.
   - **DEV_AWS_REGION**: Enter your AWS region (e.g., `us-east-1`).
   - **DEV_ECR_REPOSITORY**: Enter the name of your ECR repository (`development-app-repo`).
   - **REPOSITORY_NAME**: Enter your GitHub repository name.
   - **SSH_CLONE_LINK**: Enter the SSH clone link of your repository.
   - **AWS_ACCESS_KEY_ID**: Enter the access key id of the IAM user you've created in the first step.
   - **AWS_SECRET_ACCESS_KEY**: Enter the secret key id of the IAM user you've created in the first step.

### **Step 4: Configure the EC2 Instance**

1. **Connect to the EC2 Instance**:
   - In the EC2 dashboard, select your instance and click "Connect."
   - Follow the instructions to SSH into the instance using your key pair.
2. **Install Docker, Docker Compose, and Git**:
   - Run the following commands:
     ```bash
     sudo yum install -y docker
     sudo systemctl start docker
     sudo systemctl enable docker
     sudo usermod -aG docker $USER
     sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
     sudo chmod +x /usr/local/bin/docker-compose
     sudo yum install -y git
     ```
3. **Set Up SSH for GitHub**:
   - Create the SSH directory and add your private key:
     ```bash
     mkdir -p /home/ec2-user/.ssh
     echo '<PRIVATE_KEY_CONTENT>' > /home/ec2-user/.ssh/id_rsa
     sudo chmod 600 /home/ec2-user/.ssh/id_rsa
     echo "Host github.com\n\tStrictHostKeyChecking no\n" > /home/ec2-user/.ssh/config
     sudo chown -R ec2-user:ec2-user /home/ec2-user/.ssh
     ssh-keyscan github.com >> ~/.ssh/known_hosts
     ```

### **Conclusion**

By following these steps, you have successfully set up a development environment on AWS using the AWS Management Console and GitHub UI. This approach allows you to manage your infrastructure manually without the need for Terraform, providing a straightforward way to deploy and configure your environment.