# Strands AI AgentCore Demo

This project demonstrates how to deploy Strands agents to AWS Bedrock AgentCore following the [official documentation](https://strandsagents.com/latest/documentation/docs/user-guide/deploy/deploy_to_bedrock_agentcore/).

## Prerequisites

- Python 3.12+
- AWS Account with Bedrock access (for full agent functionality)
- uv package manager (or pip)

## Installation

The project dependencies are already installed via uv. If you need to reinstall:

```bash
uv add strands-agents strands-agents-tools strands-agents-builder bedrock-agentcore
```

Or with pip:

```bash
pip install strands-agents strands-agents-tools strands-agents-builder bedrock-agentcore
```

## Project Structure

The project has been refactored into a more organized folder structure:

- `src/agents/agent.py`: Basic Strands agent with AWS Bedrock integration
- `src/agents/agent_streaming.py`: Streaming-enabled agent implementation
- `src/agents/simple_agent.py`: Simple echo agent (no AWS required)
- `src/server/main.py`: Main entry point for the application
- `tests/test_agent.py`: Test script for verifying agent endpoints
- `tests/test_aws_bedrock.py`: AWS Bedrock access testing script
- `scripts/setup_aws.py`: Interactive AWS credentials setup
- `scripts/env_setup.sh`: Environment variables setup script
- `docs/README.md`: This file
- `docs/AWS_SETUP_GUIDE.md`: Complete AWS setup guide

## Testing the Agents

### 1. Simple Agent (No AWS Required)

This is the easiest way to test the Bedrock AgentCore framework:

```bash
# Start the simple agent server
python src/agents/simple_agent.py

# In another terminal, test with curl
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello world!"}'

# Or use the Python test script
python tests/test_agent.py
```

Expected response:
```json
{"result": "Echo: Hello world!"}
```

### 2. Full Strands Agent (AWS Credentials Required)

Before running, ensure you have AWS credentials configured:

```bash
# Configure AWS credentials (if not already done)
aws configure

# Or set environment variables
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

Then run the agent:

```bash
# Start the Strands agent server
python src/agents/agent.py

# Test with the Python script
python tests/test_agent.py
```

### 3. Streaming Agent (AWS Credentials Required)

For streaming responses:

```bash
# Start the streaming agent
python src/agents/agent_streaming.py

# Test with curl or Python script
python tests/test_agent.py
```

## Testing with Custom Prompts

Modify `test_agent.py` to test different prompts:

```python
import requests

url = "http://localhost:8080/invocations"
payload = {"prompt": "Your custom prompt here"}

response = requests.post(url, json=payload)
print(response.json())
```

## Troubleshooting

### Port Already in Use

If you see "address already in use" error:

```bash
# Find and kill the process using port 8080
lsof -i :8080 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

### AWS Credentials Error

If you see "UnrecognizedClientException" or "security token invalid":

1. **Test your current AWS configuration:**
   ```bash
   python tests/test_aws_bedrock.py
   ```

2. **If credentials are invalid, reconfigure them:**

   **Option A: Use the interactive setup script**
   ```bash
   source scripts/env_setup.sh
   ```

   **Option B: Set environment variables manually**
   ```bash
   export AWS_ACCESS_KEY_ID=your_access_key_here
   export AWS_SECRET_ACCESS_KEY=your_secret_key_here
   export AWS_DEFAULT_REGION=us-east-1
   ```

   **Option C: Update ~/.aws/credentials file**
   ```bash
   aws configure
   # Enter your Access Key ID
   # Enter your Secret Access Key
   # Enter region: us-east-1
   # Enter output format: json
   ```

3. **Verify your credentials work:**
   ```bash
   aws sts get-caller-identity
   ```

4. **Ensure Bedrock is enabled in your AWS account:**
   - Log into AWS Console
   - Navigate to Amazon Bedrock service
   - Click "Get Started" if you haven't already
   - Request access to models (especially Claude models)
   - Ensure your IAM user has the necessary permissions:
     ```json
     {
       "Version": "2012-10-17",
       "Statement": [
         {
           "Effect": "Allow",
           "Action": "bedrock:*",
           "Resource": "*"
         }
       ]
     }
     ```

### Module Import Errors

If you encounter import errors:

```bash
# Activate the virtual environment
source .venv/bin/activate

# Verify installations
pip list | grep -E "strands|bedrock"
```

## Next Steps

Once local testing is successful, you can proceed to Step 3 in the [Strands documentation](https://strandsagents.com/latest/documentation/docs/user-guide/deploy/deploy_to_bedrock_agentcore/) to deploy to AWS Bedrock AgentCore.

## Environment Variables

You can customize the agent behavior with these environment variables:

- `AWS_DEFAULT_REGION` - AWS region for Bedrock (default: us-east-1)
- `PORT` - Server port (default: 8080)
- `LOG_LEVEL` - Logging verbosity (default: INFO)

## License

This is a demo project for educational purposes.