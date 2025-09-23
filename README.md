# OpenAI Strands Agent for AWS Bedrock AgentCore

Production-ready OpenAI Strands Agent optimized for deployment to AWS Bedrock AgentCore. This project focuses exclusively on the working OpenAI integration path, providing a clean, maintainable solution for AI agent deployment.

## 🚀 Quick Start

```bash
# 1. Configure OpenAI API key
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 2. Install dependencies
uv sync

# 3. Test locally (from project root)
python src/agents/openai_agent.py

# 4. In another terminal, test the agent
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Calculate 15 * 7 and show your work"}'

# 5. Deploy to AgentCore
python deployment/deploy_to_agentcore.py --role-arn arn:aws:iam::ACCOUNT:role/AgentRuntimeRole
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
│   ├── Dockerfile                       # 🐳 AgentCore deployment
│   ├── requirements.txt                 # 📦 Production dependencies
│   ├── deploy_to_agentcore.py          # 🚀 Automated deployment
│   └── invoke_agent.py                  # 🧪 Production testing
├── tests/
│   └── test_agent_basic.py             # 🧪 Basic health checks
├── .env.example                         # 📝 Environment template
├── pyproject.toml                       # 📋 Project configuration
├── Dockerfile.local                     # 🐳 Local Docker testing
├── docker-local-test.sh                # 🧪 Automated Docker testing
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
   - Follow the [AWS Setup Guide](AWS_SETUP_GUIDE.md) for detailed instructions

## Testing the Agents

### 1. OpenAI Agent Testing

#### Production Agent
```bash
# 1. Start the OpenAI agent (from project root)
python src/agents/openai_agent.py

# 2. In another terminal, test it
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Calculate 15 * 7 and show your work"}'

# 3. Run comprehensive pytest tests
pytest tests/test_agent_basic.py -v

# Or run directly
python tests/test_agent_basic.py
```

Expected response:
```json
{
  "result": {
    "content": [{"text": "15 * 7 = 105\n\nUsing the calculator: 15 × 7 = 105"}],
    "role": "assistant"
  }
}
```

### 2. Comprehensive Testing

```bash
# Run pytest test suite (9 comprehensive tests)
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

## API Usage

The agent runs on `http://localhost:8080/invocations` and accepts:

```json
{
  "prompt": "Your message here"
}
```

Health check endpoint: `http://localhost:8080/ping`

## Troubleshooting

### OpenAI Issues

1. **Invalid API Key**:
   ```
   Error: The api_key client option must be set
   ```
   - Check your `OPENAI_API_KEY` in `.env`
   - Verify the key is valid at OpenAI Platform

2. **Rate Limiting**:
   ```
   Error: Rate limit exceeded
   ```
   - OpenAI has usage limits based on your plan
   - Consider upgrading or reducing request frequency

3. **Model Access**:
   ```
   Error: The model gpt-4o does not exist
   ```
   - Some models require higher tier access
   - Try `gpt-4o-mini` or `gpt-3.5-turbo`

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

## Cost Considerations

### OpenAI Pricing (Approximate)
- **GPT-4o-mini**: ~$0.15 per million input tokens
- **GPT-4o**: ~$5 per million input tokens
- **GPT-3.5-turbo**: ~$1 per million input tokens

### AWS Bedrock Pricing
- **Claude 3 Haiku**: ~$0.25 per million input tokens
- **Claude 3 Sonnet**: ~$3 per million input tokens

## Next Steps

1. **Deploy to AWS**: Follow the Strands documentation for AgentCore deployment
2. **Add Custom Tools**: Extend agents with your own tools and functions
3. **Multi-Agent Systems**: Explore Strands' multi-agent patterns
4. **Production Setup**: Add monitoring, logging, and error handling

## 🚀 Deployment to AWS AgentCore

### Prerequisites
- AWS CLI configured with appropriate permissions
- IAM role for AgentCore with proper permissions
- Docker installed and running

### Automated Deployment

```bash
# Deploy to AgentCore
python deployment/deploy_to_agentcore.py \
  --role-arn arn:aws:iam::YOUR-ACCOUNT-ID:role/AgentRuntimeRole \
  --region us-east-1
```

### Manual Deployment Steps

```bash
# 1. Create ECR repository
aws ecr create-repository --repository-name openai-strands-agent

# 2. Build and push ARM64 image
docker buildx build --platform linux/arm64 \
  -f deployment/Dockerfile \
  -t YOUR-ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/openai-strands-agent:latest \
  --push .

# 3. Deploy to AgentCore
aws bedrock-agentcore-control create-agent-runtime \
  --agent-runtime-name openai-strands-agent \
  --agent-runtime-artifact containerConfiguration='{containerUri=YOUR-ECR-URI}' \
  --network-configuration networkMode=PUBLIC \
  --role-arn YOUR-AGENTCORE-ROLE-ARN
```

### Testing Deployed Agent

```bash
# Test the deployed agent
python deployment/invoke_agent.py \
  --agent-arn arn:aws:bedrock-agentcore:us-east-1:ACCOUNT:runtime/AGENT-ID \
  --prompt "Hello! Test the deployed agent."
```

## 🧪 Testing & Validation

### Local Testing

#### Option 1: Direct Python Testing
```bash
# 1. Start agent locally
python src/agents/openai_agent.py

# 2. Run comprehensive tests (in another terminal)
python tests/test_openai_agent_updated.py

# 3. Run integration tests
python tests/integration_tests.py

# 4. Quick test with curl
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello! Test the agent."}'
```

#### Option 2: Docker Local Testing (Recommended for AgentCore simulation)
```bash
# 1. Ensure Docker Desktop is running
open -a Docker  # On macOS

# 2. Configure your OpenAI API key
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 3. Run automated Docker test
./docker-local-test.sh

# Or manually:
# Build ARM64 image
docker buildx create --use --name agentcore-builder
docker buildx build --platform linux/arm64 -f Dockerfile.local -t openai-strands-agent:local --load .

# Run container
docker run --platform linux/arm64 -p 8080:8080 --env-file .env openai-strands-agent:local
```

### Production Validation
```bash
# Test deployed agent performance
python deployment/invoke_agent.py \
  --agent-arn YOUR-AGENT-ARN \
  --prompt "Calculate 15 * 7 and show your work"
```

## 🛠️ Advanced Configuration

### Custom Models
Edit `src/config/settings.py` to use different OpenAI models:
```python
OPENAI_MODEL = "gpt-4o"  # or gpt-3.5-turbo, gpt-4, etc.
```

### Observability
Enable tracing in `.env`:
```bash
ENABLE_TRACING=true
```

### Performance Tuning
Adjust model parameters in settings:
```python
OPENAI_MAX_TOKENS = 2000
OPENAI_TEMPERATURE = 0.3
```

## 📊 Monitoring & Observability

AgentCore provides built-in observability through CloudWatch:

1. **Enable Transaction Search** in CloudWatch console
2. **View metrics** in GenAI Observability dashboard
3. **Monitor traces** with X-Ray integration

## 🔧 Troubleshooting

### Common Issues

1. **File Not Found Errors**
   ```bash
   # Always run commands from the project root directory
   pwd  # Should show: .../strands-ai-agentcore-demo
   python src/agents/openai_agent.py  # Correct path
   ```

2. **OpenAI API Key Issues**
   ```bash
   # Check if key is valid
   curl -H "Authorization: Bearer $OPENAI_API_KEY" \
        https://api.openai.com/v1/models
   ```

3. **Module Import Errors**
   ```bash
   # Ensure dependencies are installed
   uv sync
   # Or with pip
   pip install -r requirements.txt
   ```

4. **Docker Build Issues**
   ```bash
   # Ensure buildx is set up for ARM64
   docker buildx create --use
   ```

5. **AgentCore Deployment Issues**
   ```bash
   # Check IAM permissions
   aws sts get-caller-identity
   aws iam get-role --role-name AgentRuntimeRole
   ```

### Performance Optimization

- **Use GPT-4o-mini** for cost efficiency
- **Adjust max_tokens** based on use case
- **Implement caching** for repeated requests
- **Monitor response times** with integration tests

## 📚 References

- [Strands Agents Documentation](https://strandsagents.com)
- [OpenAI Platform](https://platform.openai.com)
- [AWS Bedrock AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/)
- [AgentCore Deployment Guide](https://strandsagents.com/latest/documentation/docs/user-guide/deploy/deploy_to_bedrock_agentcore/)