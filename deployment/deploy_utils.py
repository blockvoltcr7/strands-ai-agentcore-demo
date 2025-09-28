#!/usr/bin/env python3
"""
Shared utilities for deployment scripts.
"""
import subprocess
import os


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


def check_docker_running():
    """Check if Docker is running."""
    try:
        run_command(["docker", "info"], capture_output=True)
        return True
    except:
        return False


def get_project_config():
    """Get common project configuration."""
    return {
        "region": os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
        "repository_name": "openai-strands-agent",
        "dockerfile_path": "deployment/Dockerfile",
        "platform": "linux/arm64"
    }


def print_header(title):
    """Print a formatted header."""
    print(f"🚀 {title}")
    print("=" * 60)


def print_step(step_num, description):
    """Print a formatted step."""
    print(f"\n📋 Step {step_num}: {description}")


def print_success(title):
    """Print success message."""
    print("\n" + "🎉 " * 10)
    print(f"{title.upper()}!")
    print("🎉 " * 10)


def print_error(message, fixes=None):
    """Print error message with optional fixes."""
    print(f"❌ {message}")
    if fixes:
        print("\n💡 Common fixes:")
        for fix in fixes:
            print(f"   - {fix}")
