#!/usr/bin/env python3
"""
Automated deployment script for OpenAI Strands Agent to AWS Bedrock AgentCore.
"""
import boto3
import json
import os
import subprocess
import sys
from datetime import datetime


class AgentCoreDeployer:
    def __init__(self, region: str = "us-east-1"):
        self.region = region
        self.ecr_client = boto3.client("ecr", region_name=region)
        self.agentcore_client = boto3.client("bedrock-agentcore-control", region_name=region)
        self.account_id = boto3.client("sts").get_caller_identity()["Account"]

        # Configuration
        self.image_name = "openai-strands-agent"
        self.agent_name = "openai-strands-agent"
        self.repository_name = f"{self.image_name}"
        self.image_uri = f"{self.account_id}.dkr.ecr.{region}.amazonaws.com/{self.repository_name}:latest"

    def create_ecr_repository(self):
        """Create ECR repository if it doesn't exist."""
        try:
            print(f"📦 Creating ECR repository: {self.repository_name}")
            self.ecr_client.create_repository(repositoryName=self.repository_name)
            print("✅ ECR repository created successfully")
        except self.ecr_client.exceptions.RepositoryAlreadyExistsException:
            print("✅ ECR repository already exists")
        except Exception as e:
            print(f"❌ Error creating ECR repository: {e}")
            sys.exit(1)

    def build_and_push_image(self):
        """Build Docker image and push to ECR."""
        try:
            print("🔨 Building Docker image...")

            # Set up Docker buildx for ARM64
            subprocess.run(["docker", "buildx", "create", "--use"],
                         capture_output=True, check=False)

            # Build ARM64 image
            build_cmd = [
                "docker", "buildx", "build",
                "--platform", "linux/arm64",
                "-f", "deployment/Dockerfile",
                "-t", self.image_uri,
                "--load",
                "."
            ]

            result = subprocess.run(build_cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ Docker build failed: {result.stderr}")
                sys.exit(1)

            print("✅ Docker image built successfully")

            # Login to ECR
            print("🔐 Logging into ECR...")
            login_cmd = [
                "aws", "ecr", "get-login-password",
                "--region", self.region
            ]
            login_result = subprocess.run(login_cmd, capture_output=True, text=True)

            if login_result.returncode != 0:
                print(f"❌ ECR login failed: {login_result.stderr}")
                sys.exit(1)

            docker_login_cmd = [
                "docker", "login", "--username", "AWS",
                "--password-stdin",
                f"{self.account_id}.dkr.ecr.{self.region}.amazonaws.com"
            ]
            subprocess.run(docker_login_cmd, input=login_result.stdout, text=True, check=True)

            # Push image
            print("📤 Pushing image to ECR...")
            push_cmd = ["docker", "push", self.image_uri]
            result = subprocess.run(push_cmd, capture_output=True, text=True)

            if result.returncode != 0:
                print(f"❌ Docker push failed: {result.stderr}")
                sys.exit(1)

            print("✅ Image pushed to ECR successfully")

        except Exception as e:
            print(f"❌ Error in build and push: {e}")
            sys.exit(1)

    def deploy_agent_runtime(self, role_arn: str):
        """Deploy agent to AgentCore."""
        try:
            print("🚀 Deploying agent to AgentCore...")

            response = self.agentcore_client.create_agent_runtime(
                agentRuntimeName=self.agent_name,
                agentRuntimeArtifact={
                    'containerConfiguration': {
                        'containerUri': self.image_uri
                    }
                },
                networkConfiguration={"networkMode": "PUBLIC"},
                roleArn=role_arn
            )

            print("✅ Agent Runtime created successfully!")
            print(f"📍 Agent Runtime ARN: {response['agentRuntimeArn']}")
            print(f"📊 Status: {response['status']}")

            return response['agentRuntimeArn']

        except Exception as e:
            print(f"❌ Error deploying agent: {e}")
            sys.exit(1)

    def test_deployment(self, agent_arn: str):
        """Test the deployed agent."""
        try:
            print("🧪 Testing deployed agent...")

            agent_core_client = boto3.client('bedrock-agentcore', region_name=self.region)

            test_payload = json.dumps({
                "prompt": "Hello! This is a test of the deployed OpenAI agent."
            })

            response = agent_core_client.invoke_agent_runtime(
                agentRuntimeArn=agent_arn,
                runtimeSessionId="test-session-" + datetime.now().strftime("%Y%m%d%H%M%S"),
                payload=test_payload,
                qualifier="DEFAULT"
            )

            response_body = response['response'].read()
            response_data = json.loads(response_body)

            print("✅ Test successful!")
            print(f"📝 Response: {response_data}")

        except Exception as e:
            print(f"⚠️ Test failed (this might be expected during initial deployment): {e}")

    def deploy(self, role_arn: str):
        """Full deployment process."""
        print("🚀 Starting AgentCore Deployment Process")
        print("=" * 50)

        # Validate inputs
        if not role_arn:
            print("❌ AgentCore IAM Role ARN is required")
            print("Please provide the role ARN using --role-arn parameter")
            sys.exit(1)

        # Deployment steps
        self.create_ecr_repository()
        self.build_and_push_image()
        agent_arn = self.deploy_agent_runtime(role_arn)
        self.test_deployment(agent_arn)

        print("\n" + "🎉 " * 10)
        print("DEPLOYMENT COMPLETE!")
        print("🎉 " * 10)
        print(f"\n📍 Agent ARN: {agent_arn}")
        print(f"🌐 Region: {self.region}")
        print(f"🐳 Image: {self.image_uri}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Deploy OpenAI Strands Agent to AWS AgentCore")
    parser.add_argument("--role-arn", required=True,
                       help="AgentCore IAM Role ARN (e.g., arn:aws:iam::123456789012:role/AgentRuntimeRole)")
    parser.add_argument("--region", default="us-east-1",
                       help="AWS region for deployment (default: us-east-1)")

    args = parser.parse_args()

    deployer = AgentCoreDeployer(region=args.region)
    deployer.deploy(role_arn=args.role_arn)


if __name__ == "__main__":
    main()