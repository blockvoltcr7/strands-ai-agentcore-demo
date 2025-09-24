# Testing Your Deployed Agent

Once your OpenAI Strands Agent is deployed to AWS Bedrock Agent Core, you can test it using the `invoke_agent.py` script.

## Prerequisites

- ✅ Agent deployed to AWS Agent Core
- ✅ Agent status shows "Ready"
- ✅ AWS credentials configured
- ✅ OpenAI API key set in Agent Core environment variables

## Basic Usage

### Command Format
```bash
python deployment/invoke_agent.py --agent-arn "YOUR_AGENT_ARN" --prompt "YOUR_PROMPT"
```

### Your Current Agent ARN
```bash
python deployment/invoke_agent.py --agent-arn "arn:aws:bedrock-agentcore:us-east-1:343075903183:runtime/hosted_agent_6qv9x-g7yz867pDY" --prompt "YOUR_PROMPT"
```

## Example Test Commands

### 1. Test Calculator Tool
```bash
python deployment/invoke_agent.py --agent-arn "arn:aws:bedrock-agentcore:us-east-1:343075903183:runtime/hosted_agent_6qv9x-g7yz867pDY" --prompt "Hello! Can you calculate 25 * 8 for me?"
```

Expected response:
```json
{
  "result": {
    "role": "assistant",
    "content": [
      {
        "text": "The result of 25 × 8 is 200."
      }
    ]
  }
}
```

### 2. Test Agent Capabilities
```bash
python deployment/invoke_agent.py --agent-arn "arn:aws:bedrock-agentcore:us-east-1:343075903183:runtime/hosted_agent_6qv9x-g7yz867pDY" --prompt "Explain what you can do"
```

### 3. Test Complex Math
```bash
python deployment/invoke_agent.py --agent-arn "arn:aws:bedrock-agentcore:us-east-1:343075903183:runtime/hosted_agent_6qv9x-g7yz867pDY" --prompt "What is the square root of 144 plus 15 divided by 3?"
```

### 4. Test General Conversation
```bash
python deployment/invoke_agent.py --agent-arn "arn:aws:bedrock-agentcore:us-east-1:343075903183:runtime/hosted_agent_6qv9x-g7yz867pDY" --prompt "Tell me about artificial intelligence"
```

## Command Parameters

| Parameter | Description | Required | Default |
|-----------|-------------|----------|---------|
| `--agent-arn` | Your Agent Core runtime ARN | ✅ Yes | None |
| `--prompt` | Message to send to the agent | ❌ No | "Hello! Can you help me with a simple math problem: what is 15 * 7?" |
| `--region` | AWS region | ❌ No | us-east-1 |
| `--session-id` | Custom session ID (33+ chars) | ❌ No | Auto-generated |

## Advanced Usage

### Custom Session ID
```bash
python deployment/invoke_agent.py \
  --agent-arn "arn:aws:bedrock-agentcore:us-east-1:343075903183:runtime/hosted_agent_6qv9x-g7yz867pDY" \
  --prompt "Hello!" \
  --session-id "my-custom-session-12345678901234567890"
```

### Different Region
```bash
python deployment/invoke_agent.py \
  --agent-arn "arn:aws:bedrock-agentcore:us-west-2:343075903183:runtime/your-agent-id" \
  --prompt "Hello!" \
  --region us-west-2
```

## Troubleshooting

### Error: "Endpoint 'DEFAULT' is not ready for invocation"
- **Solution**: Agent is still starting. Wait 2-3 minutes and try again.

### Error: "Invalid security token"
- **Solution**: Check AWS credentials:
  ```bash
  aws sts get-caller-identity
  ```

### Error: "Invalid API key provided"
- **Solution**: Update OpenAI API key in Agent Core environment variables

### Error: "ValidationException"
- **Solution**: Check agent ARN is correct and agent status is "Ready"

## Alternative Testing Methods

### 1. AWS Console Test Interface
1. Go to **AWS Bedrock Agent Core**
2. Find your agent → **Test** tab
3. Enter test payload:
   ```json
   {
     "prompt": "Hello! Can you calculate 25 * 8 for me?"
   }
   ```

### 2. HTTP Gateway (if configured)
```bash
curl -X POST https://your-gateway-url/mcp \
  -H "Content-Type: application/json" \
  -H "x-api-key: your-api-key" \
  -d '{"prompt": "Hello! Can you calculate 25 * 8 for me?"}'
```

## Expected Response Format

Successful responses will have this structure:
```json
{
  "result": {
    "role": "assistant",
    "content": [
      {
        "text": "Response text here"
      }
    ]
  }
}
```

Error responses will have:
```json
{
  "error": "Error description here"
}
```

## Performance Tips

- **Session IDs**: Use consistent session IDs for conversational context
- **Prompts**: Be specific about what you want the agent to do
- **Math**: The agent has access to a calculator tool for mathematical operations
- **Timeout**: Commands may take 5-30 seconds depending on complexity

## Getting Your Agent ARN

To find your current agent ARN:
1. Go to **AWS Bedrock Agent Core** console
2. Click on your agent
3. Copy the **Runtime ID** from agent details
4. Format: `arn:aws:bedrock-agentcore:us-east-1:ACCOUNT-ID:runtime/RUNTIME-ID`

---

**🎉 Your OpenAI Strands Agent is ready for testing!**

For deployment instructions, see: [ECR_DEPLOYMENT_QUICKSTART.md](./ECR_DEPLOYMENT_QUICKSTART.md)
For complete setup guide, see: [AGENT_CORE_DEPLOYMENT_GUIDE.md](./AGENT_CORE_DEPLOYMENT_GUIDE.md)