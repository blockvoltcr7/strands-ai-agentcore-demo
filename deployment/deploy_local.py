#!/usr/bin/env python3
"""
Local Docker deployment script for OpenAI Strands Agent.
Builds and runs the Docker container locally for testing.
"""
import sys
import os
from deploy_utils import (
    run_command, check_docker_running, get_project_config,
    print_header, print_step, print_success, print_error
)


def build_local_image(config):
    """Build Docker image for local testing."""
    print_step(1, "Building Local Docker Image")
    
    dockerfile_path = config["dockerfile_path"]
    if not os.path.exists(dockerfile_path):
        print_error(f"Dockerfile not found at {dockerfile_path}")
        return False
    
    try:
        image_name = f"{config['repository_name']}:local"
        
        print(f"🏗️  Building image: {image_name}")
        print(f"📄 Using optimized Dockerfile: {dockerfile_path}")
        run_command([
            "docker", "build",
            "-f", dockerfile_path,
            "-t", image_name,
            "."
        ], capture_output=False)
        
        print(f"✅ Local image built successfully: {image_name}")
        return True
        
    except Exception as e:
        print_error("Docker build failed", [
            "Ensure Docker Desktop is running",
            "Check your Dockerfile syntax",
            "Verify all required files exist",
            "Ensure deployment/requirements.txt exists"
        ])
        return False


def run_local_container(config, port=8080, detached=True):
    """Run the Docker container locally."""
    print_step(2, "Running Local Container")
    
    try:
        image_name = f"{config['repository_name']}:local"
        container_name = f"{config['repository_name']}-local"
        
        # Stop existing container if running
        try:
            run_command(["docker", "stop", container_name], capture_output=True)
            run_command(["docker", "rm", container_name], capture_output=True)
            print("🧹 Cleaned up existing container")
        except:
            pass  # Container doesn't exist, that's fine
        
        # Run new container
        cmd = [
            "docker", "run",
            "--name", container_name,
            "-p", f"{port}:8080",
            "--env-file", ".env"
        ]
        
        if detached:
            cmd.append("-d")
        
        cmd.append(image_name)
        
        print(f"🚀 Starting container on port {port}...")
        run_command(cmd, capture_output=False)
        
        if detached:
            print(f"✅ Container running in background")
            print(f"   Container name: {container_name}")
            print(f"   Local URL: http://localhost:{port}")
            print(f"   Health check: http://localhost:{port}/ping")
            print(f"\n📋 Container Management:")
            print(f"   View logs: docker logs {container_name}")
            print(f"   Stop: docker stop {container_name}")
            print(f"   Remove: docker rm {container_name}")
        else:
            print(f"✅ Container started in foreground mode")
        
        return True
        
    except Exception as e:
        print_error("Failed to run container", [
            "Check if port is already in use",
            "Ensure image was built successfully",
            "Verify Docker Desktop is running"
        ])
        return False


def show_container_status(config):
    """Show status of local containers."""
    print_step(3, "Container Status")
    
    try:
        container_name = f"{config['repository_name']}-local"
        
        # Check if container is running
        result = run_command([
            "docker", "ps", "-f", f"name={container_name}", "--format", "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
        ])
        
        if container_name in result:
            print("✅ Container is running:")
            print(result)
        else:
            print("ℹ️  Container is not currently running")
            
            # Check if container exists but is stopped
            result = run_command([
                "docker", "ps", "-a", "-f", f"name={container_name}", "--format", "table {{.Names}}\t{{.Status}}"
            ])
            
            if container_name in result:
                print("📋 Stopped container found:")
                print(result)
                print(f"   Start with: docker start {container_name}")
        
    except Exception as e:
        print_error("Failed to check container status")


def main():
    print_header("OpenAI Strands Agent - Local Deployment")
    
    # Get configuration
    config = get_project_config()
    
    # Check Docker
    if not check_docker_running():
        print_error("Docker is not running", [
            "Start Docker Desktop",
            "Ensure Docker daemon is accessible"
        ])
        return 1
    
    print("✅ Docker is running")
    
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description="Deploy OpenAI Strands Agent locally")
    parser.add_argument("--build-only", action="store_true", help="Only build the image, don't run")
    parser.add_argument("--run-only", action="store_true", help="Only run existing image, don't build")
    parser.add_argument("--status", action="store_true", help="Show container status")
    parser.add_argument("--port", type=int, default=8080, help="Port to run on (default: 8080)")
    parser.add_argument("--foreground", action="store_true", help="Run in foreground mode")
    
    args = parser.parse_args()
    
    if args.status:
        show_container_status(config)
        return 0
    
    # Build image
    if not args.run_only:
        if not build_local_image(config):
            return 1
    
    # Run container
    if not args.build_only:
        if not run_local_container(config, port=args.port, detached=not args.foreground):
            return 1
    
    # Success
    if args.build_only:
        print_success("Local Build Complete")
    elif args.run_only:
        print_success("Local Container Started")
    else:
        print_success("Local Deployment Complete")
        
        print(f"\n📋 Local Deployment Summary:")
        print(f"   Image: {config['repository_name']}:local")
        print(f"   Container: {config['repository_name']}-local")
        print(f"   Port: {args.port}")
        
        print(f"\n📌 Next Steps:")
        print(f"1. Test your agent: http://localhost:{args.port}")
        print(f"2. Check health: http://localhost:{args.port}/ping")
        print(f"3. View logs: docker logs {config['repository_name']}-local")
        print(f"4. When ready, deploy to ECR: python deployment/deploy_ecr.py")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
