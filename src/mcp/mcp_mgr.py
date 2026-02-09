import asyncio
import os
from typing import Dict, Optional
from dotenv import load_dotenv
from fastmcp import Client
from fastmcp.client.client import CallToolResult
from fastmcp.mcp_config import RemoteMCPServer, MCPConfig
import mcp
from aiolimiter import AsyncLimiter
from  enum import Enum, unique

@unique
class MCPServerName(Enum):
    DEVIN = "devin"


# 加载环境变量
load_dotenv()

BASE_URL = "https://mcp.devin.ai/mcp"
DEVIN_API_KEY = os.getenv("DEVIN_API_KEY")

RemoteMCPServer(
    url=BASE_URL,
    transport="http",
    auth=DEVIN_API_KEY
)

# --------------------------
# 核心：MCP Client 单例管理器
# --------------------------
class MCPClientManager:
    # 缓存 Client 实例：key=server名称, value=(client实例, 协程锁, 限流器)
    _client_cache: Dict[str, tuple[Client, asyncio.Lock, AsyncLimiter]] = {}
    _config_cache: Dict[str, MCPConfig] = {}

    @classmethod
    def init_server_config(cls, server_name: MCPServerName, url: str, api_key: str, transport: str = "http"):
        """初始化 MCP Server 配置（提前注册，避免重复创建）"""
        if server_name not in cls._config_cache:
            cls._config_cache[server_name] = MCPConfig(
                mcpServers={
                    server_name: RemoteMCPServer(
                        url=url,
                        transport=transport,
                        auth=api_key
                    )
                }
            )

    @classmethod
    async def get_client(cls, server_name: MCPServerName, rate_limit: tuple[int, int] = (1, 60)) -> Client:
        """
        获取单例 Client 实例（自动创建/缓存）
        :param server_name: MCP Server 名称（如 "devin"）
        :param rate_limit: 限流配置 (每秒最大请求数, 时间窗口(秒))，默认 10req/s
        """
        if server_name not in cls._client_cache:
            # 1. 创建 Client 实例
            config = cls._config_cache[server_name]
            client = Client(config)
            # 2. 初始化协程锁和限流器
            lock = asyncio.Lock()
            limiter = AsyncLimiter(*rate_limit)
            # 3. 缓存
            cls._client_cache[server_name] = (client, lock, limiter)
            # 4. 初始化 Client 连接
            await client.__aenter__()
        
        return cls._client_cache[server_name][0]

    @classmethod
    async def close_all(cls):
        """关闭所有缓存的 Client 连接"""
        for client, _, _ in cls._client_cache.values():
            await client.__aexit__(None, None, None)
        cls._client_cache.clear()

# --------------------------
# 自定义限流上下文管理器
# --------------------------
class MCPClientContext:
    def __init__(self, server_name: str, rate_limit: tuple[int, int] = (10, 1)):
        self.server_name = server_name
        self.rate_limit = rate_limit
        self.client: Optional[Client] = None
        self.lock: Optional[asyncio.Lock] = None
        self.limiter: Optional[AsyncLimiter] = None

    async def __aenter__(self):
        """进入上下文：获取单例 Client + 限流 + 加锁"""
        # 1. 获取 Client 及配套工具
        self.client = await MCPClientManager.get_client(self.server_name, self.rate_limit)
        self.lock = MCPClientManager._client_cache[self.server_name][1]
        self.limiter = MCPClientManager._client_cache[self.server_name][2]
        
        # 2. 限流等待（达到速率限制时阻塞）
        await self.limiter.acquire()
        # 3. 协程锁（保证同一时间只有一个协程调用 Client）
        await self.lock.acquire()
        
        return self.client

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """退出上下文：释放锁"""
        if self.lock and self.lock.locked():
            self.lock.release()

# --------------------------
# 示例：多协程调用同一个 MCP Server
# --------------------------
async def call_mcp_tool(server_name: str, tool_name: str, arguments: dict):
    """封装的 MCP 工具调用函数"""
    # 使用自定义上下文管理器（自动处理单例、限流、锁）
    async with MCPClientContext(server_name, rate_limit=(1, 1)) as client:  # 限制 5req/s
        try:
            # 调用工具
            async with client:
                result: CallToolResult = await client.call_tool(
                    name=tool_name,
                    arguments=arguments,
                    raise_on_error=False
                )
                if result.is_error:
                    print(f"协程 {asyncio.current_task().get_name()} 调用失败: {result.content[0].text}")
                else:
                    print(f"协程 {asyncio.current_task().get_name()} 调用成功: {result.data}")
                return result
        except Exception as e:
            print(f"协程 {asyncio.current_task().get_name()} 异常: {str(e)}")
            raise

async def main():
    # 1. 初始化 MCP Server 配置（全局只需要初始化一次）
    MCPClientManager.init_server_config(
        server_name=MCPServerName.DEVIN,
        url=BASE_URL,
        api_key=DEVIN_API_KEY
    )

    # 2. 模拟多协程并发调用同一个 MCP Server
    tasks = []
    for i in range(2):  # 启动8个协程并发调用
        task = asyncio.create_task(
            call_mcp_tool(
                server_name=MCPServerName.DEVIN,
                tool_name="read_wiki_structure",
                arguments={"repoName": "1850298154/HULK"}
            ),
            name=f"Task-{i+1}"
        )
        tasks.append(task)
    
    # 3. 等待所有协程完成
    await asyncio.gather(*tasks)

    # 4. 关闭所有 Client 连接（程序退出前执行）
    await MCPClientManager.close_all()

if __name__ == "__main__":
    asyncio.run(main())