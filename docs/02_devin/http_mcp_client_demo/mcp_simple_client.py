#!/usr/bin/env python3
"""
Simplified MCP-style client that replicates the original functionality
without requiring full MCP server setup
"""

import requests
import json
import asyncio
from typing import Dict, Any

BASE_URL = "https://mcp.deepwiki.com/mcp"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream"
}

def save_to_file(filename: str, data: Any) -> None:
    """Save data to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"结果已成功写入文件: {filename}")

async def call_wiki_tool(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Call wiki tool via HTTP and return result"""
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        },
        "id": 1
    }
    
    try:
        response = requests.post(BASE_URL, headers=HEADERS, json=payload)
        
        # Handle SSE or regular JSON
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
        
        return final_result
    except Exception as e:
        return {"error": str(e)}

class WikiMCPClient:
    """MCP-style client for wiki operations"""
    
    def __init__(self):
        self.tools = {
            "read_wiki_structure": {
                "description": "Read the structure of a wiki repository",
                "parameters": {"repoName": "string"}
            },
            "read_wiki_contents": {
                "description": "Read the contents of a wiki repository", 
                "parameters": {"repoName": "string"}
            },
            "ask_question": {
                "description": "Ask a question about the wiki repository",
                "parameters": {"repoName": "string", "question": "string"}
            },
            "save_all_wiki_data": {
                "description": "Save all wiki data (structure, contents, and Q&A) to files",
                "parameters": {"repoName": "string", "question": "string (optional)"}
            }
        }
    
    def list_tools(self):
        """List available tools"""
        return self.tools
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a specific tool"""
        if tool_name == "save_all_wiki_data":
            return await self.save_all_wiki_data(arguments)
        else:
            return await call_wiki_tool(tool_name, arguments)
    
    async def save_all_wiki_data(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute all three operations and save to files"""
        repo_name = arguments["repoName"]
        question = arguments.get("question", "How does tool call work?")
        
        results = {}
        
        # 1. Get structure
        print("Getting wiki structure...")
        structure_result = await call_wiki_tool("read_wiki_structure", {"repoName": repo_name})
        save_to_file("result_structure.json", structure_result)
        results["structure"] = structure_result
        
        # 2. Get contents
        print("Getting wiki contents...")
        contents_result = await call_wiki_tool("read_wiki_contents", {"repoName": repo_name})
        save_to_file("result_contents.json", contents_result)
        results["contents"] = contents_result
        
        # 3. Ask question
        print(f"Asking question: {question}")
        question_result = await call_wiki_tool("ask_question", {
            "repoName": repo_name,
            "question": question
        })
        save_to_file("result_question.json", question_result)
        results["question"] = question_result
        
        return {
            "success": True,
            "message": f"All wiki data saved successfully for repository: {repo_name}",
            "files_created": ["result_structure.json", "result_contents.json", "result_question.json"],
            "results": results
        }

async def main():
    """Main function demonstrating usage"""
    client = WikiMCPClient()
    
    # List available tools
    print("Available tools:")
    for tool_name, tool_info in client.list_tools().items():
        print(f"- {tool_name}: {tool_info['description']}")
    
    print("\n" + "="*50 + "\n")
    
    # Option 1: Use the combined tool to save all data
    print("Executing save_all_wiki_data...")
    result = await client.call_tool(
        "save_all_wiki_data",
        {
            "repoName": "1850298154/algo_agent",
            "question": "How does tool call work?"
        }
    )
    
    print("Result:")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    print("\n" + "="*50 + "\n")
    
    # Option 2: Call individual tools
    print("Calling individual tools...")
    
    # Get structure
    print("1. Getting wiki structure...")
    structure_result = await client.call_tool(
        "read_wiki_structure",
        {"repoName": "1850298154/algo_agent"}
    )
    print("Structure result:")
    print(json.dumps(structure_result, ensure_ascii=False, indent=2)[:500] + "...")
    
    # Get contents
    print("\n2. Getting wiki contents...")
    contents_result = await client.call_tool(
        "read_wiki_contents",
        {"repoName": "1850298154/algo_agent"}
    )
    print("Contents result:")
    print(json.dumps(contents_result, ensure_ascii=False, indent=2)[:500] + "...")
    
    # Ask question
    print("\n3. Asking question...")
    question_result = await client.call_tool(
        "ask_question",
        {
            "repoName": "1850298154/algo_agent",
            "question": "How does tool call work?"
        }
    )
    print("Question result:")
    print(json.dumps(question_result, ensure_ascii=False, indent=2)[:500] + "...")

if __name__ == "__main__":
    asyncio.run(main())
