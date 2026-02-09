import asyncio
import os
from typing import Dict, Optional
from dotenv import load_dotenv
from fastmcp import Client
from fastmcp.client.client import CallToolResult
from fastmcp.mcp_config import RemoteMCPServer, MCPConfig
from aiolimiter import AsyncLimiter
from enum import Enum, unique

# 导入Pydantic核心类
from pydantic import BaseModel, ConfigDict
from src.mcp import mcp_enum

# --------------------------
# 示例：多协程调用同一个 MCP Server
# --------------------------
async def call_mcp_tool(
    cache_item: mcp_enum.ClientCacheItem, 
    tool_name: str, 
    arguments: dict) -> CallToolResult:
    """封装的 MCP 工具调用函数"""
    async with cache_item.client as client: 
        try:
            async with cache_item.limiter:
                async with cache_item.semaphore:
                    result: CallToolResult = await client.call_tool(
                        name=tool_name,
                        arguments=arguments,
                        raise_on_error=False
                    )
                    if result.is_error:
                        # print(f"协程 {asyncio.current_task().get_name()} 调用失败: {result.content[0].text}")
                        return result.content[0].text
                    else:
                        # print(f"协程 {asyncio.current_task().get_name()} 调用成功: {result.data}")
                        return result.data
        except Exception as e:
            print(f"协程 {asyncio.current_task().get_name()} 异常: {str(e)}")
            raise


async def main():
    tasks = []
    for i in range(1):  # 启动8个协程并发调用
        task = asyncio.create_task(
            call_mcp_tool(
                cache_item=mcp_enum.devin_cache_item,
                tool_name="read_wiki_structure",
                arguments={"repoName": "1850298154/HULK"}
            ),
            name=f"Task-{i+1}"
        )
        tasks.append(task)
    
    # 3. 等待所有协程完成
    results:list[str] = await asyncio.gather(*tasks)
    return results

if __name__ == "__main__":
    results:list[str]  = asyncio.run(main())
    print("\n所有协程结果：\n", results)
