# Optimized Dockerfile for AWS Bedrock AgentCore Deployment
# Multi-stage build with minimal dependencies for fast builds
FROM --platform=linux/arm64 python:3.12-slim as builder

WORKDIR /app

# Install only essential build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy project files for installation
COPY pyproject.toml .
COPY deployment/requirements.txt requirements.txt

# Install dependencies in a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Production stage
FROM --platform=linux/arm64 python:3.12-slim

WORKDIR /app

# Install only runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY src/ ./src/
COPY .env.example .env

# Set Python path
ENV PYTHONPATH=/app

# Expose port 8080 (required by AgentCore)
EXPOSE 8080

# Optimized health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=2 \
    CMD curl -f http://localhost:8080/ping || exit 1

# Run the agent
CMD ["python", "src/agents/openai_agent.py"]