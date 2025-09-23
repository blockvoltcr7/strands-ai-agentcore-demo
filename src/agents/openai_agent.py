from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands import Agent
from strands.models.openai import OpenAIModel
from strands_tools import calculator
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.settings import settings
from utils.helpers import validate_payload, format_response

app = BedrockAgentCoreApp()

# Validate settings
settings.validate()

# Initialize OpenAI model with settings
model = OpenAIModel(
    client_args={
        "api_key": settings.OPENAI_API_KEY,
    },
    model_id=settings.OPENAI_MODEL,
    params={
        "max_tokens": settings.OPENAI_MAX_TOKENS,
        "temperature": settings.OPENAI_TEMPERATURE,
    }
)

# Create agent with tools
agent = Agent(model=model, tools=[calculator])

@app.entrypoint
def invoke(payload):
    """Process user input and return a response using OpenAI"""
    try:
        # Validate payload and extract prompt
        user_message = validate_payload(payload)

        # Process with agent
        result = agent(user_message)

        # Return formatted response
        return {"result": result.message}
    except ValueError as e:
        return {"error": f"Invalid request: {str(e)}"}
    except Exception as e:
        return {"error": f"Failed to process request: {str(e)}"}

if __name__ == "__main__":
    print("🚀 Starting OpenAI Strands Agent with AgentCore...")
    print(f"Model: {settings.OPENAI_MODEL}")
    print(f"Host: {settings.HOST}:{settings.PORT}")
    app.run(host=settings.HOST, port=settings.PORT)