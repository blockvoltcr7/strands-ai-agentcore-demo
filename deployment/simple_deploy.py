#!/usr/bin/env python3
"""
Simplified deployment script that assumes ECR repo exists.
"""
import boto3
import json
import os
import subprocess
import sys
from datetime import datetime


def main():
    print("🚀 OpenAI Strands Agent - AgentCore Deployment")
    print("=" * 60)

    # Configuration
    region = "us-east-1"
    repository_name = "openai-strands-agent"
    agent_name = "openai-strands-agent"

    # Get account ID
    try:
        sts_client = boto3.client("sts")
        account_id = sts_client.get_caller_identity()["Account"]
        print(f"✅ AWS Account: {account_id}")
        print(f"✅ Region: {region}")
    except Exception as e:
        print(f"❌ Error getting AWS account info: {e}")
        return 1

    image_uri = f"{account_id}.dkr.ecr.{region}.amazonaws.com/{repository_name}:latest"
    print(f"📦 Target Image URI: {image_uri}")

    # Step 1: Build and push Docker image
    print("\n🔨 Step 1: Building and pushing Docker image...")

    try:
        # Login to ECR
        print("🔐 Logging into ECR...")
        login_cmd = [
            "aws", "ecr", "get-login-password",
            "--region", region
        ]
        login_result = subprocess.run(login_cmd, capture_output=True, text=True, check=True)

        docker_login_cmd = [
            "docker", "login", "--username", "AWS", "--password-stdin",
            f"{account_id}.dkr.ecr.{region}.amazonaws.com"
        ]
        subprocess.run(docker_login_cmd, input=login_result.stdout, text=True, check=True)
        print("✅ ECR login successful")

    except subprocess.CalledProcessError as e:
        print(f"❌ ECR login failed: {e}")
        print("💡 Make sure you have ECR permissions or ask admin to create repository")
        return 1

    try:
        # Build ARM64 image for AgentCore
        print("🏗️ Building ARM64 Docker image...")

        # Use production Dockerfile
        dockerfile_path = "deployment/Dockerfile"
        if not os.path.exists(dockerfile_path):
            print(f"❌ Production Dockerfile not found at {dockerfile_path}")
            return 1

        build_cmd = [
            "docker", "buildx", "build",
            "--platform", "linux/arm64",
            "-f", dockerfile_path,
            "-t", image_uri,
            "--push", "."
        ]

        subprocess.run(build_cmd, check=True)
        print("✅ Docker image built and pushed successfully")

    except subprocess.CalledProcessError as e:
        print(f"❌ Docker build/push failed: {e}")
        return 1

    # Step 2: Create IAM role for AgentCore
    role_arn = f"arn:aws:iam::{account_id}:role/AgentRuntimeRole"
    print(f"\n🔑 Step 2: Using IAM Role: {role_arn}")
    print("💡 Make sure this role exists with AgentCore permissions")

    # Step 3: Deploy to AgentCore
    print("\n🚀 Step 3: Deploying to AgentCore...")

    try:
        agentcore_client = boto3.client("bedrock-agentcore-control", region_name=region)

        response = agentcore_client.create_agent_runtime(
            agentRuntimeName=agent_name,
            agentRuntimeArtifact={
                'containerConfiguration': {
                    'containerUri': image_uri
                }
            },
            networkConfiguration={"networkMode": "PUBLIC"},
            roleArn=role_arn
        )

        agent_runtime_arn = response['agentRuntimeArn']
        print(f"✅ Agent deployed successfully!")
        print(f"📋 Agent Runtime ARN: {agent_runtime_arn}")

        # Step 4: Test the deployment
        print("\n🧪 Step 4: Testing deployment...")
        print("⏳ Waiting for agent to be ready...")

        # Wait for agent to be active
        import time
        for i in range(12):  # Wait up to 2 minutes
            try:
                status_response = agentcore_client.get_agent_runtime(
                    agentRuntimeArn=agent_runtime_arn
                )
                status = status_response['status']
                print(f"📊 Agent Status: {status}")

                if status == 'ACTIVE':
                    print("✅ Agent is ready!")
                    break
                elif status in ['FAILED', 'STOPPED']:
                    print(f"❌ Agent deployment failed with status: {status}")
                    return 1

            except Exception as e:
                print(f"⚠️ Error checking status: {e}")

            time.sleep(10)
        else:
            print("⚠️ Agent taking longer than expected to start")

        print(f"\n🎉 Deployment Complete!")
        print(f"📋 Agent Runtime ARN: {agent_runtime_arn}")
        print(f"💡 Use this ARN to invoke your agent")

        return 0

    except Exception as e:
        print(f"❌ AgentCore deployment failed: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)