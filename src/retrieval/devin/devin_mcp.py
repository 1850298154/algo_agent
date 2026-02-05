# import asyncio
# from mcp import ClientSession
# from mcp.client.sse import sse_client

# async def main():
#     # --- 配置区 ---
#     # 场景 A: 公开版
#     target_url = "https://mcp.deepwiki.com/mcp"
#     headers = {}

#     # 场景 B: 私有版 (如果使用私有版，请取消下面两行的注释)
#     # target_url = "https://mcp.devin.ai/mcp"
#     # headers = {"Authorization": "Bearer YOUR_API_KEY_HERE"}

#     print(f"🚀 正在连接到 MCP 服务器: {target_url}...")

#     # 1. 初始化 SSE 传输层
#     async with sse_client(url=target_url, headers=headers) as (read_stream, write_stream):
        
#         # 2. 建立 MCP 会话
#         async with ClientSession(read_stream, write_stream) as session:
            
#             # 3. 初始化 (协议握手)
#             await session.initialize()
#             print("✅ 握手成功！")

#             # 4. 列出所有可用的工具 (Tools)
#             print("\n🔍 正在获取可用工具列表...")
#             response = await session.list_tools()
#             tools = response.tools
            
#             for tool in tools:
#                 print(f"  - [工具名]: {tool.name}")
#                 print(f"    [描述]: {tool.description}")
#                 print(f"    [参数]: {tool.inputSchema.get('properties', {}).keys()}")
#                 print("-" * 30)

#             # 5. 示例：调用一个工具 (假设有一个工具叫 'search')
#             # if any(t.name == "search" for t in tools):
#             #     print("\n🛠️  正在调用 'search' 工具...")
#             #     result = await session.call_tool("search", arguments={"query": "什么是 MCP 协议？"})
#             #     print(f"📝 结果: {result}")

# if __name__ == "__main__":
#     try:
#         asyncio.run(main())
#     except KeyboardInterrupt:
#         pass
#     except Exception as e:
#         print(f"❌ 运行出错: {e}")

import asyncio
import httpx
import traceback
from mcp import ClientSession
from mcp.client.sse import sse_client

# 目标配置
MCP_URL = "https://mcp.deepwiki.com/mcp"
# MCP_URL = "https://mcp.devin.ai/mcp" # 如果用这个，记得加 headers
HEADERS = {
    "User-Agent": "mcp-python-client/1.0", # 有些服务器需要 User-Agent
    # "Authorization": "Bearer <YOUR_KEY>"
    "Accept": "text/event-stream",    
}

async def check_connection_first():
    """先用普通 HTTP 请求测试服务器是否存活"""
    print(f"📡 [预检] 正在测试连接: {MCP_URL} ...")
    async with httpx.AsyncClient() as client:
        try:
            # MCP SSE 端点通常接受 GET 请求
            resp = await client.get(MCP_URL, headers=HEADERS, timeout=5.0)
            print(f"📡 [预检] HTTP 状态码: {resp.status_code}")
            if resp.status_code != 200:
                print(f"⚠️ [预警] 服务器返回了非 200 状态码，连接可能会失败。内容: {resp.text}")
        except Exception as e:
            print(f"❌ [预检失败] 无法连接到服务器: {e}")
            return False
    return True

async def main():
    # 1. 先跑预检，排除网络通断问题
    if not await check_connection_first():
        return

    print(f"\n🚀 [启动] 正在通过 MCP SDK 连接...")
    
    try:
        # 增加 timeout 时间，防止握手太慢
        async with sse_client(url=MCP_URL, headers=HEADERS, timeout=30.0) as (read_stream, write_stream):
            print("✅ SSE 流已连接，正在初始化 Session...")
            
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                print("🤝 MCP 协议握手成功！")

                result = await session.list_tools()
                print(f"\n🎉 成功获取工具列表 ({len(result.tools)} 个):")
                for tool in result.tools:
                    print(f" - {tool.name}: {tool.description[:50]}...")

    except Exception as e:
        print("\n💥 捕获到详细错误:")
        # 专门处理 TaskGroup/ExceptionGroup 错误，把里面的内容打印出来
        if hasattr(e, 'exceptions'):
            for i, idx_e in enumerate(e.exceptions):
                print(f"  错误 {i+1}: {type(idx_e).__name__} - {idx_e}")
        else:
            print(f"  {type(e).__name__}: {e}")
        
        # 打印完整的堆栈跟踪，方便排查
        print("\n📋 完整堆栈:")
        traceback.print_exc()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass