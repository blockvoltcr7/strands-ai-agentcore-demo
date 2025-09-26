# Docker Local Testing Guide

This guide provides step-by-step instructions for testing your OpenAI Strands Agent locally using Docker, simulating the exact ARM64 environment used by AWS Bedrock AgentCore.

## 🐳 Prerequisites

- **Docker Desktop** installed and running
- **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))
- **Project dependencies** installed (`uv sync` or `pip install -r requirements.txt`)

## 🚀 Quick Start

### 1. Start Docker Desktop

```bash
# On macOS
open -a Docker

# On Linux
sudo systemctl start docker

# On Windows
# Start Docker Desktop from the Start menu
```

Wait for Docker to fully start (you'll see the Docker icon in your system tray).

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env file and add your OpenAI API key
# OPENAI_API_KEY=sk-your-actual-api-key-here
```

### 3. Run Automated Test

```bash
# Make script executable (if needed)
chmod +x docker-local-test.sh

# Run the automated Docker test
./docker-local-test.sh
```

## 📋 What the Automated Test Does

The `docker-local-test.sh` script performs the following steps:

1. ✅ **Checks Docker Status** - Verifies Docker is running
2. ✅ **Creates ARM64 Builder** - Sets up buildx for ARM64 architecture
3. ✅ **Builds Container** - Creates the ARM64 Docker image
4. ✅ **Starts Container** - Runs the agent on port 8080
5. ✅ **Tests Endpoints** - Validates `/ping` and `/invocations`
6. ✅ **Shows Results** - Displays OpenAI agent responses

## 🔧 Manual Docker Commands

If you prefer to run commands manually:

### Build the Image

```bash
# Create ARM64 builder (one-time setup)
docker buildx create --use --name agentcore-builder

# Build the ARM64 image
docker buildx build --platform linux/arm64 \
    -f Dockerfile.local \
    -t openai-strands-agent:local \
    --load .
```

### Run the Container

```bash
# Start the container
docker run --platform linux/arm64 \
    -p 8080:8080 \
    --env-file .env \
    --name openai-strands-test \
    --rm \
    openai-strands-agent:local
```

### Test the Endpoints

```bash
# Test health check
curl http://localhost:8080/ping

# Test OpenAI agent
curl -X POST http://localhost:8080/invocations \
    -H "Content-Type: application/json" \
    -d '{"prompt": "who is god of war and what is his role. Specifically kratos"}'
```

## 🧪 Expected Responses

### `/ping` Endpoint
```json
{"status": "healthy"}
```

### `/invocations` Endpoint
```json
{
  "result": {
    "content": [
      {
        "text": "15 * 7 = 105\n\nUsing the calculator: 15 × 7 = 105"
      }
    ],
    "role": "assistant"
  }
}
```

## 🐛 Troubleshooting

### Docker Not Running
```
❌ Error: Cannot connect to the Docker daemon
```
**Solution**: Start Docker Desktop and wait for it to fully initialize.

### Missing API Key
```
⚠️ OPENAI_API_KEY not set in .env file
```
**Solution**: Edit `.env` file and add your OpenAI API key.

### Port Already in Use
```
❌ Error: Port 8080 is already in use
```
**Solution**: Stop other services or use a different port:
```bash
docker run -p 8081:8080 ...
```

### ARM64 Build Issues
```
❌ Error: No builder instance found
```
**Solution**: Create the buildx builder:
```bash
docker buildx create --use --name agentcore-builder
```

### Container Won't Start
```bash
# Check container logs
docker logs openai-strands-test

# Check if image exists
docker images | grep openai-strands-agent
```

## 🔄 Container Management

### Stop the Container
```bash
# If running in background
docker stop openai-strands-test

# If running with --rm flag, it auto-removes when stopped
```

### Remove the Container
```bash
# Remove stopped container
docker rm openai-strands-test

# Remove the image
docker rmi openai-strands-agent:local
```

### View Container Logs
```bash
# Live logs
docker logs -f openai-strands-test

# Last 50 lines
docker logs --tail 50 openai-strands-test
```

## 🏗️ Dockerfile Details

The `Dockerfile.local` creates an ARM64 container with:

- **Base Image**: `python:3.12-slim` on ARM64
- **Dependencies**: All project requirements
- **Port**: 8080 (AgentCore standard)
- **Health Check**: Built-in `/ping` endpoint monitoring
- **Observability**: OpenTelemetry auto-instrumentation ready

## 🔄 Development Workflow

### 1. Code Changes
```bash
# After making code changes, rebuild the image
docker buildx build --platform linux/arm64 -f Dockerfile.local -t openai-strands-agent:local --load .
```

### 2. Quick Test
```bash
# Run automated test after rebuild
./docker-local-test.sh
```

### 3. Clean Rebuild
```bash
# Remove old image and rebuild from scratch
docker rmi openai-strands-agent:local
docker buildx build --platform linux/arm64 -f Dockerfile.local -t openai-strands-agent:local --load . --no-cache
```

## 🚀 Next Steps

Once your Docker local testing is successful:

1. **Deploy to AgentCore** using `deployment/deploy_to_agentcore.py`
2. **Monitor Performance** with the integration tests
3. **Set up Observability** with CloudWatch and X-Ray

## 📚 Related Files

- `Dockerfile.local` - ARM64 Dockerfile for local testing
- `docker-local-test.sh` - Automated testing script
- `deployment/Dockerfile` - Production Dockerfile for AgentCore
- `.env.example` - Environment variable template
- `requirements.txt` - Python dependencies

## 🔗 Useful Links

- [Docker Desktop Download](https://www.docker.com/products/docker-desktop/)
- [Docker Buildx Documentation](https://docs.docker.com/buildx/)
- [OpenAI API Keys](https://platform.openai.com/api-keys)
- [AWS Bedrock AgentCore Documentation](https://docs.aws.amazon.com/bedrock-agentcore/)