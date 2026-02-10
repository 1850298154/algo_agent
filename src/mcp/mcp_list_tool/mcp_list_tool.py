# FastMCP 官方推荐的配置格式
import asyncio
from dotenv import load_dotenv
load_dotenv()
from fastmcp import Client 
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
from src.mcp import mcp_enum
import json
from pathlib import Path

async def main():
    for client_item in mcp_enum.client_item_list:
        async with client_item.client:
            infos: list[mcp.types.Tool] = await client_item.client.list_tools()
            print('\ninfos\n\n', infos)

            new_infos = [i.model_dump() for i in infos]
            base_dir = Path(__file__).resolve().parent.parent / mcp_enum.mcp_list_tool_json_dir
            path = base_dir / f"{next(iter(client_item.client.transport.config.mcpServers.keys()))}.json.all.json"
            with open(path, "w", encoding="utf-8") as f:
                json.dump (new_infos, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    asyncio.run(main())