#!/usr/bin/env python3
"""
ECR deployment script for OpenAI Strands Agent.
Builds and pushes Docker image to AWS ECR for production deployment.
"""
import boto3
import sys
import os
from deploy_utils import (
    run_command, check_docker_running, get_project_config,
    print_header, print_step, print_success, print_error
)


def verify_aws_credentials(region):
    """Verify AWS credentials and return account info."""
    print_step(1, "Verifying AWS Configuration")
    
    try:
        sts_client = boto3.client("sts")
        caller_info = sts_client.get_caller_identity()
        account_id = caller_info["Account"]
        user_arn = caller_info["Arn"]

        print(f"✅ AWS Account: {account_id}")
        print(f"✅ User/Role: {user_arn.split('/')[-1]}")
        print(f"✅ Region: {region}")
        
        return account_id
        
    except Exception as e:
        print_error(f"AWS credential error: {e}", [
            "Configure AWS credentials: aws configure",
            "OR set environment variables:",
            "  export AWS_ACCESS_KEY_ID=your-key",
            "  export AWS_SECRET_ACCESS_KEY=your-secret"
        ])
        return None


def setup_ecr_repository(region, repository_name):
    """Create ECR repository if it doesn't exist."""
    print_step(2, "Setting up ECR Repository")
    
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
        
        return True
        
    except Exception as e:
        print_error(f"ECR error: {e}", [
            "Ensure your IAM user has ECR permissions",
            "Attach policy: AmazonEC2ContainerRegistryFullAccess"
        ])
        return False


def login_to_ecr(region, account_id):
    """Login to ECR registry."""
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
        return True
        
    except Exception as e:
        print_error("ECR login failed")
        return False


def build_and_push_image(config, image_uri):
    """Build and push Docker image to ECR."""
    print_step(3, "Building and Pushing Docker Image")
    
    dockerfile_path = config["dockerfile_path"]
    if not os.path.exists(dockerfile_path):
        print_error(f"Dockerfile not found at {dockerfile_path}")
        return False
    
    print(f"🚀 Using optimized build with minimal dependencies")

    try:
        # Ensure buildx is available
        try:
            run_command(["docker", "buildx", "ls"], capture_output=True)
        except:
            print("📦 Setting up Docker buildx...")
            run_command(["docker", "buildx", "create", "--name", "agentcore-builder", "--use"])

        # Build and push in one step
        print(f"🏗️  Building {config['platform']} image...")
        print(f"📤 Pushing to: {image_uri}")
        
        run_command([
            "docker", "buildx", "build",
            "--platform", config["platform"],
            "-f", dockerfile_path,
            "-t", image_uri,
            "--push",
            "."
        ], capture_output=False)

        print("✅ Docker image built and pushed successfully!")
        return True

    except Exception as e:
        print_error("Docker build/push failed", [
            "Ensure Docker Desktop is running",
            "Check your Dockerfile exists",
            "Verify .env.example exists (copied to .env in container)",
            "Check if pyproject.toml is in the root directory"
        ])
        return False


def main():
    print_header("OpenAI Strands Agent - ECR Deployment")
    
    # Get configuration
    config = get_project_config()
    region = config["region"]
    repository_name = config["repository_name"]
    
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description="Deploy OpenAI Strands Agent to ECR")
    parser.add_argument("--region", default=region, help=f"AWS region (default: {region})")
    parser.add_argument("--repository", default=repository_name, help=f"ECR repository name (default: {repository_name})")
    parser.add_argument("--tag", default="latest", help="Image tag (default: latest)")
    parser.add_argument("--skip-docker-check", action="store_true", help="Skip Docker running check")
    
    args = parser.parse_args()
    
    # Update config with args
    region = args.region
    repository_name = args.repository
    
    # Check Docker
    if not args.skip_docker_check and not check_docker_running():
        print_error("Docker is not running", [
            "Start Docker Desktop",
            "Use --skip-docker-check if using remote Docker"
        ])
        return 1
    
    if not args.skip_docker_check:
        print("✅ Docker is running")
    
    # Verify AWS credentials
    account_id = verify_aws_credentials(region)
    if not account_id:
        return 1
    
    # Setup ECR repository
    if not setup_ecr_repository(region, repository_name):
        return 1
    
    # Build image URI
    image_uri = f"{account_id}.dkr.ecr.{region}.amazonaws.com/{repository_name}:{args.tag}"
    print(f"📋 Target image URI: {image_uri}")
    
    # Login to ECR
    if not login_to_ecr(region, account_id):
        return 1
    
    # Build and push image
    if not build_and_push_image(config, image_uri):
        return 1
    
    # Success summary
    print_success("ECR Deployment Successful")

    print(f"\n📋 Deployment Summary:")
    print(f"   Repository: {repository_name}")
    print(f"   Image URI: {image_uri}")
    print(f"   Region: {region}")
    print(f"   Platform: {config['platform']}")

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
