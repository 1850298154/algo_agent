from src.agent import deep_research_api
from src.agent.msg import msg_mem
from src.agent_swarm import summon


import asyncio
import pprint
import json
from src.agent import system_prompt
from src.agent import tool 
from src.utils.log_decorator import global_logger 
from src.agent.msg import msg_ctr 
from src.agent.msg import msg_mem 


async def gen_msg(message_mem):
    gen = summon.summon_agent_generator(
            message_mem            = message_mem,
            tool_class_list     = [tool.python_tool.ExecutePythonCodeTool],
            # tool_class_list     = [],
            # mcp_tool_name_list  = mcp_enum.mcp_list_tool_name_list,
            mcp_tool_name_list  = [],
    )
    async for ret_message_mem in gen:
        yield ret_message_mem
        
    json_str = json.dumps(ret_message_mem, default=lambda o: o.model_dump())
    pure_python_data = json.loads(json_str)
    global_logger.info(f"一共{len(ret_message_mem.messages)}条对话：\n\n {pprint.pformat(ret_message_mem)}\n\n")
    pass
