# Strands AI Agent - Universe Question

This project demonstrates how to create a Strands AI agent that uses Amazon Bedrock models to ask philosophical questions about the universe and receive thoughtful responses.

## Features

- **Amazon Bedrock Integration**: Uses Claude Sonnet 4 via Amazon Bedrock
- **Philosophical AI Agent**: Configured with a system prompt for deep, thoughtful responses
- **Interactive Questions**: Asks multiple questions about the universe and existence
- **Error Handling**: Comprehensive error handling and troubleshooting guidance
- **AWS Integration**: Proper AWS credential management and region configuration

## Prerequisites

### AWS Setup

1. **AWS Account**: You need an active AWS account
2. **Model Access**: Request access to Claude models in Amazon Bedrock:
   - Go to AWS Bedrock Console → Model Access
   - Request access to "Claude 3.5 Sonnet v2" and "Claude 4 Sonnet"
3. **AWS Credentials**: Configure credentials with Bedrock permissions:
   ```bash
   aws configure
   ```
   Or set environment variables:
   ```bash
   export AWS_ACCESS_KEY_ID=your_access_key
   export AWS_SECRET_ACCESS_KEY=your_secret_key
   export AWS_DEFAULT_REGION=us-west-2
   ```

### Required IAM Permissions

Your AWS credentials need these permissions:
- `bedrock:InvokeModel`
- `bedrock:InvokeModelWithResponseStream`

### Python Dependencies

Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the agent directly:
```bash
python test_bedrockagent.py
```

### Custom Questions

You can modify the questions in the script or extend it to accept command-line arguments:

```python
from test_bedrockagent import create_universe_agent, ask_universe_question

agent = create_universe_agent()
response = ask_universe_question(agent, "What is the meaning of life?")
print(response)
```

## Configuration Options

### Model Configuration

The agent uses these default settings:
- **Model**: `anthropic.claude-sonnet-4-20250514-v1:0`
- **Temperature**: 0.7 (creative but coherent)
- **Max Tokens**: 1000
- **Region**: `us-west-2`

You can modify these in the `create_universe_agent()` function.

### System Prompt

The agent is configured with a system prompt that encourages philosophical and scientific thinking about cosmic questions. You can customize this in the agent creation.

## Troubleshooting

### Common Issues

1. **Import Error**: Ensure Strands is installed: `pip install strands`
2. **AWS Credentials**: Check if AWS credentials are properly configured
3. **Model Access**: Verify model access is granted in AWS Bedrock Console
4. **Region Issues**: Ensure the specified region supports your chosen model
5. **Permission Errors**: Check IAM permissions for Bedrock access

### Error Messages

- **"You don't have access to the model"**: Request model access in AWS Bedrock Console
- **"Model identifier is invalid"**: Check if using correct model ID format
- **"AWS credentials not found"**: Configure AWS credentials using `aws configure`

## Example Output

```
🚀 Strands AI Agent - Universe Question
==================================================
🤖 Creating Strands AI agent with Amazon Bedrock...
✅ Agent created successfully!

🌌 Asking: What is the ultimate nature of reality and our place in the universe?
============================================================

📝 Agent Response:
------------------------------
The nature of reality appears to be a profound interplay between consciousness and the cosmos...
```

## Extending the Agent

### Adding New Questions

Modify the `follow_up_questions` list in the `main()` function:

```python
follow_up_questions = [
    "Your custom question here?",
    "Another philosophical question?"
]
```

### Using Different Models

Change the model in `create_universe_agent()`:

```python
bedrock_model = BedrockModel(
    model_id="us.amazon.nova-premier-v1:0",  # Different model
    temperature=0.5,
    max_tokens=500
)
```

### Custom System Prompt

Modify the system prompt for different agent personalities:

```python
agent = Agent(
    model=bedrock_model,
    system_prompt="You are a cosmic explorer who answers questions with wonder and scientific accuracy..."
)
```

## Security Notes

- Never commit AWS credentials to version control
- Use IAM roles for production deployments
- Consider using AWS Secrets Manager for sensitive configuration
- Follow AWS security best practices for Bedrock usage
