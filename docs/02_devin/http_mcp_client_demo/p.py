import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client

async def main():
    # 连接到 SSE (Server-Sent Events) 端点
    url = "https://mcp.deepwiki.com/mcp"
    
    print(f"Connecting to {url}...")
    
    # 使用 sse_client 上下文管理器
    async with sse_client(url=url) as (read_stream, write_stream):
        # 创建 MCP 客户端会话
        async with ClientSession(read_stream, write_stream) as session:
            # 初始化连接
            await session.initialize()
            
            # 列出可用工具 (对应你代码中的 tools/list)
            result = await session.list_tools()
            
            # 打印工具列表
            print("\n--- Available Tools ---")
            for tool in result.tools:
                print(f"Name: {tool.name}")
                print(f"Description: {tool.description}")
                print(f"Schema: {tool.inputSchema}\n")

if __name__ == "__main__":
    asyncio.run(main())