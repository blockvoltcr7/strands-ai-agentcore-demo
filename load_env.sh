#!/bin/bash
# Load environment variables from .env file

if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo "✅ AWS environment variables loaded!"
    echo "   Region: $AWS_DEFAULT_REGION"
    echo "   Access Key: ${AWS_ACCESS_KEY_ID:0:10}..."

    # Test AWS credentials
    aws sts get-caller-identity > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "✅ AWS credentials are valid!"
    else
        echo "❌ AWS credentials are invalid. Please check your Secret Access Key in .env"
    fi
else
    echo "❌ .env file not found!"
fi