#!/bin/bash
# Local Docker testing script for OpenAI Strands Agent

set -e

echo "🐳 OpenAI Strands Agent - Local Docker Testing"
echo "=============================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop and try again."
    echo "💡 Start Docker Desktop app or run: open -a Docker"
    exit 1
fi

echo "✅ Docker is running"

# Create buildx builder if it doesn't exist
if ! docker buildx ls | grep -q agentcore-builder; then
    echo "📦 Creating ARM64 buildx builder..."
    docker buildx create --use --name agentcore-builder
else
    echo "✅ Using existing buildx builder"
    docker buildx use agentcore-builder
fi

# Build the ARM64 image
echo "🔨 Building ARM64 Docker image..."
docker buildx build --platform linux/arm64 \
    -f Dockerfile.local \
    -t openai-strands-agent:local \
    --load . \
    --no-cache

echo "✅ Docker image built successfully!"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from .env.example..."
    cp .env.example .env
    echo "📝 Please edit .env and add your OPENAI_API_KEY before running the container"
    exit 1
fi

# Check if OPENAI_API_KEY is set
if ! grep -q "OPENAI_API_KEY=sk-" .env 2>/dev/null; then
    echo "⚠️  OPENAI_API_KEY not set in .env file"
    echo "📝 Please edit .env and add your OpenAI API key"
    exit 1
fi

echo "🚀 Starting container..."
docker run --platform linux/arm64 \
    -p 8080:8080 \
    --env-file .env \
    --name openai-strands-test \
    --rm \
    openai-strands-agent:local &

# Wait for container to start
echo "⏳ Waiting for agent to start..."
sleep 10

# Test the endpoints
echo "🧪 Testing endpoints..."

# Test /ping
echo "Testing /ping endpoint..."
if curl -f http://localhost:8080/ping > /dev/null 2>&1; then
    echo "✅ /ping endpoint working"
else
    echo "❌ /ping endpoint failed"
fi

# Test /invocations
echo "Testing /invocations endpoint..."
response=$(curl -s -X POST http://localhost:8080/invocations \
    -H "Content-Type: application/json" \
    -d '{"prompt": "Hello! This is a test."}')

if echo "$response" | grep -q "result"; then
    echo "✅ /invocations endpoint working"
    echo "📋 Response: $response"
else
    echo "❌ /invocations endpoint failed"
    echo "📋 Response: $response"
fi

echo ""
echo "🎉 Local Docker testing complete!"
echo "🔗 Agent running at: http://localhost:8080"
echo "🛑 To stop: docker stop openai-strands-test"