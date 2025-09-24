# ECR Deployment Quick Start Guide

**Deploy your OpenAI Strands Agent to AWS ECR in 5 minutes**

This guide assumes you have already set up your AWS account, IAM users, and roles. If not, see [AGENT_CORE_DEPLOYMENT_GUIDE.md](./AGENT_CORE_DEPLOYMENT_GUIDE.md) for complete AWS setup instructions.

## Prerequisites

Before starting, ensure you have:
- ✅ AWS Account with IAM user created
- ✅ Docker Desktop installed and running
- ✅ AWS CLI installed (`brew install awscli` on Mac)
- ✅ OpenAI API key

## Step 1: Clone and Configure Project

```bash
# Clone the repository
git clone <repository-url>
cd strands-ai-agentcore-demo

# Create environment file from template
cp .env.example .env
```

## Step 2: Configure Credentials

Edit `.env` file and add your credentials:

```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-proj-your-actual-openai-api-key-here

# AWS Configuration
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_DEFAULT_REGION=us-east-1
```

## Step 3: Configure AWS CLI

```bash
# Configure AWS CLI with your credentials
aws configure
# Enter when prompted:
# AWS Access Key ID: [your-access-key]
# AWS Secret Access Key: [your-secret-key]
# Default region name: us-east-1
# Default output format: json

# Verify credentials work
aws sts get-caller-identity
```

Expected output:
```json
{
    "UserId": "AIDAXXXXXX",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/your-username"
}
```

## Step 4: Deploy to ECR (Automated Script)

### Option A: Use the Deployment Script (Recommended)

```bash
# Load environment variables
set -a && source .env && set +a

# Run the deployment script
python deployment/simple_deploy.py
```

The script will automatically:
1. Create ECR repository
2. Build ARM64 Docker image
3. Push to ECR
4. Output the ECR URI for Agent Core configuration

### Option B: Manual Deployment

If the script fails or you prefer manual control:

```bash
# 1. Create ECR repository
aws ecr create-repository --repository-name openai-strands-agent --region us-east-1

# 2. Get your AWS account ID
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# 3. Login to ECR
aws ecr get-login-password --region us-east-1 | \
docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# 4. Build ARM64 Docker image (required for Agent Core)
docker buildx create --name agentcore-builder --use
docker buildx build --platform linux/arm64 -f deployment/Dockerfile -t openai-strands-agent:latest --load .

# 5. Tag image for ECR
docker tag openai-strands-agent:latest \
$AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/openai-strands-agent:latest

# 6. Push to ECR
docker push $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/openai-strands-agent:latest
```

## Step 5: Deploy to Agent Core

After pushing to ECR, you'll get an image URI like:
```
123456789012.dkr.ecr.us-east-1.amazonaws.com/openai-strands-agent:latest
```

### Via AWS Console:

1. Go to **AWS Bedrock → Agent Core → Runtime agents**
2. Click **Create runtime agent**
3. Configure:
   - **Container URI**: Your ECR image URI from above
   - **Port**: 8080
   - **IAM Role**: Select your AgentRuntimeRole
   - **Environment Variables**:
     - `OPENAI_API_KEY`: Your OpenAI API key
     - `OPENAI_MODEL`: gpt-4o-mini

### Via CLI (if available in your region):

```bash
# Replace with your values
ROLE_ARN="arn:aws:iam::$AWS_ACCOUNT_ID:role/AgentRuntimeRole"
IMAGE_URI="$AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/openai-strands-agent:latest"

python deployment/deploy_to_agentcore.py --role-arn $ROLE_ARN --region us-east-1
```

## Step 6: Test Your Deployment

Once deployed, test your agent:

```bash
# In AWS Console: Agent Core → Your Agent → Test tab
# Use this test payload:
{
  "prompt": "Hello! Can you calculate 25 * 8 for me?"
}
```

Expected response:
```json
{
  "result": {
    "role": "assistant",
    "content": [{"text": "The result of 25 × 8 is 200."}]
  }
}
```

## Common Issues and Solutions

### Issue: "Invalid security token"
```bash
# Solution: Refresh AWS credentials
aws configure
# Re-enter your access key and secret
```

### Issue: Docker buildx not found
```bash
# Solution: Create buildx builder
docker buildx create --name agentcore-builder --use
```

### Issue: ECR login fails
```bash
# Solution: Ensure Docker Desktop is running
open -a Docker  # On macOS
# Wait for Docker to start, then retry
```

### Issue: Platform mismatch error
```bash
# Solution: Always use --platform linux/arm64 flag
# Agent Core requires ARM64 architecture
docker buildx build --platform linux/arm64 ...
```

### Issue: Permission denied on ECR
```bash
# Solution: Attach ECR policy to your IAM user
# In AWS Console: IAM → Users → Your User → Add permissions
# Attach: AmazonEC2ContainerRegistryFullAccess
```

## Quick Command Reference

```bash
# Check AWS identity
aws sts get-caller-identity

# List ECR repositories
aws ecr describe-repositories --region us-east-1

# View Docker images
docker images | grep openai-strands-agent

# Clean up old Docker images
docker system prune -a

# View ECR images
aws ecr list-images --repository-name openai-strands-agent --region us-east-1
```

## Environment Variables Required

Your `.env` file must contain:
```bash
# Required for agent runtime
OPENAI_API_KEY=sk-proj-...
OPENAI_MODEL=gpt-4o-mini

# Required for deployment
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_DEFAULT_REGION=us-east-1
```

## Project Structure

Key files for deployment:
```
strands-ai-agentcore-demo/
├── .env                        # Your credentials (create from .env.example)
├── deployment/
│   ├── Dockerfile             # Container definition (ARM64)
│   ├── requirements.txt       # Python dependencies
│   ├── simple_deploy.py       # Automated deployment script
│   └── deploy_to_agentcore.py # Full Agent Core deployment
└── src/
    └── agents/
        └── openai_agent.py    # Main agent implementation
```

## Next Steps

1. **Create Gateway** for HTTP access - see [AGENT_CORE_DEPLOYMENT_GUIDE.md](./AGENT_CORE_DEPLOYMENT_GUIDE.md#manual-agent-core-deployment)
2. **Set up monitoring** with CloudWatch
3. **Configure auto-scaling** if needed
4. **Add custom tools** to your agent

## Support

- Full deployment guide: [AGENT_CORE_DEPLOYMENT_GUIDE.md](./AGENT_CORE_DEPLOYMENT_GUIDE.md)
- AWS Bedrock documentation: https://docs.aws.amazon.com/bedrock/
- Project issues: Create an issue in the repository

---

**Time to deployment: ~5 minutes** with proper AWS setup ⚡