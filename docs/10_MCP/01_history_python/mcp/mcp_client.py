# FastMCP 官方推荐的配置格式
import asyncio
from numpy import isin
import requests
import json
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
        "devin": RemoteMCPServer(
            url=BASE_URL,
            transport="http",
            auth=DEVIN_API_KEY
        )
    }
)

client = Client(config)

async def main():
    async with client:
        # Tools are namespaced by server
        # answer:CallToolResult = await client.call_tool_mcp("read_wiki_structure", {"repoName": "1850298154/HULK"})
        infos:list[mcp.types.Tool] = await client.list_tools()
        print('\ninfos\n\n', infos)
        for info in infos:
            print('\ninfo\n\n', info)
            print('\ninfo.description\n\n', info.description)
            print('\ninfo.inputSchema\n\n', info.inputSchema)
            print('\ninfo.outputSchema\n\n', info.outputSchema)
            print('\ninfo.icons\n\n', info.icons)
            print('\ninfo.annotations\n\n', info.annotations)
            print('\ninfo.meta\n\n', info.meta)
            print('\ninfo.execution\n\n', info.execution)
        answer:CallToolResult = await client.call_tool(
            # "potentially_failing_tool",
            # {"param": "value"},
            name="read_wiki_structure", 
            arguments={"repoName": "1850298154/HULK"},
            raise_on_error=False
        )

        if answer.is_error:
            print(f"Tool failed: {answer.content[0].text}") # CallToolResult(content=[TextContent(type='text', text='Unknown tool: potentially_failing_tool', annotations=None, meta=None)], structured_content=None, meta=None, data=None, is_error=True)
        else:
            print(f"Tool succeeded: {answer.data}")
        print('\nclient.name\n\n',client.name)
        print('\nclient.transport\n\n',client.transport)
        print('\nclient.initialize_result\n\n',client.initialize_result)
        print('\nclient.initialize_result.serverInfo\n\n',client.initialize_result.serverInfo) #  name='DeepWiki' title=None version='2.14.3' websiteUrl=None icons=None
        print('\nanswer\n\n',answer)
        print('\nanswer.content\n\n',answer.content)
        print('\nanswer.structuredContent\n\n',answer.structured_content)
        print('\nanswer.is_error\n\n',answer.is_error)
        print('\nanswer.meta\n\n',answer.meta)
        for e in answer.content:
            if isinstance(e, TextContent):
                print('\nTextContent\n\n', type(e))
            else:
                print('\nOtherContent\n\n',type(e))
            print('\ne\n\n',e)
            print('\ne.type\n\n',e.type)
            print('\ne.text\n\n',e.text)
            print('\ne.text\n\n',e.text)
            print('\ne.text\n\n',e.text)
        

if __name__ == "__main__":
    asyncio.run(main())