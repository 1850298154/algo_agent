from src.agent import deep_research_api
from src.agent.msg import msg_mem
from src.agent_swarm import summon

from typing import List, Tuple, Optional, Any, AsyncGenerator
import streamlit as st
import asyncio
import pprint
import json
from src.agent import system_prompt
from src.agent.tool.sandbox import python_tool 
from src.utils.log_decorator import global_logger 
from src.agent.msg import msg_ctr 
from src.agent.msg import msg_mem 
from src.mcp import mcp_enum 

# @st.cache_data()
async def get_cached_msg_genor(message_mem) -> AsyncGenerator[msg_mem.MessageMemory, None]:
    genor = summon.summon_agent_generator(
            message_mem            = message_mem,
            tool_class_list     = [python_tool.ExecutePythonCodeTool],
            # tool_class_list     = [],
            mcp_tool_name_list  = mcp_enum.mcp_list_tool_name_list,
        #     mcp_tool_name_list  = [],
    )
    return genor