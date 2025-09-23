"""
Utility functions for the OpenAI Strands AgentCore application.
"""
import json
from typing import Any, Dict
from datetime import datetime, timezone


def format_response(message: str, model: str = "openai-agent") -> Dict[str, Any]:
    """Format agent response in a consistent structure."""
    return {
        "message": message,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model": model,
    }


def validate_payload(payload: Dict[str, Any]) -> str:
    """Validate and extract prompt from payload."""
    if not isinstance(payload, dict):
        raise ValueError("Payload must be a dictionary")

    prompt = payload.get("prompt", "")
    if not prompt:
        raise ValueError(
            "No prompt found in payload. Please provide a 'prompt' key."
        )

    return prompt


def safe_json_serialize(data: Any) -> str:
    """Safely serialize data to JSON."""
    try:
        return json.dumps(data, default=str)
    except (TypeError, ValueError) as e:
        return json.dumps({"error": f"Serialization failed: {str(e)}"})