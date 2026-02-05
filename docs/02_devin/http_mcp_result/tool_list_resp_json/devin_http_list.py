import requests

BASE_URL = "https://mcp.deepwiki.com/mcp"

response = requests.post(
    BASE_URL,
    headers={
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"  # 必须同时接受这两种格式
    },
    json={
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "ask_question",
            "arguments": {
                "repo": "owner/repo-name",
                "question": "How does authentication work?"
            }
        },
        "id": 1
    }
)

result = response.text
print(result)