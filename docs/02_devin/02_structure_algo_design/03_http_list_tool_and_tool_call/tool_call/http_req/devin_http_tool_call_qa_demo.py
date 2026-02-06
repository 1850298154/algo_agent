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
'''response.text
event: message
data: {"jsonrpc":"2.0","id":1,"result":{"content":[{"type":"text","text":"Based on the provided codebase context, there is no information available regarding how authentication works within the `algo_agent` system itself. The documentation primarily focuses on setting up and connecting to various databases (PostgreSQL, MySQL, pgvector) for data processing examples. \n\nThe database setups involve specifying `POSTGRES_PASSWORD` for PostgreSQL and `MYSQL_ROOT_PASSWORD` for MySQL during container deployment, which are used for connecting to these databases.   However, this refers to database authentication, not user authentication for the `algo_agent` system itself.  \n\nA `ToolRouter` class is mentioned, which includes a `tool_permissions` attribute and a check for `user_role` to determine if a user has permission to call a tool.  This suggests a form of authorization based on roles, but the mechanism for authenticating the `user_role` itself is not described. \n\n## Notes\nThe provided context heavily details database setup and interaction, including connection parameters like usernames and passwords for PostgreSQL and MySQL.   While these are authentication credentials for database access, they do not explain how a user authenticates with the `algo_agent` system itself.   The `ToolRouter` snippet hints at role-based authorization, but the initial authentication process to assign or verify a `user_role` is not covered. \n\nWiki pages you might want to explore:\n- [Database Setup for Examples (1850298154/algo_agent)](/wiki/1850298154/algo_agent#8.3)\n\nView this search on DeepWiki: https://deepwiki.com/search/how-does-authentication-work_bf55116d-4f53-4d3d-879c-ba51f1bc1f32\n"}],"structuredContent":{"result":"Based on the provided codebase context, there is no information available regarding how authentication works within the `algo_agent` system itself. The documentation primarily focuses on setting up and connecting to various databases (PostgreSQL, MySQL, pgvector) for data processing examples. \n\nThe database setups involve specifying `POSTGRES_PASSWORD` for PostgreSQL and `MYSQL_ROOT_PASSWORD` for MySQL during container deployment, which are used for connecting to these databases.   However, this refers to database authentication, not user authentication for the `algo_agent` system itself.  \n\nA `ToolRouter` class is mentioned, which includes a `tool_permissions` attribute and a check for `user_role` to determine if a user has permission to call a tool.  This suggests a form of authorization based on roles, but the mechanism for authenticating the `user_role` itself is not described. \n\n## Notes\nThe provided context heavily details database setup and interaction, including connection parameters like usernames and passwords for PostgreSQL and MySQL.   While these are authentication credentials for database access, they do not explain how a user authenticates with the `algo_agent` system itself.   The `ToolRouter` snippet hints at role-based authorization, but the initial authentication process to assign or verify a `user_role` is not covered. \n\nWiki pages you might want to explore:\n- [Database Setup for Examples (1850298154/algo_agent)](/wiki/1850298154/algo_agent#8.3)\n\nView this search on DeepWiki: https://deepwiki.com/search/how-does-authentication-work_bf55116d-4f53-4d3d-879c-ba51f1bc1f32\n"},"isError":false}}
'''
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