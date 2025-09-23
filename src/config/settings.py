"""
Configuration settings for the OpenAI Strands AgentCore application.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings."""

    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    OPENAI_MAX_TOKENS: int = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
    OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))

    # AgentCore Configuration
    AGENTCORE_REGION: str = os.getenv("AGENTCORE_REGION", "us-east-1")
    AGENTCORE_ROLE_ARN: str = os.getenv("AGENTCORE_ROLE_ARN", "")

    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8080"))

    # Observability Configuration
    ENABLE_TRACING: bool = os.getenv("ENABLE_TRACING", "false").lower() == "true"

    @classmethod
    def validate(cls) -> bool:
        """Validate required settings."""
        if not cls.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY environment variable is required. "
                "Please set it in your .env file."
            )
        return True


# Global settings instance
settings = Settings()