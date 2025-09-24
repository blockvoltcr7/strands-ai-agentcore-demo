#!/usr/bin/env python3
"""
Unified deployment script for OpenAI Strands Agent to AWS ECR.
Handles ECR repository creation, Docker build, and push.
Note: Agent Core deployment via CLI often fails - use AWS Console instead.
"""
import boto3
import json
import os
import subprocess
import sys
from datetime import datetime


def run_command(cmd, capture_output=True, check=True, input_text=None):
    """Helper to run shell commands with proper error handling."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=capture_output,
            text=True,
            check=check,
            input=input_text
        )
        return result.stdout if capture_output else None
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {' '.join(cmd)}")
        print(f"   Error: {e.stderr if e.stderr else str(e)}")
        raise


def main():
    print("🚀 OpenAI Strands Agent - ECR Deployment")
    print("=" * 60)

    # Configuration
    region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    repository_name = "openai-strands-agent"

    # Verify AWS credentials
    print("\n📋 Step 1: Verifying AWS Configuration")
    try:
        sts_client = boto3.client("sts")
        caller_info = sts_client.get_caller_identity()
        account_id = caller_info["Account"]
        user_arn = caller_info["Arn"]

        print(f"✅ AWS Account: {account_id}")
        print(f"✅ User/Role: {user_arn.split('/')[-1]}")
        print(f"✅ Region: {region}")
    except Exception as e:
        print(f"❌ AWS credential error: {e}")
        print("\n💡 Fix: Configure AWS credentials:")
        print("   aws configure")
        print("   OR")
        print("   export AWS_ACCESS_KEY_ID=your-key")
        print("   export AWS_SECRET_ACCESS_KEY=your-secret")
        return 1

    # ECR setup
    image_uri = f"{account_id}.dkr.ecr.{region}.amazonaws.com/{repository_name}:latest"

    print("\n📦 Step 2: Setting up ECR Repository")
    try:
        ecr_client = boto3.client("ecr", region_name=region)

        # Check if repository exists
        try:
            ecr_client.describe_repositories(repositoryNames=[repository_name])
            print(f"✅ ECR repository '{repository_name}' already exists")
        except ecr_client.exceptions.RepositoryNotFoundException:
            # Create repository
            ecr_client.create_repository(
                repositoryName=repository_name,
                imageScanningConfiguration={'scanOnPush': True},
                encryptionConfiguration={'encryptionType': 'AES256'}
            )
            print(f"✅ Created ECR repository '{repository_name}'")
            print(f"   URI: {image_uri}")
    except Exception as e:
        print(f"❌ ECR error: {e}")
        print("\n💡 Fix: Ensure your IAM user has ECR permissions")
        print("   Attach policy: AmazonEC2ContainerRegistryFullAccess")
        return 1

    # Docker operations
    print("\n🐳 Step 3: Building and Pushing Docker Image")

    # Check Docker is running
    try:
        run_command(["docker", "info"], capture_output=True)
    except:
        print("❌ Docker is not running")
        print("\n💡 Fix: Start Docker Desktop")
        return 1

    # Login to ECR
    print("🔐 Logging into ECR...")
    try:
        login_password = run_command([
            "aws", "ecr", "get-login-password",
            "--region", region
        ])

        run_command([
            "docker", "login",
            "--username", "AWS",
            "--password-stdin",
            f"{account_id}.dkr.ecr.{region}.amazonaws.com"
        ], input_text=login_password, capture_output=True)

        print("✅ ECR login successful")
    except Exception as e:
        print(f"❌ ECR login failed")
        return 1

    # Build Docker image
    print("🏗️  Building ARM64 Docker image...")
    dockerfile_path = "deployment/Dockerfile"

    if not os.path.exists(dockerfile_path):
        print(f"❌ Dockerfile not found at {dockerfile_path}")
        return 1

    try:
        # Ensure buildx is available
        try:
            run_command(["docker", "buildx", "ls"], capture_output=True)
        except:
            print("📦 Setting up Docker buildx...")
            run_command(["docker", "buildx", "create", "--name", "agentcore-builder", "--use"])

        # Build and push in one step
        print(f"📤 Building and pushing to: {image_uri}")
        run_command([
            "docker", "buildx", "build",
            "--platform", "linux/arm64",
            "-f", dockerfile_path,
            "-t", image_uri,
            "--push",
            "."
        ], capture_output=False)

        print("✅ Docker image built and pushed successfully!")

    except Exception as e:
        print(f"❌ Docker build/push failed")
        print("\n💡 Common fixes:")
        print("   - Ensure Docker Desktop is running")
        print("   - Check your Dockerfile exists")
        print("   - Verify .env.example exists (copied to .env in container)")
        return 1

    # Success summary
    print("\n" + "🎉 " * 10)
    print("ECR DEPLOYMENT SUCCESSFUL!")
    print("🎉 " * 10)

    print(f"\n📋 Deployment Summary:")
    print(f"   Repository: {repository_name}")
    print(f"   Image URI: {image_uri}")
    print(f"   Region: {region}")

    print("\n📌 Next Steps:")
    print("1. Go to AWS Bedrock Agent Core in the console")
    print("2. Create or update your Agent Runtime")
    print("3. Use this Container URI:")
    print(f"   {image_uri}")
    print("4. Add environment variables:")
    print("   - OPENAI_API_KEY: your-api-key")
    print("   - OPENAI_MODEL: gpt-4o-mini")
    print("\n💡 Note: Agent Core CLI deployment often fails.")
    print("   Use the AWS Console for reliable deployment.")

    return 0


if __name__ == "__main__":
    sys.exit(main())