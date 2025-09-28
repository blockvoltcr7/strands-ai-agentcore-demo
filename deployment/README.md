# Deployment Scripts

This directory contains deployment scripts for the OpenAI Strands Agent.

## Scripts Overview

### 🏠 `deploy_local.py` - Local Development
Builds and runs the Docker container locally for testing.

```bash
# Build and run locally
python deployment/deploy_local.py

# Build only (don't run)
python deployment/deploy_local.py --build-only

# Run only (don't build)
python deployment/deploy_local.py --run-only

# Custom port
python deployment/deploy_local.py --port 3000

# Run in foreground
python deployment/deploy_local.py --foreground

# Check container status
python deployment/deploy_local.py --status
```

### ☁️ `deploy_ecr.py` - Production Deployment
Builds and pushes Docker image to AWS ECR with optimized minimal dependencies.

```bash
# Deploy to ECR (optimized build, ~3-4 minutes)
python deployment/deploy_ecr.py

# Custom region
python deployment/deploy_ecr.py --region us-west-2

# Custom repository name
python deployment/deploy_ecr.py --repository my-agent

# Custom tag
python deployment/deploy_ecr.py --tag v1.0.0
```

#### 🚀 Build Optimizations (Default)

- **Multi-stage build** for smaller final images
- **Minimal dependencies** (~20 packages vs 630+)
- **No OpenTelemetry bloat** (removed 50+ packages)
- **3x faster builds** (3-4 min vs 8-12 min)
- **Same functionality** with basic logging

### 🛠️ `deploy_utils.py` - Shared Utilities
Common functions used by both deployment scripts.

## Prerequisites

### For Local Deployment
- Docker Desktop running
- Python 3.12+

### For ECR Deployment
- Docker Desktop running
- AWS CLI configured (`aws configure`)
- ECR permissions (AmazonEC2ContainerRegistryFullAccess)

## Workflow

1. **Local Testing**: `python deployment/deploy_local.py`
2. **Test your agent**: Visit `http://localhost:8080`
3. **Check health**: Visit `http://localhost:8080/ping`
4. **View logs**: `docker logs openai-strands-agent-local`

### Production Deployment
 1. **Deploy to ECR**: `python deployment/deploy_ecr.py`
 2. **Go to AWS Bedrock Agent Core Console**
 3. **Create/Update Agent Runtime** with the provided Container URI
 4. **Add environment variables**:
   - `OPENAI_API_KEY`: your-api-key
   - `OPENAI_MODEL`: gpt-4o-mini

## Invoke the Agent (AWS AgentCore)

Use `deployment/invoke_agent.py` to send a prompt to your deployed AgentCore runtime.

```bash
# From project root
python3 deployment/invoke_agent.py \
  --agent-arn arn:aws:bedrock-agentcore:us-east-1:343075903183:runtime/Morpheus-KcMY9vEB51 \
  --prompt "hello" \
  --session-id "my-session-id"
  --qualifier "DEFAULT"
```

Notes:
- Ensure your AWS credentials are configured and have permission to call `bedrock-agentcore:InvokeAgentRuntime`.
- Required: `--agent-arn` is your Agent Runtime ARN (copy from the Bedrock AgentCore console).
- Optional: `--region` (defaults to `us-east-1`).
- Optional: `--session-id` (33+ chars). If omitted or too short, the script auto-generates/pads a valid ID.

## Troubleshooting

### Docker Issues
- Ensure Docker Desktop is running
- Check available disk space

### AWS Issues
- Verify AWS credentials: `aws sts get-caller-identity`
- Check ECR permissions
- Ensure region is correct

### Build Issues
- Verify `pyproject.toml` exists in project root
- Check `deployment/Dockerfile` syntax
- Ensure `.env.example` exists

## File Structure

```
deployment/
├── deploy_local.py     # Local deployment
├── deploy_ecr.py       # ECR deployment
├── deploy_utils.py     # Shared utilities
├── Dockerfile          # Optimized Docker image
├── requirements.txt    # Minimal dependencies
├── invoke_agent.py     # Agent invocation script
└── README.md          # This file
