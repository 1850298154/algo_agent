import asyncio
import os
from dotenv import load_dotenv
from fastmcp import Client
from fastmcp.mcp_config import RemoteMCPServer, MCPConfig
from aiolimiter import AsyncLimiter
from enum import Enum, unique
from pydantic import BaseModel, ConfigDict, Field
load_dotenv()

# --------------------------
# 定义Pydantic模型封装客户端相关对象
# --------------------------
class ClientCacheItem(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,  # 允许非标准类型（兼容原有逻辑）
    )
    """封装MCP客户端、协程锁、限流器的Pydantic模型"""
    # 1. 复用的单纯享元类
    client: Client          # MCP客户端实例
    limiter: AsyncLimiter   # 速率限流器
    semaphore: asyncio.Semaphore  # 协程信号量（控制并发数）

# --------------------------
# 定义枚举类标识不同的MCP服务器（可扩展）
# --------------------------
@unique
class MCPServerEnum(Enum):
    DEVIN = "devin"
    GITHUB = "github"

# ---------------------------
# MCP客户端缓存（单例享元模式）
# ---------------------------
devin_cache_item = ClientCacheItem(
    client=Client(MCPConfig(mcpServers={
                MCPServerEnum.DEVIN: 
                    RemoteMCPServer(
                    url="https://mcp.devin.ai/mcp",
                    transport="http",
                    auth=os.getenv("DEVIN_API_KEY")
                )})),
    limiter=AsyncLimiter(1, 1), #　请求频率：控制在1-2 次 / 秒（60-120 次 / 分钟）以下
    semaphore=asyncio.Semaphore(5),  # 并发连接：不超过5 个同时请求（与第三方实现默认值一致）
)

github_cache_item = ClientCacheItem(
    client=Client(MCPConfig(mcpServers={
                MCPServerEnum.GITHUB: 
                    RemoteMCPServer(
                    url="https://api.githubcopilot.com/mcp/",
                    transport="http",
                    auth=os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
                )})),
    limiter=AsyncLimiter(1, 1),
    semaphore=asyncio.Semaphore(5),  # 并发连接：不超过5 个同时请求（与第三方实现默认值一致）
)

