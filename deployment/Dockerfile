# Dockerfile for AWS Bedrock AgentCore Deployment
# Must be ARM64 for AgentCore compatibility
FROM --platform=linux/arm64 python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY deployment/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY .env.example .env

# Set Python path
ENV PYTHONPATH=/app

# Expose port 8080 (required by AgentCore)
EXPOSE 8080

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=30s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/ping || exit 1

# Run the agent directly
CMD ["python", "src/agents/openai_agent.py"]