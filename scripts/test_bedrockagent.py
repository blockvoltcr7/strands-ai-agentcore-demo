#!/usr/bin/env python3
"""
Bedrock Agent - Universe Question

This script creates a Strands AI agent that uses Amazon Bedrock models
to ask a philosophical question about the universe and print the response.
"""

import os
import sys
from typing import Optional

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

try:
    from strands import Agent
    from strands.models import BedrockModel
except ImportError as e:
    print(f"Error importing Strands: {e}")
    print("Please install Strands: pip install strands")
    sys.exit(1)


def create_universe_agent() -> Agent:
    """
    Create a Strands AI agent configured to use Amazon Bedrock.
    
    Returns:
        Agent: Configured Strands agent with Bedrock model
    """
    try:
        # Create a Bedrock model with Claude Sonnet
        bedrock_model = BedrockModel(
            model_id="amazon.nova-micro-v1:0",
            temperature=0.7,
            max_tokens=1000,
            region_name="us-east-1"
        )
        
        # Create agent with the model
        agent = Agent(
            model=bedrock_model,
            system_prompt="You are a thoughtful philosopher and scientist who ponders deep questions about the universe. Provide insightful, creative, and scientifically-grounded responses to questions about existence, reality, and the cosmos."
        )
        
        return agent
        
    except Exception as e:
        print(f"Error creating agent: {e}")
        print("Please ensure AWS credentials are configured and Bedrock model access is granted.")
        raise


def ask_universe_question(agent: Agent, question: str = None) -> str:
    """
    Ask the agent a question about the universe and return the response.
    
    Args:
        agent: The Strands agent instance
        question: The question to ask (optional, uses default if not provided)
        
    Returns:
        str: The agent's response
    """
    if question is None:
        question = "What is the ultimate nature of reality and our place in the universe?"
    
    try:
        print(f"🌌 Asking: {question}")
        print("=" * 60)
        
        # Get response from agent
        response = agent(question)
        
        return str(response)
        
    except Exception as e:
        error_msg = f"Error getting response: {e}"
        print(error_msg)
        return error_msg


def main():
    """
    Main function to run the universe question agent.
    """
    print("🚀 Strands AI Agent - Universe Question")
    print("=" * 50)
    
    # Check AWS credentials
    if not (os.getenv('AWS_ACCESS_KEY_ID') or os.path.exists(os.path.expanduser('~/.aws/credentials'))):
        print("⚠️  AWS credentials not found!")
        print("Please configure AWS credentials using one of these methods:")
        print("1. aws configure")
        print("2. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables")
        print("3. Use AWS IAM roles if running on AWS infrastructure")
        return
    
    try:
        # Create the agent
        print("🤖 Creating Strands AI agent with Amazon Bedrock...")
        agent = create_universe_agent()
        print("✅ Agent created successfully!")
        
        # Ask the universe question
        response = ask_universe_question(agent)
        
        # Print the response
        print("\n📝 Agent Response:")
        print("-" * 30)
        print(response)
        
        # Ask follow-up questions
        follow_up_questions = [
            "How does consciousness emerge from the universe?",
            "What existed before the Big Bang?",
            "Are we alone in the universe?"
        ]
        
        print("\n" + "=" * 60)
        print("🤔 Follow-up Questions:")
        
        for i, follow_up in enumerate(follow_up_questions, 1):
            print(f"\n{i}. {follow_up}")
            follow_up_response = ask_universe_question(agent, follow_up)
            print(follow_up_response)
            print()
            
    except Exception as e:
        print(f"❌ Error running agent: {e}")
        print("\nTroubleshooting tips:")
        print("1. Ensure AWS credentials are properly configured")
        print("2. Verify Bedrock model access is granted in AWS Console")
        print("3. Check if the specified region supports the model")
        print("4. Ensure Strands is properly installed: pip install strands")


if __name__ == "__main__":
    main()