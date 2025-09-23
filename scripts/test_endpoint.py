import requests
import json

url = "https://gateway-quick-start-3b33cf-6ew1ekhgbc.gateway.bedrock-agentcore.us-east-1.amazonaws.com/mcp"
headers = {
    "Content-Type": "application/json",
    "x-api-key": "agent-core-api-key"
}
payload = {
    "prompt": "Hello! Can you calculate 25 * 8 for me?"
}

response = requests.post(url, headers=headers, json=payload)
print(response.json())

# Expected Response

# You should get back something like:
# {
# "result": {
#     "role": "assistant",
#     "content": [
#     {
#         "text": "The result of 25 × 8 is 200."
#     }
#     ]
# }
# }