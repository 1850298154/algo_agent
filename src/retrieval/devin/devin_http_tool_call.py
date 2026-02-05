import requests

BASE_URL = "https://mcp.deepwiki.com/mcp"

response = requests.post(
    BASE_URL,
    headers={
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"
    },
    json={
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "ask_question",
            "arguments": {
                "repoName": "1850298154/algo_agent",
                "question": "How does authentication work?"
            }
        },
        "id": 1
    }
)

print(f"Status Code: {response.status_code}")
print(f"Response Text: {response.text}")

# Handle SSE format response
if response.text.startswith("event:"):
    # Extract JSON data from SSE format
    lines = response.text.split('\n')
    for line in lines:
        if line.startswith('data: '):
            json_data = line[6:]  # Remove 'data: ' prefix
            import json
            result = json.loads(json_data)
            print("Parsed result:")
            print(result)
            break
else:
    # Handle regular JSON response
    try:
        result = response.json()
        print(result)
    except requests.exceptions.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        print(f"Response is not valid JSON. Status: {response.status_code}")
        print(f"Raw response: {response.text}")