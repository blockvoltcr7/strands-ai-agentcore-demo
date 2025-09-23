# Complete AWS Agent Core Deployment Guide

**Deploy OpenAI Strands Agents to AWS Bedrock Agent Core - Manual Console Approach**

This guide provides step-by-step instructions for deploying OpenAI Strands Agents to AWS Bedrock Agent Core using the AWS console interface. It's based on real-world deployment experience and focuses on the manual approach since automated CLI deployment often fails due to service availability and permission issues.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [AWS Account Setup](#aws-account-setup)
3. [IAM Configuration](#iam-configuration)
4. [ECR Repository Setup](#ecr-repository-setup)
5. [Docker Image Preparation](#docker-image-preparation)
6. [Manual Agent Core Deployment](#manual-agent-core-deployment)
7. [Environment Configuration](#environment-configuration)
8. [Testing & Validation](#testing--validation)
9. [Observability Setup](#observability-setup)
10. [Troubleshooting](#troubleshooting)
11. [Cost Management](#cost-management)

---

## Prerequisites

Before starting, ensure you have:

- ✅ AWS Account with administrative access
- ✅ OpenAI API Key ([Get one here](https://platform.openai.com/api-keys))
- ✅ Docker Desktop installed and running
- ✅ AWS CLI installed and configured
- ✅ This project cloned locally
- ✅ Basic understanding of Docker and AWS services

**Required Software Versions:**
- Docker: 20.10+ with buildx support
- AWS CLI: 2.0+
- Python: 3.12+

---

## AWS Account Setup

### Step 1: Secure Your Root Account

1. **Enable MFA on Root Account**
   - Sign in to [AWS Console](https://console.aws.amazon.com/) as root
   - Navigate to **Security credentials**
   - Enable **Multi-factor authentication (MFA)**
   - Use Google Authenticator or similar app

2. **Set Billing Alerts**
   - Go to **Billing Dashboard** → **Billing preferences**
   - Enable **Receive Billing Alerts**
   - Set up budget alerts for cost control

### Step 2: Enable Required AWS Services

1. **Enable Amazon Bedrock**
   - Search for "Bedrock" in AWS Console
   - Navigate to **Amazon Bedrock**
   - Request model access for:
     - ✅ Anthropic Claude 3 Haiku
     - ✅ Anthropic Claude 3 Sonnet
     - ✅ Anthropic Claude 3.5 Sonnet

2. **Enable Bedrock Agent Core**
   - In Bedrock console, look for **Agent Core** or **Runtime Management**
   - If not available, check service availability in your region
   - **Note:** Agent Core may not be available in all regions

---

## IAM Configuration

### Step 3: Create Development User

Create a dedicated IAM user for development work (never use root for daily operations).

1. **Create IAM User**
   ```
   Navigate to: IAM Console → Users → Create user

   User Details:
   - Username: bedrock-developer
   - ✅ Provide user access to AWS Management Console
   - Console access: I want to create an IAM user
   - Set custom password
   - ❌ Uncheck "Users must create a new password at next sign-in"
   ```

2. **Attach Required Policies**

   Select **Attach policies directly** and add:
   - `AmazonBedrockFullAccess`
   - `AmazonEC2ContainerRegistryFullAccess`
   - `IAMReadOnlyAccess` (for role management)

   **If AmazonBedrockFullAccess doesn't exist, create custom policy:**

   ```json
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Action": [
                   "bedrock:*",
                   "bedrock-agentcore:*"
               ],
               "Resource": "*"
           },
           {
               "Effect": "Allow",
               "Action": [
                   "logs:CreateLogGroup",
                   "logs:CreateLogStream",
                   "logs:PutLogEvents",
                   "logs:DescribeLogGroups",
                   "logs:DescribeLogStreams"
               ],
               "Resource": "*"
           }
       ]
   }
   ```

3. **Create Access Keys**
   ```
   Navigate to: IAM → Users → bedrock-developer → Security credentials

   Access Keys Section:
   - Click "Create access key"
   - Use case: Command Line Interface (CLI)
   - Description: "bedrock-agentcore-deployment"

   ⚠️ CRITICAL: Save both Access Key ID and Secret Access Key securely
   ```

### Step 4: Create Agent Runtime Role

Agent Core requires a specific IAM role to execute your agent.

1. **Create the Role**
   ```
   Navigate to: IAM Console → Roles → Create role

   Trusted Entity:
   - AWS service
   - Use case: Bedrock (if available) or Custom trust policy
   ```

2. **Trust Policy** (if using custom):
   ```json
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Principal": {
                   "Service": "bedrock.amazonaws.com"
               },
               "Action": "sts:AssumeRole"
           },
           {
               "Effect": "Allow",
               "Principal": {
                   "Service": "bedrock-agentcore.amazonaws.com"
               },
               "Action": "sts:AssumeRole"
           }
       ]
   }
   ```

3. **Attach Permissions Policy**:
   ```json
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Action": [
                   "logs:CreateLogGroup",
                   "logs:CreateLogStream",
                   "logs:PutLogEvents",
                   "logs:DescribeLogGroups",
                   "logs:DescribeLogStreams"
               ],
               "Resource": "*"
           },
           {
               "Effect": "Allow",
               "Action": [
                   "bedrock:InvokeModel",
                   "bedrock:InvokeModelWithResponseStream"
               ],
               "Resource": "*"
           }
       ]
   }
   ```

4. **Name the Role**: `AgentRuntimeRole`

5. **Copy the ARN**: `arn:aws:iam::YOUR-ACCOUNT-ID:role/AgentRuntimeRole`

---

## ECR Repository Setup

### Step 5: Configure AWS CLI

1. **Set AWS Credentials**
   ```bash
   aws configure
   # Enter your Access Key ID
   # Enter your Secret Access Key
   # Default region: us-east-1
   # Default output format: json
   ```

2. **Verify Configuration**
   ```bash
   aws sts get-caller-identity
   # Should return your bedrock-developer user info
   ```

### Step 6: Create ECR Repository

1. **Create Repository via Console**
   ```
   Navigate to: ECR Console → Repositories → Create repository

   Repository Configuration:
   - Visibility: Private
   - Repository name: openai-strands-agent
   - Tag immutability: Disabled (for easier development)
   - Image scanning: Enabled (recommended for security)
   - Encryption: Enabled with default KMS key
   ```

2. **Alternative: Create via CLI**
   ```bash
   aws ecr create-repository \
     --repository-name openai-strands-agent \
     --region us-east-1
   ```

3. **Note the Repository URI**:
   ```
   YOUR-ACCOUNT-ID.dkr.ecr.us-east-1.amazonaws.com/openai-strands-agent
   ```

---

## Docker Image Preparation

### Step 7: Prepare OpenAI Configuration

1. **Create Environment File**
   ```bash
   cp .env.example .env
   ```

2. **Configure OpenAI API Key** in `.env`:
   ```bash
   # OpenAI Configuration
   OPENAI_API_KEY=sk-proj-your-actual-openai-api-key-here

   # Agent Configuration
   OPENAI_MODEL=gpt-4o-mini
   OPENAI_MAX_TOKENS=2000
   OPENAI_TEMPERATURE=0.7
   HOST=0.0.0.0
   PORT=8080
   ```

### Step 8: Build ARM64 Docker Image

Agent Core requires ARM64 architecture. Follow these steps carefully:

1. **Set up Docker Buildx for ARM64**
   ```bash
   # Create buildx builder (if not exists)
   docker buildx create --name agentcore-builder --use

   # Verify buildx is working
   docker buildx ls
   ```

2. **Build the Docker Image**
   ```bash
   # From your project root directory
   docker buildx build \
     --platform linux/arm64 \
     -f deployment/Dockerfile \
     -t openai-strands-agent:latest \
     --load \
     .
   ```

   **Expected Output:**
   ```
   [+] Building 45.2s (12/12) FINISHED
   => [internal] load build definition from Dockerfile
   => [internal] load .dockerignore
   => [1/7] FROM docker.io/library/python:3.12-slim
   => [2/7] WORKDIR /app
   => [3/7] RUN apt-get update && apt-get install -y build-essential curl
   => [4/7] COPY deployment/requirements.txt .
   => [5/7] RUN pip install --no-cache-dir -r requirements.txt
   => [6/7] COPY src/ ./src/
   => [7/7] COPY .env.example .env
   => exporting to docker image format
   ```

3. **Verify Image Creation**
   ```bash
   docker images | grep openai-strands-agent
   # Should show your image with ARM64 architecture
   ```

### Step 9: Push to ECR

1. **Login to ECR**
   ```bash
   aws ecr get-login-password --region us-east-1 | \
   docker login --username AWS --password-stdin \
   YOUR-ACCOUNT-ID.dkr.ecr.us-east-1.amazonaws.com
   ```

2. **Tag Image for ECR**
   ```bash
   docker tag openai-strands-agent:latest \
   YOUR-ACCOUNT-ID.dkr.ecr.us-east-1.amazonaws.com/openai-strands-agent:latest
   ```

3. **Push to ECR**
   ```bash
   docker push YOUR-ACCOUNT-ID.dkr.ecr.us-east-1.amazonaws.com/openai-strands-agent:latest
   ```

   **Expected Output:**
   ```
   The push refers to repository [YOUR-ACCOUNT-ID.dkr.ecr.us-east-1.amazonaws.com/openai-strands-agent]
   abc123def456: Pushed
   def456ghi789: Pushed
   latest: digest: sha256:abcd1234... size: 856
   ```

---

## Manual Agent Core Deployment

### Step 10: Deploy via AWS Console

Since the CLI often fails due to service availability, use the manual console approach:

1. **Navigate to Bedrock Agent Core**
   ```
   AWS Console → Amazon Bedrock → Agent Core (or Runtime Management)

   If not available:
   - Try different regions (us-east-1, us-west-2)
   - Contact AWS support for Agent Core access
   ```

2. **Create New Agent Runtime**
   ```
   Click: Create runtime agent (or similar button)

   Basic Configuration:
   - Runtime name: hosted-agent-openai
   - Description: OpenAI Strands Agent with Calculator Tool
   ```

3. **Container Configuration**
   ```
   Container Settings:
   - Container URI: YOUR-ACCOUNT-ID.dkr.ecr.us-east-1.amazonaws.com/openai-strands-agent:latest
   - Port: 8080 (required by Agent Core)
   - Health check path: /ping
   ```

4. **IAM Role Configuration**
   ```
   Execution Role:
   - Use existing role: AgentRuntimeRole
   - ARN: arn:aws:iam::YOUR-ACCOUNT-ID:role/AgentRuntimeRole
   ```

5. **Network Configuration**
   ```
   Network Settings:
   - Network mode: Public (for external access)
   - VPC: Default VPC (or custom if needed)
   ```

### Step 11: Environment Variables

**Critical Step:** Configure the OpenAI API key in the runtime environment.

1. **Add Environment Variables**
   ```
   In the Agent Core configuration:

   Environment Variables:
   - OPENAI_API_KEY: sk-proj-your-actual-openai-api-key-here
   - OPENAI_MODEL: gpt-4o-mini
   - OPENAI_MAX_TOKENS: 2000
   - OPENAI_TEMPERATURE: 0.7
   - HOST: 0.0.0.0
   - PORT: 8080
   ```

2. **Deploy the Runtime**
   ```
   Click: Create runtime (or Deploy)

   Expected Status: Creating → Running
   Time: 2-5 minutes for initial deployment
   ```

---

## Testing & Validation

### Step 12: Test Your Deployed Agent

1. **Find Your Agent in Console**
   ```
   Navigate to: Bedrock Agent Core → Runtime agents
   Find: hosted-agent-openai
   Status should be: Running
   ```

2. **Use Built-in Test Interface**
   ```
   Click on your agent → Test tab

   Test Payload:
   {
     "prompt": "Hello! Can you calculate 25 * 8 for me?"
   }

   Expected Response:
   {
     "result": {
       "role": "assistant",
       "content": [
         {
           "text": "The result of 25 × 8 is 200."
         }
       ]
     }
   }
   ```

3. **Verify Calculator Tool Works**
   ```
   Test more complex calculations:
   {
     "prompt": "What's the square root of 144 plus 15 multiplied by 3?"
   }
   ```

### Step 13: Monitor Logs

1. **Access CloudWatch Logs**
   ```
   Navigate to: CloudWatch → Log groups
   Look for: /aws/bedrock-agentcore/runtimes/your-agent-id
   ```

2. **Expected Log Entries**
   ```
   2024-09-23T10:30:45.123Z | INFO | __main__ | Processing request with payload: {"prompt": "..."}
   2024-09-23T10:30:45.456Z | INFO | __main__ | Validated user message: Hello! Can you calculate 25 * 8 for me?
   2024-09-23T10:30:45.789Z | INFO | __main__ | Invoking agent with OpenAI model
   2024-09-23T10:30:46.123Z | INFO | __main__ | Agent processing completed successfully
   2024-09-23T10:30:46.234Z | INFO | __main__ | Returning response: {"result": {...}}
   ```

---

## Observability Setup

### Step 14: Configure Monitoring

1. **CloudWatch Dashboard**
   ```
   Navigate to: CloudWatch → Dashboards → Create dashboard

   Add Widgets:
   - Agent invocation count
   - Average response time
   - Error rate
   - Log insights queries
   ```

2. **Set Up Alerts**
   ```
   CloudWatch → Alarms → Create alarm

   Metrics to Monitor:
   - Error rate > 5%
   - Response time > 30 seconds
   - Failed invocations
   ```

3. **Log Insights Queries**
   ```
   Useful CloudWatch Insights queries:

   # Find errors
   fields @timestamp, @message
   | filter @message like /ERROR/
   | sort @timestamp desc

   # Response times
   fields @timestamp, @message
   | filter @message like /processing completed/
   | sort @timestamp desc
   ```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: "Unable to invoke endpoint successfully"
**Symptoms:**
- Agent sandbox shows error when testing
- CloudWatch logs show OpenTelemetry errors

**Solution:**
1. Check Dockerfile CMD line:
   ```dockerfile
   # WRONG (causes OpenTelemetry errors)
   CMD ["python", "-m", "opentelemetry.instrumentation.auto_instrumentation", "python", "src/agents/openai_agent.py"]

   # CORRECT (direct execution)
   CMD ["python", "src/agents/openai_agent.py"]
   ```

2. Rebuild and redeploy the Docker image:
   ```bash
   docker buildx build --platform linux/arm64 -f deployment/Dockerfile -t openai-strands-agent .
   docker tag openai-strands-agent:latest YOUR-ECR-URI
   docker push YOUR-ECR-URI
   ```

#### Issue 2: "Invalid security token" during ECR push
**Symptoms:**
- AWS CLI commands fail with authentication errors
- ECR login fails

**Solution:**
1. Verify AWS credentials:
   ```bash
   aws sts get-caller-identity
   ```

2. Update AWS credentials:
   ```bash
   aws configure
   # Re-enter your Access Key ID and Secret
   ```

3. Check IAM permissions:
   - Ensure `AmazonEC2ContainerRegistryFullAccess` is attached
   - Verify access keys are active in IAM console

#### Issue 3: "No module named 'openai'" in agent logs
**Symptoms:**
- Agent starts but fails on first request
- OpenAI import errors in CloudWatch logs

**Solution:**
1. Verify requirements.txt includes all dependencies:
   ```txt
   bedrock_agentcore
   strands-agents
   strands-tools
   openai
   ```

2. Rebuild Docker image with updated requirements

#### Issue 4: "Model access denied" errors
**Symptoms:**
- Agent responds but OpenAI API calls fail
- Rate limiting or permission errors

**Solution:**
1. Verify OpenAI API key in environment variables
2. Check OpenAI account billing and limits
3. Test API key locally:
   ```bash
   curl -H "Authorization: Bearer $OPENAI_API_KEY" \
        https://api.openai.com/v1/models
   ```

#### Issue 5: Agent Core not available in region
**Symptoms:**
- Cannot find Agent Core in AWS console
- Service not available errors

**Solution:**
1. Try different AWS regions:
   - us-east-1 (primary)
   - us-west-2
   - eu-west-1

2. Contact AWS support for Agent Core access
3. Use alternative deployment methods if Agent Core unavailable

### Performance Optimization

1. **Model Selection**
   ```
   Cost-effective options:
   - gpt-4o-mini: ~$0.15 per million tokens
   - gpt-3.5-turbo: ~$1 per million tokens

   Higher quality:
   - gpt-4o: ~$5 per million tokens
   ```

2. **Response Time Optimization**
   ```python
   # In settings.py
   OPENAI_MAX_TOKENS = 1000  # Reduce for faster responses
   OPENAI_TEMPERATURE = 0.3  # Lower for more consistent responses
   ```

3. **Memory Usage**
   ```
   Monitor container memory usage in CloudWatch
   Consider increasing container resources if needed
   ```

---

## Cost Management

### Expected Costs

1. **AWS Services**
   ```
   Agent Core: ~$0.10 per hour running time
   ECR: $0.10 per GB per month storage
   CloudWatch Logs: $0.50 per GB ingested
   ```

2. **OpenAI API**
   ```
   GPT-4o-mini: ~$0.15 per million input tokens
   Typical request: 100-500 tokens
   Cost per request: ~$0.00015
   ```

### Cost Optimization Tips

1. **Set Budget Alerts**
   ```
   AWS Budgets → Create budget
   Monthly limit: $20 (adjust as needed)
   Alerts at 80% and 100%
   ```

2. **Monitor Usage**
   ```
   CloudWatch → Billing → Estimated charges
   Review monthly AWS bill
   Monitor OpenAI usage dashboard
   ```

3. **Development Best Practices**
   ```
   - Stop agent runtime when not in use
   - Use smaller models during development
   - Implement request caching where appropriate
   - Set reasonable token limits
   ```

---

## Security Best Practices

### API Key Management

1. **Never commit secrets to Git**
   ```bash
   # Ensure .env is in .gitignore
   echo ".env" >> .gitignore
   ```

2. **Use AWS Secrets Manager** (Production)
   ```
   Store OpenAI API key in AWS Secrets Manager
   Reference in Agent Core environment variables
   ```

3. **Rotate keys regularly**
   ```
   OpenAI: Generate new API keys monthly
   AWS: Rotate access keys every 90 days
   ```

### Network Security

1. **VPC Configuration**
   ```
   Use private VPC for production deployments
   Configure security groups appropriately
   Enable VPC Flow Logs for monitoring
   ```

2. **Access Control**
   ```
   Implement least privilege IAM policies
   Use IAM roles instead of access keys where possible
   Enable CloudTrail for audit logging
   ```

---

## Next Steps

### Production Deployment

1. **Environment Separation**
   ```
   Create separate AWS accounts for:
   - Development
   - Staging
   - Production
   ```

2. **CI/CD Pipeline**
   ```
   Set up automated deployment using:
   - GitHub Actions
   - AWS CodePipeline
   - Docker registry webhooks
   ```

3. **Advanced Monitoring**
   ```
   Implement comprehensive monitoring:
   - X-Ray tracing
   - Custom CloudWatch metrics
   - Application performance monitoring
   ```

### Scaling Considerations

1. **Auto Scaling**
   ```
   Configure Agent Core auto-scaling based on:
   - Request volume
   - Response time thresholds
   - CPU/memory utilization
   ```

2. **Load Balancing**
   ```
   For high-traffic applications:
   - Multiple agent runtime instances
   - Application Load Balancer
   - Geographic distribution
   ```

---

## Support and Resources

### Documentation
- [AWS Bedrock Agent Core Documentation](https://docs.aws.amazon.com/bedrock/)
- [Strands Agents Documentation](https://strandsagents.com)
- [OpenAI API Documentation](https://platform.openai.com/docs)

### AWS Support
- [AWS Support Center](https://console.aws.amazon.com/support/)
- [AWS re:Post Community](https://repost.aws/)
- [AWS Service Health Dashboard](https://status.aws.amazon.com/)

### Project Support
- Create issues in the project repository
- Review existing documentation in the `docs/` folder
- Check CloudWatch logs for detailed error information

---

## Appendix

### Useful Commands Reference

```bash
# AWS CLI Verification
aws sts get-caller-identity
aws ecr describe-repositories --region us-east-1

# Docker Commands
docker buildx ls
docker images | grep openai-strands-agent
docker logs CONTAINER_ID

# Local Testing
python src/agents/openai_agent.py
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Test message"}'

# CloudWatch Logs
aws logs describe-log-groups --region us-east-1
aws logs tail /aws/bedrock-agentcore/runtimes/YOUR-RUNTIME-ID --follow
```

### Environment Variables Reference

```bash
# Required for Agent
OPENAI_API_KEY=sk-proj-your-key-here
OPENAI_MODEL=gpt-4o-mini
OPENAI_MAX_TOKENS=2000
OPENAI_TEMPERATURE=0.7
HOST=0.0.0.0
PORT=8080

# Optional for Development
ENABLE_TRACING=true
LOG_LEVEL=INFO
```

---

**🎉 Congratulations!** You now have a complete understanding of how to deploy OpenAI Strands Agents to AWS Bedrock Agent Core. This guide captures real-world deployment experience and should help you avoid common pitfalls while ensuring a successful deployment.

For additional help, refer to the troubleshooting section or check the CloudWatch logs for specific error details.