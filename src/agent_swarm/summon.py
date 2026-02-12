from typing import List, Tuple, Optional, Any, AsyncGenerator

from src.agent import deep_research_api
from src.agent.msg import msg_mem


async def summon_agent_generator(
    message_mem: deep_research_api.msg_mem.MessageMemory,
    tool_class_list: list = [],
    mcp_tool_name_list: list = [],
) -> AsyncGenerator[msg_mem.MessageMemory, None]:
    genor = deep_research_api.run_agent_generator(
        message_mem=message_mem,
        tool_class_list=tool_class_list,
        mcp_tool_name_list=mcp_tool_name_list,
    )
    try:
        async for ret_message_mem in genor: 
            yield ret_message_mem
    finally:
        await genor.aclose()  # 确保生成器被正确关闭，释放资源，不然后又 cancel 异常
