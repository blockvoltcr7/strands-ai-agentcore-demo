from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands import Agent
from strands.models.openai import OpenAIModel
from strands_tools import calculator
import sys
import os
import logging

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.settings import settings
from utils.helpers import validate_payload, format_response

app = BedrockAgentCoreApp()

# Configure logging for observability
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler()]
)

# Enable Strands SDK logging
logging.getLogger("strands").setLevel(logging.DEBUG)

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
    logger = logging.getLogger(__name__)
    try:
        logger.info(f"Processing request with payload: {payload}")

        # Validate payload and extract prompt
        user_message = validate_payload(payload)
        logger.info(f"Validated user message: {user_message}")

        # Process with agent
        logger.info("Invoking agent with OpenAI model")
        result = agent(user_message)
        logger.info("Agent processing completed successfully")

        # Return formatted response
        response = {"result": result.message}
        logger.info(f"Returning response: {response}")
        return response
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        return {"error": f"Invalid request: {str(e)}"}
    except Exception as e:
        logger.error(f"Processing error: {str(e)}", exc_info=True)
        return {"error": f"Failed to process request: {str(e)}"}

if __name__ == "__main__":
    print("🚀 Starting OpenAI Strands Agent with AgentCore...")
    print(f"Model: {settings.OPENAI_MODEL}")
    print(f"Host: {settings.HOST}:{settings.PORT}")
    app.run(host=settings.HOST, port=settings.PORT)