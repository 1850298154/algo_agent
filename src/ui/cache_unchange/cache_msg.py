from openai.types.chat.chat_completion_message_param import (
    ChatCompletionDeveloperMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionAssistantMessageParam,
    ChatCompletionToolMessageParam,
    ChatCompletionFunctionMessageParam,    
    ChatCompletionMessageParam,
) 
import streamlit as st
from pathlib import Path

import asyncio
import pprint
import json
from src.agent import system_prompt
from src.agent import tool 
from src.utils.log_decorator import global_logger 
from src.agent.msg import msg_ctr 
from src.agent.msg import msg_mem 
from src.mcp import mcp_enum 
from src.agent import deep_research_api
from src.agent.msg import msg_mem
from src.agent_swarm import summon

# @st.cache_data  
def get_cached_msg(user_prompt ):
    message_mem: msg_mem.MessageMemory = msg_mem.init_messages_with_system_prompt(
        agent_name_id="test_simple_code_agent",
        system_prompt=system_prompt.obedient_system_prompt,
        user_prompt=user_prompt,
        msg_ctr_config=msg_ctr.MessageControlConfig(max_rounds=5)
    )
    return message_mem