# Complete AWS Setup Guide for Bedrock AgentCore

## Prerequisites
- A new AWS account with root access
- A web browser
- Terminal/Command line access

---

## Step 1: Secure Your Root Account (5 minutes)

### 1.1 Enable MFA on Root Account
1. Sign in to AWS Console as root user: https://console.aws.amazon.com/
2. Click your account name (top right) → **Security credentials**
3. In **Multi-factor authentication (MFA)** section → Click **Assign MFA device**
4. Follow the wizard to set up MFA (use Google Authenticator or similar)

### 1.2 Set Billing Alerts
1. Go to **Billing Dashboard** → **Billing preferences**
2. Enable **Receive Billing Alerts**
3. Save preferences

---

## Step 2: Create IAM User for Development (10 minutes)

> **Important:** Never use root account for daily operations!

### 2.1 Create IAM User
1. Navigate to **IAM Console**: https://console.aws.amazon.com/iam/
2. Click **Users** in left sidebar → **Create user**
3. User details:
   - User name: `bedrock-developer` (or your preferred name)
   - Check ✅ **Provide user access to the AWS Management Console**
   - Console access: **I want to create an IAM user**
   - Console password: Set a custom password
   - Uncheck "Users must create a new password at next sign-in"
4. Click **Next**

### 2.2 Set Permissions
1. Select **Attach policies directly**
2. Search and select these policies:
   - `AmazonBedrockFullAccess` (if available)
   - If not available, we'll create a custom policy (see Step 2.3)
3. Click **Next** → **Create user**
4. **IMPORTANT**: Download the .csv file with credentials

### 2.3 Create Custom Bedrock Policy (if needed)
If `AmazonBedrockFullAccess` doesn't exist:

1. Go to **IAM** → **Policies** → **Create policy**
2. Click **JSON** tab and paste:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "BedrockFullAccess",
            "Effect": "Allow",
            "Action": [
                "bedrock:*"
            ],
            "Resource": "*"
        },
        {
            "Sid": "BedrockModelInvocation",
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": "arn:aws:bedrock:*::foundation-model/*"
        }
    ]
}
```

3. Click **Next**
4. Policy name: `BedrockDeveloperPolicy`
5. Click **Create policy**
6. Go back to your IAM user → **Add permissions** → **Attach policies**
7. Search and attach `BedrockDeveloperPolicy`

### 2.4 Create Access Keys
1. Go to **IAM** → **Users** → Click your `bedrock-developer` user
2. Click **Security credentials** tab
3. In **Access keys** section → **Create access key**
4. Select **Command Line Interface (CLI)**
5. Check the confirmation box → **Next**
6. Description tag: `bedrock-agentcore-dev`
7. Click **Create access key**
8. **CRITICAL**: Save both:
   - Access key ID (looks like: AKIAIOSFODNN7EXAMPLE)
   - Secret access key (looks like: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY)
9. Download .csv file as backup

---

## Step 3: Enable Amazon Bedrock (5 minutes)

### 3.1 Navigate to Bedrock
1. In AWS Console, search for **"Bedrock"** in the top search bar
2. Click **Amazon Bedrock**
3. If you see a "Get started" page, click **Get started**

### 3.2 Request Model Access
1. In Bedrock console, click **Model access** (left sidebar)
2. Click **Manage model access** or **Enable specific models**
3. **IMPORTANT**: Request access to these models:
   - ✅ **Anthropic - Claude 3 Sonnet**
   - ✅ **Anthropic - Claude 3 Haiku**
   - ✅ **Anthropic - Claude 3.5 Sonnet** (if available)
   - ✅ **Anthropic - Claude 3 Opus** (if available)
4. Check the boxes next to these models
5. Click **Request model access** or **Save changes**
6. Most Anthropic models are **instantly approved**
7. Status should change to **"Access granted"** within seconds

### 3.3 Verify Model Access
1. Still in Bedrock console → **Model access**
2. Ensure status shows **"Access granted"** for Claude models
3. If status is "Available to request", click on it and request access

---

## Step 4: Configure Local Development Environment (5 minutes)

### 4.1 Test Current Configuration
First, let's see what's currently configured:

```bash
cd ~/dev/personal/aws-agentcore/strands-ai-agentcore-demo
python tests/test_aws_bedrock.py
```

### 4.2 Configure AWS Credentials

**Option A: Using Environment Variables (Recommended for testing)**

```bash
# Add these to your terminal session
export AWS_ACCESS_KEY_ID='your-access-key-from-step-2.4'
export AWS_SECRET_ACCESS_KEY='your-secret-key-from-step-2.4'
export AWS_DEFAULT_REGION='us-east-1'

# Verify it works
aws sts get-caller-identity
```

**Option B: Using AWS CLI Configuration (Permanent)**

```bash
aws configure
# Enter when prompted:
# AWS Access Key ID: your-access-key-from-step-2.4
# AWS Secret Access Key: your-secret-key-from-step-2.4
# Default region name: us-east-1
# Default output format: json

# Verify it works
aws sts get-caller-identity
```

**Option C: Using the Setup Script**

```bash
source env_setup.sh
# Follow the prompts
```

### 4.3 Verify Everything Works

```bash
# Test AWS credentials
python tests/test_aws_bedrock.py

# You should see:
# ✓ AWS Region: us-east-1
# ✓ Bedrock client created successfully
# ✓ Can access Bedrock - found X models
```

---

## Step 5: Test Your Agent (2 minutes)

### 5.1 Test Basic Connectivity
```bash
# Test without Bedrock (should always work)
python src/agents/simple_agent.py

# In another terminal
python tests/test_agent.py
```

### 5.2 Test with Bedrock
```bash
# Kill any running servers
lsof -i :8080 | grep LISTEN | awk '{print $2}' | xargs kill -9 2>/dev/null || true

# Start the streaming agent
python src/agents/agent_streaming.py

# In another terminal
python tests/test_agent.py
```

---

## Step 6: Troubleshooting Checklist

### If you get "Invalid Security Token"
- [ ] Verify access keys are correct (no extra spaces)
- [ ] Check keys haven't been deactivated in IAM
- [ ] Ensure you're using the right AWS account
- [ ] Try regenerating access keys

### If you get "Access Denied"
- [ ] Verify IAM user has BedrockFullAccess or custom policy
- [ ] Check Bedrock model access is granted
- [ ] Ensure you're in the right region (us-east-1)

### If Bedrock models aren't available
- [ ] Go to Bedrock console → Model access
- [ ] Request access to Claude models
- [ ] Wait for approval (usually instant for Claude)
- [ ] Try a different region if models aren't available

### Quick Debug Commands
```bash
# Check AWS identity
aws sts get-caller-identity

# List available Bedrock models
aws bedrock list-foundation-models --region us-east-1

# Test Bedrock access
aws bedrock-runtime invoke-model \
  --model-id anthropic.claude-3-haiku-20240307-v1:0 \
  --body '{"anthropic_version":"bedrock-2023-05-31","messages":[{"role":"user","content":"Hello"}],"max_tokens":100}' \
  --region us-east-1 \
  output.json
```

---

## Step 7: Cost Management Tips

### Set up Budget Alerts
1. Go to **AWS Budgets** in console
2. Create budget → **Cost budget**
3. Set monthly budget (e.g., $10)
4. Set alerts at 80% and 100%

### Bedrock Pricing Notes
- Claude 3 Haiku: ~$0.25 per million input tokens
- Claude 3 Sonnet: ~$3 per million input tokens
- Claude 3.5 Sonnet: ~$3 per million input tokens
- You're charged per token processed

### Free Tier
- New AWS accounts get some free tier benefits
- Bedrock itself doesn't have free tier
- Each API call costs money (though very small amounts for testing)

---

## Next Steps

Once everything is working:

1. **Test your agent locally**:
   ```bash
   python src/agents/agent.py
   # In another terminal
   curl -X POST http://localhost:8080/invocations \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Hello, how are you?"}'
   ```

2. **Deploy to Bedrock AgentCore** following Step 3 in the [Strands documentation](https://strandsagents.com/latest/documentation/docs/user-guide/deploy/deploy_to_bedrock_agentcore/)

3. **Monitor costs** in AWS Billing Dashboard

---

## Security Best Practices

1. **Never commit credentials to git**
   - Add `.env` to `.gitignore`
   - Use environment variables or AWS profiles

2. **Rotate access keys regularly**
   - Every 90 days minimum
   - Immediately if compromised

3. **Use least privilege principle**
   - Only grant permissions needed
   - Use separate IAM users for different projects

4. **Enable CloudTrail** for audit logging (optional but recommended for production)

---

## Quick Reference

### Your Setup Commands
```bash
# Set credentials (every new terminal session)
export AWS_ACCESS_KEY_ID='your-key'
export AWS_SECRET_ACCESS_KEY='your-secret'
export AWS_DEFAULT_REGION='us-east-1'

# Test AWS access
aws sts get-caller-identity

# Test Bedrock access
python tests/test_aws_bedrock.py

# Run agent
python src/agents/agent.py

# Test with the Python script
python tests/test_agent.py
```

### Useful AWS Console Links
- [IAM Console](https://console.aws.amazon.com/iam/)
- [Bedrock Console](https://console.aws.amazon.com/bedrock/)
- [Billing Dashboard](https://console.aws.amazon.com/billing/)
- [CloudWatch Logs](https://console.aws.amazon.com/cloudwatch/)

---

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all checkboxes in the setup steps
3. Check AWS service health: https://status.aws.amazon.com/
4. Review IAM permissions and Bedrock model access

Remember: Keep your AWS credentials secure and never share them!