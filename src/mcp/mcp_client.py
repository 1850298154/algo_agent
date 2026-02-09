# FastMCP 官方推荐的配置格式
import asyncio
from numpy import isin
import os
from dotenv import load_dotenv
load_dotenv()

BASE_URL = "https://mcp.devin.ai/mcp" # devin 私有仓库，既可以访问公开，又可以访问私有
DEVIN_API_KEY = os.getenv("DEVIN_API_KEY")
    
from fastmcp import Client 
from mcp.types import (
    ContentBlock,
    TextContent,
    ImageContent,
    AudioContent,
    ResourceLink,
    EmbeddedResource,
    ) 
from fastmcp.client.client import (
    CallToolResult, 
    MCPConfig,
)
from fastmcp.mcp_config import (
    RemoteMCPServer,
    MCPServerTypes,
    MCPConfig,
)
import mcp


from  enum import Enum, unique

@unique
class MCPServerName(Enum):
    DEVIN = "devin"

config = {
    "mcpServers": {
        "devin": {
            "url": BASE_URL,
            "transport": "http",
            "auth": DEVIN_API_KEY
        }
    }
}
config = MCPConfig(
    mcpServers={
        # "devin": RemoteMCPServer(
        MCPServerName.DEVIN: RemoteMCPServer(
            url=BASE_URL,
            transport="http",
            auth=DEVIN_API_KEY
        )
    }
)

client = Client(config)

async def main():
    async with client:
        infos:list[mcp.types.Tool] = await client.list_tools()
        print('\ninfos\n\n', infos)
        answer:CallToolResult = await client.call_tool(
            # "potentially_failing_tool",
            # {"param": "value"},
            name="read_wiki_structure", 
            arguments={"repoName": "1850298154/HULK"},
            raise_on_error=False
        )

        if answer.is_error:
            print(f"Tool failed: {answer.content[0].text}")
        else:
            print(f"Tool succeeded: {answer.data}")

if __name__ == "__main__":
    asyncio.run(main())