"""
MCP 客户端

    https://zhuanlan.zhihu.com/p/1939376580968292383
pip install mcp
    
    https://pypi.org/project/mcp/#session-properties-and-methods
    
    https://github.com/modelcontextprotocol/python-sdk
    https://deepwiki.com/modelcontextprotocol/python-sdk

    https://deepwiki.com/search/mcptooltool_3d154dc8-2a7a-4728-86f4-b02972d75a68?mode=fast



"""
BASE_URL = "https://mcp.deepwiki.com/mcp"

"""可流式 HTTP 客户端"""
import asyncio
from mcp import ClientSession
# from mcp.client.streamable_http import streamablehttp_client
from mcp.client.streamable_http import streamable_http_client
from mcp.types import ListToolsResult, CallToolResult

async def main():
    async with streamable_http_client(BASE_URL) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            # tools:ListToolsResult = await session.list_tools()
            tools:ListToolsResult = await session.list_tools()
            # print(f"可用工具：{[tool.name for tool in tools.tools]}")
            print(f"可用工具：{tools}")
            
            resources = await session.list_resources()
            print(f"Available resources: {[r.uri for r in resources.resources]}")            
            
            # 调用工具
            result: CallToolResult = await session.call_tool("read_wiki_structure", arguments={"repoName": "1850298154/algo_agent"})
            print(f"工具结果：{result.content}")
            """
            可用工具：meta=None nextCursor=None tools=[Tool(name='read_wiki_structure', title=None, description='Get a list of documentation topics for a GitHub repository.\n\nArgs:\n    repoName: GitHub rfastmcp': {'tags': []}}, execution=None), Tool(name='ask_question', title=None, description='Ask any question about a GitHub repository and get an AI-powered, context-grounded response.\n\nArgs:\n    repoName: GitHub repository or list of repositories (max 10) in owner/repo format\n    question: The question to ask about the repository', inputSchema={'properties': {'repoName': {'anyOf': [{'type': 'string'}, {'items': {'type': 'string'}, 'type': 'array'}]}, 'question': {'type': 'string'}}, 'required': ['repoName', 'question'], 'type': 'object'}, outputSchema={'properties': {'result': {'type': 'string'}}, 'required': ['result'], 'type': 'object', 'x-fastmcp-wrap-result': True}, icons=None, annotations=None, meta={'_fastmcp': {'tags': []}}, execution=None)] 
            
            [TextContent(type='text', text='Available pages for 1850298154/algo_agent:\n\n- 1 Overview\n- 2 Getting Started\n- 3 Agent Orchestration\n  - 3.1 Query Processing Loop\n  - 3.2 LLM Integration\n  - 3.3 Memory and Context Management\n  - 3.4 Action Coordination\n- 4 Tool System\n  - 4.1 BaseTool Interface\n  - 4.2 Python Code Execution Tool\n  - 4.3 Recursive Task Planning Tool\n- 5 Execution Runtime\n  - 5.1 Subprocess Execution\n  - 5.2 Subthread Execution\n  - 5.3 Direct Execution\n  - 5.4 ExecutionResult and Status Handling\n  - 5.5 Workspace State Management\n  - 5.6 Working Directory and Environment\n- 6 Observability and Logging\n  - 6.1 Logging System Architecture\n  - 6.2 Log Files and Analysis\n  - 6.3 Tracing and Performance Monitoring\n- 7 Use Cases and Examples\n  - 7.1 Emergency Response Planning Example\n  - 7.2 Data Processing and Visualization\n  - 7.3 Geographic Data Processing\n- 8 Development and Testing\n  - 8.1 Testing the Execution System\n  - 8.2 Creating New Tools\n  - 8.3 Database Setup for Examples\n- 9 Architecture Reference\n  - 9.1 ExecutionResult Schema Reference\n  - 9.2 Task Tree Schema Reference\n  - 9.3 Tool Schema Format\n- 10 Troubleshooting\n  - 10.1 Common Execution Errors\n  - 10.2 Tool Call Errors', annotations=None, meta=None)]             
            """

if __name__ == "__main__":
    asyncio.run(main())