from src.agent import deep_research_api
from src.agent.msg import msg_mem
from src.agent_swarm import summon


import asyncio
import pprint
import json
from typing import List, Tuple, Optional, Any, AsyncGenerator

from src.agent import system_prompt
from src.agent import tool 
from src.utils.log_decorator import global_logger 
from src.agent.msg import msg_ctr 
from src.agent.msg import msg_mem 

from src.ui.cache_unchange import (
    cache_msg_genor
)

async def gen_msg(message_mem) -> AsyncGenerator[msg_mem.MessageMemory, None]:
    genor = await cache_msg_genor.get_cached_msg_genor(message_mem)
    # 确保是同一个genor
    print(f"genor id: {id(genor)}")
    async for ret_message_mem in genor:
        yield ret_message_mem
        
    json_str = json.dumps(ret_message_mem, default=lambda o: o.model_dump())
    pure_python_data = json.loads(json_str)
    global_logger.info(f"一共{len(ret_message_mem.messages)}条对话：\n\n {pprint.pformat(pure_python_data)}\n\n")
    pass
