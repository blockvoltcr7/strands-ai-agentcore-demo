#!/usr/bin/env python3
"""
Test script to invoke the deployed OpenAI Strands Agent on AWS AgentCore.
"""
import boto3
import json
import sys
from datetime import datetime


def invoke_agent(agent_arn: str, prompt: str, region: str = "us-east-1", session_id: str = None):
    """Invoke the deployed agent with a prompt."""

    if not session_id:
        session_id = f"test-session-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    # Ensure session_id meets AgentCore requirements (33+ characters)
    if len(session_id) < 33:
        session_id = session_id + "-" + "x" * (33 - len(session_id))

    client = boto3.client('bedrock-agentcore', region_name=region)

    payload = json.dumps({"prompt": prompt})

    try:
        print(f"🚀 Invoking agent...")
        print(f"📍 Agent ARN: {agent_arn}")
        print(f"🔗 Session ID: {session_id}")
        print(f"💬 Prompt: {prompt}")
        print("-" * 50)

        response = client.invoke_agent_runtime(
            agentRuntimeArn=agent_arn,
            runtimeSessionId=session_id,
            payload=payload,
            qualifier="DEFAULT"
        )

        response_body = response['response'].read()
        response_data = json.loads(response_body)

        print("✅ Success!")
        print(f"📝 Response: {json.dumps(response_data, indent=2)}")

        return response_data

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Invoke deployed OpenAI Strands Agent")
    parser.add_argument("--agent-arn", required=True,
                       help="AgentCore Agent Runtime ARN")
    parser.add_argument("--prompt", default="Hello! Can you help me with a simple math problem: what is 15 * 7?",
                       help="Prompt to send to the agent")
    parser.add_argument("--region", default="us-east-1",
                       help="AWS region (default: us-east-1)")
    parser.add_argument("--session-id",
                       help="Session ID (will be auto-generated if not provided)")

    args = parser.parse_args()

    invoke_agent(
        agent_arn=args.agent_arn,
        prompt=args.prompt,
        region=args.region,
        session_id=args.session_id
    )


if __name__ == "__main__":
    main()