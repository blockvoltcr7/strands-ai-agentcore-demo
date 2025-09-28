# AWS IAM Setup Guide for ECR Deployment

This guide walks you through setting up AWS IAM users with the necessary permissions to deploy Docker images to Amazon ECR (Elastic Container Registry) for use with AWS Bedrock AgentCore.

## Prerequisites

- AWS Account with administrative access
- Access to AWS Management Console

## 📋 Overview

You'll need to:
1. Create an IAM user for ECR deployment
2. Attach the required permission policies
3. Generate access keys
4. Install and configure AWS CLI
5. Test the setup

## 🔐 Step 1: Create IAM User

### 1.1 Navigate to IAM Console
1. Sign in to the [AWS Management Console](https://console.aws.amazon.com/)
2. Navigate to **IAM** (Identity and Access Management)
3. Click **Users** in the left sidebar
4. Click **Create user**

### 1.2 Configure User Details
1. **User name**: Enter a descriptive name (e.g., `bedrock-developer`, `ecr-deployment-user`)
2. **Provide user access to the AWS Management Console**: ❌ **Leave unchecked** (this user is for programmatic access only)
3. Click **Next**

## 🛡️ Step 2: Attach Permission Policies

You need to attach the following AWS managed policies to your user:

### Required Policies

#### 2.1 Amazon ECR Full Access
- **Policy Name**: `AmazonEC2ContainerRegistryFullAccess`
- **Purpose**: Allows creating repositories, pushing/pulling images
- **Permissions**: Full ECR access including:
  - `ecr:GetAuthorizationToken`
  - `ecr:BatchCheckLayerAvailability`
  - `ecr:CompleteLayerUpload`
  - `ecr:CreateRepository`
  - `ecr:DescribeRepositories`
  - `ecr:InitiateLayerUpload`
  - `ecr:PutImage`
  - `ecr:UploadLayerPart`

#### 2.2 Bedrock Agent Core Full Access
- **Policy Name**: `AmazonBedrockAgentCoreFullAccess`
- **Purpose**: Allows creating and managing AgentCore runtimes
- **Required for**: Deploying agents to Bedrock AgentCore

#### 2.3 Additional Recommended Policies

##### For Advanced Users (Optional)
- **Policy Name**: `EC2InstanceProfileForImageBuilderECRContainerBuilds`
- **Purpose**: If using EC2 for building images
- **When needed**: Advanced deployment scenarios

### 2.4 Attach Policies to User
1. In the **Set permissions** step, select **Attach policies directly**
2. Search for and select the following policies:
   - ✅ `AmazonEC2ContainerRegistryFullAccess`
   - ✅ `AmazonBedrockAgentCoreFullAccess`
3. Click **Next**
4. Review the configuration
5. Click **Create user**

## 🔑 Step 3: Generate Access Keys

### 3.1 Create Access Key
1. After creating the user, click on the **user name** to open user details
2. Click the **Security credentials** tab
3. Scroll down to **Access keys** section
4. Click **Create access key**

### 3.2 Select Use Case
1. Choose **Command Line Interface (CLI)**
2. Check the confirmation box: "I understand the above recommendation..."
3. Click **Next**

### 3.3 Add Description (Optional)
1. Add a description tag (e.g., "ECR deployment for Strands AgentCore")
2. Click **Create access key**

### 3.4 Download Credentials
⚠️ **IMPORTANT**: This is your only chance to see the secret access key!

1. **Copy** or **Download** the credentials:
   - **Access Key ID**: `AKIA...` (starts with AKIA)
   - **Secret Access Key**: Long random string
2. Store these securely (password manager recommended)
3. Click **Done**

## 💻 Step 4: Install AWS CLI

### 4.1 Download AWS CLI

#### macOS
```bash
# Using Homebrew (recommended)
brew install awscli

# Or download installer
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /
```

#### Windows
```powershell
# Download and run the MSI installer
# https://awscli.amazonaws.com/AWSCLIV2.msi
```

#### Linux
```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

### 4.2 Verify Installation
```bash
aws --version
# Should output: aws-cli/2.x.x Python/3.x.x...
```

## ⚙️ Step 5: Configure AWS CLI

### 5.1 Run AWS Configure
```bash
aws configure
```

### 5.2 Enter Your Credentials
```
AWS Access Key ID [None]: AKIA****************SWOU
AWS Secret Access Key [None]: ****************************************
Default region name [None]: us-east-1
Default output format [None]: json
```

**Region Notes**:
- Use `us-east-1` for Bedrock AgentCore (most services available)
- Or choose your preferred region where Bedrock is available

### 5.3 Verify Configuration
```bash
# Check configuration
aws configure list

# Test credentials
aws sts get-caller-identity
```

Expected output:
```json
{
    "UserId": "AIDACKCEVSQ6C2EXAMPLE",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/bedrock-developer"
}
```

## 🧪 Step 6: Test ECR Access

### 6.1 Test ECR Authentication
```bash
# Test ECR login (replace with your region)
aws ecr get-login-password --region us-east-1
```

Should return a long token string (not an error).

### 6.2 List ECR Repositories
```bash
# List existing repositories
aws ecr describe-repositories --region us-east-1
```

If you have no repositories yet, this will return an empty list `[]`.

## 🚀 Step 7: Deploy Your First Image

Now you can use the deployment script:

```bash
# Navigate to your project
cd /path/to/strands-ai-agentcore-demo

# Deploy to ECR
python deployment/deploy_ecr.py
```

The script will:
1. ✅ Verify your AWS credentials
2. ✅ Create ECR repository (if needed)
3. ✅ Build Docker image
4. ✅ Push to ECR
5. ✅ Provide next steps for AgentCore deployment

## 🔒 Security Best Practices

### Access Key Security
- ❌ **Never** commit access keys to version control
- ❌ **Never** share access keys in chat/email
- ✅ **Use** AWS CLI profiles for multiple accounts
- ✅ **Rotate** access keys regularly (every 90 days)
- ✅ **Delete** unused access keys

### IAM User Management
- ✅ **Use** descriptive user names
- ✅ **Add** tags to identify purpose
- ✅ **Review** permissions regularly
- ✅ **Enable** CloudTrail for audit logging

### Alternative: IAM Roles (Advanced)
For production environments, consider using IAM roles instead of users:
- EC2 instance roles
- AWS SSO integration
- Cross-account roles

## 🛠️ Troubleshooting

### Common Issues

#### 1. "Access Denied" Errors
```
An error occurred (AccessDenied) when calling the GetAuthorizationToken operation
```

**Solutions**:
- Verify IAM policies are attached correctly
- Check if user has `AmazonEC2ContainerRegistryFullAccess`
- Ensure AWS CLI is configured with correct credentials

#### 2. "Region Not Supported" Errors
```
The security token included in the request is invalid
```

**Solutions**:
- Verify region supports Bedrock AgentCore
- Use `us-east-1` (most comprehensive service availability)
- Check `aws configure list` for correct region

#### 3. "Repository Not Found" Errors
```
RepositoryNotFoundException
```

**Solutions**:
- The deployment script creates repositories automatically
- Verify ECR permissions include `ecr:CreateRepository`
- Check repository name doesn't contain invalid characters

#### 4. Docker Build Failures
```
Error response from daemon: Get https://xxx.dkr.ecr.region.amazonaws.com/v2/
```

**Solutions**:
- Ensure Docker Desktop is running
- Run `aws ecr get-login-password` to test authentication
- Check internet connectivity

### Getting Help

#### Check Current Configuration
```bash
# View current AWS configuration
aws configure list

# Check identity
aws sts get-caller-identity

# Test ECR access
aws ecr describe-repositories --region us-east-1
```

#### Useful AWS CLI Commands
```bash
# List all IAM users
aws iam list-users

# List policies attached to user
aws iam list-attached-user-policies --user-name your-username

# List ECR repositories
aws ecr describe-repositories

# Get ECR login token
aws ecr get-login-password --region us-east-1
```

## 📚 Additional Resources

- [AWS IAM User Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/)
- [AWS CLI Configuration Guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)
- [Amazon ECR User Guide](https://docs.aws.amazon.com/AmazonECR/latest/userguide/)
- [AWS Bedrock AgentCore Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html)

## 🎯 Quick Reference

### Required IAM Policies
```
AmazonEC2ContainerRegistryFullAccess
AmazonBedrockAgentCoreFullAccess
```

### AWS CLI Setup Commands
```bash
# Install (macOS)
brew install awscli

# Configure
aws configure

# Test
aws sts get-caller-identity
aws ecr get-login-password --region us-east-1
```

### Deployment Command
```bash
python deployment/deploy_ecr.py
```

---

**Need help?** Check the troubleshooting section above or refer to the AWS documentation links.
