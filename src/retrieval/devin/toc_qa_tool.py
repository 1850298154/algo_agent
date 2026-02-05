import requests
import json

BASE_URL = "https://mcp.deepwiki.com/mcp"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream"
}

def save_to_file(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"结果已成功写入文件: {filename}")

def call_and_save(tool_name, arguments, request_id, output_file):
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        },
        "id": request_id
    }
    
    response = requests.post(BASE_URL, headers=HEADERS, json=payload)
    
    # 处理 SSE 或 普通 JSON
    final_result = {}
    if response.text.startswith("event:"):
        lines = response.text.split('\n')
        for line in lines:
            if line.startswith('data: '):
                final_result = json.loads(line[6:])
                break
    else:
        try:
            final_result = response.json()
        except:
            final_result = {"raw_error": "Failed to parse JSON", "content": response.text}
    
    # 写入文件
    save_to_file(output_file, final_result)

# --- 执行所有工具调用 ---

# 1. 保存结构
call_and_save(
    "read_wiki_structure", 
    {"repoName": "1850298154/algo_agent"}, 
    1, 
    "result_structure.json"
)

# 2. 保存内容
call_and_save(
    "read_wiki_contents", 
    {"repoName": "1850298154/algo_agent"}, 
    2, 
    "result_contents.json"
)

# 3. 保存提问结果
call_and_save(
    "ask_question", 
    {
        "repoName": "1850298154/algo_agent", 
        "question": "How does tool call work?"
    }, 
    3, 
    "result_question.json"
)