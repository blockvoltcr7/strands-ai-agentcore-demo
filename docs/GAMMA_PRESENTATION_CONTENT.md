# AWS AgentCore Deployment Presentation Content for Gamma.app

## Instructions for Using This Content

1. **Open Gamma.app** and select "Presentation" type
2. **Copy everything below the line** into the text input area
3. **Select "Generate from notes or an outline"** option
4. Gamma will automatically create your presentation with proper formatting

---

# Deploy OpenAI Agents to AWS AgentCore
## From Local Development to Production

Learn to deploy production-ready OpenAI agents using Strands AI framework to AWS Bedrock AgentCore

### What You'll Learn
- Set up local development environment
- Deploy agents locally without Docker
- Containerize with Docker for cloud deployment
- Push to AWS ECR (Elastic Container Registry)
- Deploy to AWS AgentCore and test in production

---

# Prerequisites & Initial Setup
## What You Need Before Starting

### Required Software & Accounts
- Python 3.12+ installed
- Docker Desktop running
- AWS Account with AgentCore access
- OpenAI API account and key
- AWS CLI configured

### Project Architecture
- **Strands AI Framework**: Agent orchestration
- **OpenAI GPT-4o-mini**: Cost-effective LLM
- **AWS ECR**: Container registry
- **AWS AgentCore**: Serverless agent runtime
- **Calculator Tool**: Built-in mathematical capabilities

---

# Local Development Setup
## Getting Started Without Docker

### Step 1: Environment Configuration
```bash
# Clone and setup project
git clone your-project-repo
cd strands-ai-agentcore-demo

# Create environment file
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=your_key_here
```

### Step 2: Install Dependencies
```bash
# Install with uv (recommended)
uv sync

# Alternative with pip
pip install -r requirements.txt
```

### Step 3: Run Agent Locally
```bash
# Start the agent server
python src/agents/openai_agent.py

# Test in another terminal
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Calculate 15 * 7 and show work"}'
```

---

# Testing & Validation
## Ensure Everything Works

### Comprehensive Testing
```bash
# Run pytest test suite
pytest tests/test_agent_basic.py -v

# Direct test execution
python tests/test_agent_basic.py

# Health check endpoint
curl http://localhost:8080/ping
```

### Expected Response Format
```json
{
  "result": {
    "content": [{"text": "15 * 7 = 105\n\nUsing calculator: 15 × 7 = 105"}],
    "role": "assistant"
  }
}
```

### Key Features Tested
- Calculator tool functionality
- Error handling and validation
- Response formatting
- Health monitoring endpoint

---

# Docker Containerization
## Preparing for Cloud Deployment

### Local Docker Testing
```bash
# Ensure Docker is running
open -a Docker  # macOS

# Run automated test script
./docker-local-test.sh

# Or manual approach:
docker buildx create --use --name agentcore-builder
docker buildx build --platform linux/arm64 \
  -f Dockerfile.local -t openai-agent:local --load .

# Run container locally
docker run --platform linux/arm64 \
  -p 8080:8080 --env-file .env openai-agent:local
```

### Why ARM64 Platform?
- AWS AgentCore runs on ARM64 architecture
- Graviton processors for cost efficiency
- Better performance for AI workloads
- Required for AgentCore compatibility

---

# AWS ECR Setup
## Container Registry Configuration

### Step 1: Create ECR Repository
```bash
# Create repository
aws ecr create-repository --repository-name openai-strands-agent

# Get login token
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  YOUR-ACCOUNT.dkr.ecr.us-east-1.amazonaws.com
```

### Step 2: Build & Push Production Image
```bash
# Build ARM64 production image
docker buildx build --platform linux/arm64 \
  -f deployment/Dockerfile \
  -t YOUR-ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/openai-strands-agent:latest \
  --push .
```

### ECR Best Practices
- Use semantic versioning for tags
- Enable image scanning for security
- Set lifecycle policies for cost management
- Monitor image sizes and optimize layers

---

# AgentCore Deployment
## Production Deployment to AWS

### Prerequisites Setup
- IAM role: `AgentRuntimeRole` with proper permissions
- Environment variables configured in AgentCore
- ECR image successfully pushed
- AgentCore service availability in your region

### Deployment Options

#### Option 1: Automated Deployment
```bash
python deployment/deploy_to_agentcore.py \
  --role-arn arn:aws:iam::ACCOUNT:role/AgentRuntimeRole \
  --region us-east-1
```

#### Option 2: Manual Console Deployment (Recommended)
1. Navigate to AWS AgentCore Console
2. Create new agent with ECR image URI
3. Configure environment variables
4. Set IAM role and permissions
5. Deploy and test

---

# Testing Production Deployment
## Validation & Monitoring

### Agent Invocation Testing
```bash
# Test deployed agent
python deployment/invoke_agent.py \
  --agent-arn arn:aws:bedrock-agentcore:us-east-1:ACCOUNT:runtime/AGENT-ID \
  --prompt "Test production deployment with calculation: 25 * 8"
```

### Monitoring & Observability
- **CloudWatch Logs**: Real-time agent logs
- **X-Ray Tracing**: Request flow visualization
- **GenAI Dashboard**: Performance metrics
- **Transaction Search**: Debug specific requests

### Performance Optimization
- Monitor response times and token usage
- Adjust model parameters for cost vs quality
- Implement caching for repeated requests
- Use GPT-4o-mini for cost efficiency

---

# Troubleshooting & Best Practices
## Common Issues & Solutions

### Deployment Issues
```bash
# Check IAM permissions
aws sts get-caller-identity
aws iam get-role --role-name AgentRuntimeRole

# Verify ECR access
aws ecr describe-repositories

# Test OpenAI API key
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
     https://api.openai.com/v1/models
```

### Cost Optimization
- **GPT-4o-mini**: ~$0.15 per million tokens
- **GPT-4o**: ~$5 per million tokens
- **AgentCore**: Pay per invocation
- **ECR**: Storage and data transfer costs

### Security Best Practices
- Store API keys in environment variables only
- Use IAM roles with minimal permissions
- Enable CloudTrail for audit logging
- Implement request rate limiting

### Next Steps
- Add custom tools and capabilities
- Explore multi-agent orchestration
- Implement advanced monitoring
- Scale to production workloads

---

## Additional Notes for Gamma.app

### Presentation Settings
- **Style**: Professional/Technical
- **Format**: Step-by-step tutorial
- **Audience**: Students and developers learning AWS deployment
- **Duration**: 30-45 minutes for full presentation

### Tips for Enhancement in Gamma
1. Use the AI chat to add visual diagrams for architecture
2. Apply "Traditional" page style if exporting to PowerPoint
3. Enable analytics to track engagement during live presentations
4. Consider adding speaker notes for each slide
5. Use one-click redesign to match your organization's branding

### Recording Your YouTube Video
When recording your tutorial video:
1. Use this presentation as your visual guide
2. Live demo each step while explaining
3. Show actual terminal output and AWS console
4. Highlight common errors and solutions
5. Keep segments under 10 minutes for better retention