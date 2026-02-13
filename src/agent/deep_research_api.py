from openai.types.chat.chat_completion import (
    ChatCompletionMessage,
)
from openai.types.chat.chat_completion_message import (
    FunctionCall,
    ChatCompletionMessageToolCallUnion,
)
from openai.types.chat.chat_completion_message_function_tool_call import (
    ChatCompletionMessageFunctionToolCall,
)
from openai.types.chat.chat_completion_message_param import (
    ChatCompletionDeveloperMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionAssistantMessageParam,
    ChatCompletionToolMessageParam,
    ChatCompletionFunctionMessageParam,    
    ChatCompletionMessageParam,
) 

import pprint
import asyncio
from typing import List, Tuple, Optional, Any, AsyncGenerator

from src.utils.log_decorator import global_logger, traceable

from src.agent import llm
from src.agent.action import action_processer 
from src.agent.msg import msg_mem 
from src.agent.msg import msg_ctr 
from src.agent.tool import (
    tool_gen_descrip,
    tool_base
)
from src.mcp import mcp_2_tool 


async def run_agent_generator(
    message_mem: msg_mem.MessageMemory,
    tool_class_list: list[tool_base.ToolBase] = [],
    mcp_tool_name_list: list[str] = [],
    ) -> AsyncGenerator[msg_mem.MessageMemory, None]:

    tools_schema_list = tool_gen_descrip.get_tools_schema(tool_class_list)
    mcp_schema_list = mcp_2_tool.filter_schema_for_register(mcp_tool_name_list)

    # 模型的第一轮调用
    assist_msg: ChatCompletionMessage = llm.run_llm_once(message_mem, tools_schema_list+mcp_schema_list)
    yield message_mem

    # 如果需要调用工具，则进行模型的多轮调用，直到模型判断无需调用工具
    while (assist_msg.tool_calls or assist_msg.function_call) and message_mem.need_msg_stop_control(message_mem.msg_ctr_cfg) == False:
        # 1. 处理工具调用（包括函数调用），并将工具调用结果追加到消息中
        yield await action_processer.process_tool_calls(message_mem, assist_msg)
        
        # 2. 让模型基于工具输出继续生成下一轮输出
        assist_msg = llm.run_llm_once(message_mem, tools_schema_list+mcp_schema_list)
    yield message_mem
