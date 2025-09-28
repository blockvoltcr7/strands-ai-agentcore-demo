# OpenAI Strands Agent for AWS Bedrock AgentCore

Production-ready OpenAI Strands Agent optimized for deployment to AWS Bedrock AgentCore. This project focuses exclusively on the working OpenAI integration path, providing a clean, maintainable solution for AI agent deployment.


## 🚀 Quick Start

```bash
# 1. Configure OpenAI API key
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 2. Install dependencies
uv sync

# 3a. Run locally (no Docker, recommended for fast dev)
python src/agents/openai_agent.py

# 3b. Or run via Docker (from project root)
python deployment/deploy_local.py

# 4. Test locally in another terminal (works for either method)
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "hello"}'

# 5. Deploy image to ECR for AgentCore (when ready)
python deployment/deploy_ecr.py

# 6. (After creating/updating your AgentCore runtime in AWS Console)
#    Invoke your deployed agent (replace with your Agent Runtime ARN)
python deployment/invoke_agent.py \
  --agent-arn arn:aws:bedrock-agentcore:us-east-1:ACCOUNT_ID:runtime/YOUR_AGENT_ID \
  --prompt "Hello from README"
```

## Prerequisites

- Python 3.12+
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- AWS Account with AgentCore access
- Docker (for deployment)
- uv package manager (recommended) or pip

## Installation

```bash
# Install all dependencies (already configured in pyproject.toml)
uv sync

# Alternative with pip (if not using uv)
pip install -r requirements.txt
```

## 📁 Project Structure

```
/
├── src/
│   ├── agents/
│   │   └── openai_agent.py              # 🤖 Production OpenAI agent
│   ├── config/
│   │   └── settings.py                  # ⚙️ Configuration management
│   └── utils/
│       └── helpers.py                   # 🛠️ Common utilities
├── deployment/
│   ├── Dockerfile                       # 🐳 AgentCore deployment image
│   ├── requirements.txt                 # 📦 Minimal production deps
│   ├── deploy_local.py                  # ▶️ Local Docker run
│   ├── deploy_ecr.py                    # ☁️ Build & push to ECR
│   ├── invoke_agent.py                  # 🧪 Invoke deployed AgentCore runtime
│   └── README.md                        # 📖 Deployment docs
├── tests/
│   └── test_agent_basic.py             # 🧪 Basic health checks
├── .env.example                         # 📝 Environment template
├── pyproject.toml                       # 📋 Project configuration
├── requirements.txt                     # 📦 Dev deps (alt to uv)
└── README.md                           # 📖 This file
```

## Configuration

### Environment Variables

Create a `.env` file with your credentials:

```bash
# AWS Credentials (for Bedrock agents)
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_DEFAULT_REGION=us-east-1

# OpenAI Configuration (for OpenAI agents)
OPENAI_API_KEY=your_openai_api_key
```

### Getting API Keys

1. **OpenAI API Key**:
   - Go to [OpenAI Platform](https://platform.openai.com/api-keys)
   - Create a new API key
   - Add it to your `.env` file

2. **AWS Credentials**:
   - Follow the [AWS IAM Setup Guide](./docs/AWS_IAM_SETUP_GUIDE.md) for detailed instructions on creating IAM users and configuring AWS CLI

## Testing the Agent Locally

### 1. OpenAI Agent Testing

#### Development Agent (No Docker)
```bash
# 1. Start the agent locally (no Docker)
python src/agents/openai_agent.py

# 2. In another terminal, test it
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "hello"}'

# 3. Run comprehensive pytest tests
pytest tests/test_agent_basic.py -v

# Or run directly
python tests/test_agent_basic.py
```

#### Production-like (Docker)
```bash
# 1. Start the agent in Docker (from project root)
python deployment/deploy_local.py

# 2. In another terminal, test it
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "hello"}'

# 3. Run comprehensive pytest tests
pytest tests/test_agent_basic.py -v

# Or run directly
python tests/test_agent_basic.py
```

Expected response:
```json
{
  "result": {
    "content": [{"text": "Wake up neo"}],
    "role": "assistant"
  }
}
```

### 2. Comprehensive Testing

```bash
# Run pytest test suite
pytest tests/test_agent_basic.py -v

# Quick run with direct execution
python tests/test_agent_basic.py

# Run all tests in tests directory
pytest tests/ -v
```

## Features

### OpenAI Agent Features
- **Calculator Tool**: Performs mathematical calculations
- **Production Ready**: Single, focused agent for AgentCore deployment
- **Cost Efficient**: Uses GPT-4o-mini by default for lower costs
- **Health Monitoring**: Built-in /ping endpoint for monitoring
- **Error Handling**: Robust error handling and validation

## API Usage (Local)

The agent runs on `http://localhost:8080/invocations` and accepts:

```json
{
  "prompt": "hello"
}
```

Health check endpoint: `http://localhost:8080/ping`


### General Issues

1. **Port in Use**:
   ```bash
   lsof -i :8080 | grep LISTEN | awk '{print $2}' | xargs kill -9
   ```

2. **Environment Variables**:
   ```bash
   source load_env.sh
   echo $OPENAI_API_KEY  # Should show your key
   ```

## Next Steps

1. **Deploy to AWS**: Follow the Strands documentation for AgentCore deployment
2. **Add Custom Tools**: Extend agents with your own tools and functions
3. **Multi-Agent Systems**: Explore Strands' multi-agent patterns
4. **Production Setup**: Add monitoring, logging, and error handling

## 🚀 Deployment to AWS AgentCore

**📖 For complete step-by-step deployment instructions, see: [AGENT_CORE_DEPLOYMENT_GUIDE.md](./docs/AGENT_CORE_DEPLOYMENT_GUIDE.md)**

The comprehensive deployment guide covers:
- ✅ Complete IAM setup with correct permissions
- ✅ ECR repository creation and Docker image management
- ✅ Manual AWS console deployment (recommended)
- ✅ Environment configuration and troubleshooting
- ✅ Real-world deployment experience and solutions

### Quick Deployment Overview

For experienced users, here's the condensed version:

### Prerequisites
- AWS CLI configured with appropriate permissions
- IAM role for AgentCore with proper permissions
- Docker installed and running
- **See [AGENT_CORE_DEPLOYMENT_GUIDE.md](./docs/AGENT_CORE_DEPLOYMENT_GUIDE.md) for detailed setup**

### Deployment Flow Summary

1. Build and push image to ECR:
   ```bash
   python deployment/deploy_ecr.py
   ```
2. In AWS Console, create/update an AgentCore Runtime using the pushed image.
3. Set environment variables in the runtime:
   - `OPENAI_API_KEY`: your-api-key
   - `OPENAI_MODEL`: gpt-4o-mini (default)
4. Test the deployed runtime from your machine:
   ```bash
   python deployment/invoke_agent.py \
     --agent-arn arn:aws:bedrock-agentcore:us-east-1:ACCOUNT_ID:runtime/YOUR_AGENT_ID \
     --prompt "Hello"
   ```

### Testing Deployed Agent

```bash
# Test the deployed agent
python deployment/invoke_agent.py \
  --agent-arn arn:aws:bedrock-agentcore:us-east-1:ACCOUNT:runtime/AGENT-ID \
  --prompt "Hello"
```

## 🧪 Testing & Validation

### Local Testing

```bash
# Option A: Run locally without Docker (fast dev loop)
python src/agents/openai_agent.py

# In another terminal, hit the local endpoint
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello"}'

# Option B: Run via Dock# Ensure Docker Desktop is running

# Start the container locally
python deployment/deploy_local.py

# In another terminal, hit the local endpoint
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello"}'
```

### Production Validation
```bash
# Test deployed agent (replace with your ARN)
python deployment/invoke_agent.py \
  --agent-arn arn:aws:bedrock-agentcore:us-east-1:XXXXXXXXX:runtime/YOUR_AGENT_ID \
  --prompt "hello" \
  --session-id "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" \
  --qualifier "DEFAULT"
```

## 📚 References

- [Strands Agents Documentation](https://strandsagents.com)
- [OpenAI Platform](https://platform.openai.com)
- [AWS Bedrock AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/)
- [AgentCore Deployment Guide](https://strandsagents.com/latest/documentation/docs/user-guide/deploy/deploy_to_bedrock_agentcore/)