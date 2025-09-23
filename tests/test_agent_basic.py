#!/usr/bin/env python
"""
Pytest test suite for OpenAI Agent - validates 200 status and response format.
"""
import requests
import json
import pytest


@pytest.fixture(scope="module")
def agent_base_url():
    """Base URL for the agent."""
    return "http://localhost:8080"


def test_ping_endpoint(agent_base_url):
    """Test the /ping health check endpoint."""
    url = f"{agent_base_url}/ping"

    response = requests.get(url, timeout=10)

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"


def test_agent_invocation_status_code(agent_base_url):
    """Test that agent responds with 200 status code."""
    url = f"{agent_base_url}/invocations"
    payload = {"prompt": "Hello"}

    response = requests.post(url, json=payload, timeout=30)

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"


def test_agent_response_format(agent_base_url):
    """Test that agent returns valid JSON with 'result' field."""
    url = f"{agent_base_url}/invocations"
    payload = {"prompt": "Hello"}

    response = requests.post(url, json=payload, timeout=30)

    # Should be valid JSON
    result = response.json()

    # Should have 'result' field
    assert 'result' in result, f"Response missing 'result' field. Got: {result}"

    # Result should be a dict with expected structure
    assert isinstance(result['result'], dict), "Result should be a dictionary"


def test_agent_calculator_tool(agent_base_url):
    """Test that agent can use the calculator tool."""
    url = f"{agent_base_url}/invocations"
    payload = {"prompt": "Calculate 5 + 3 using the calculator"}

    response = requests.post(url, json=payload, timeout=30)

    assert response.status_code == 200
    result = response.json()
    assert 'result' in result

    # Response should contain the calculation result
    response_text = str(result['result']).lower()
    assert '8' in response_text or 'eight' in response_text, f"Expected calculation result in: {result}"


@pytest.mark.parametrize("prompt", [
    "Hello",
    "What is AI?",
    "Calculate 2 + 2",
])
def test_agent_multiple_prompts(agent_base_url, prompt):
    """Test agent with multiple different prompts."""
    url = f"{agent_base_url}/invocations"
    payload = {"prompt": prompt}

    response = requests.post(url, json=payload, timeout=30)

    assert response.status_code == 200
    result = response.json()
    assert 'result' in result
    assert isinstance(result['result'], dict)


def test_agent_error_handling_empty_prompt(agent_base_url):
    """Test agent error handling with empty prompt."""
    url = f"{agent_base_url}/invocations"
    payload = {"prompt": ""}

    response = requests.post(url, json=payload, timeout=30)

    # Should handle gracefully (either success or proper error)
    assert response.status_code in [200, 400, 422], f"Unexpected status code: {response.status_code}"

    if response.status_code == 200:
        result = response.json()
        assert 'result' in result or 'error' in result


def test_agent_error_handling_missing_prompt(agent_base_url):
    """Test agent error handling with missing prompt field."""
    url = f"{agent_base_url}/invocations"
    payload = {"message": "Hello"}  # Wrong field name

    response = requests.post(url, json=payload, timeout=30)

    # Should handle gracefully
    result = response.json()
    assert 'result' in result or 'error' in result


if __name__ == "__main__":
    # Run pytest when executed directly
    import subprocess
    import sys

    result = subprocess.run([
        sys.executable, "-m", "pytest",
        __file__,
        "-v",
        "--tb=short",
        "--color=yes"
    ])

    sys.exit(result.returncode)