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
from typing import List, Tuple, Optional, Any

from src.utils import global_logger, traceable

from src.agent import llm
from src.agent.action import action_processer 
from src.agent import memory 
from src.agent import tool 

async def user_query(sys_prompt: str, user_prompt: str, tool_class_list: list[tool.base_tool.BaseTool]) -> None:
    global_logger.info(f"用户输入： {user_prompt}\n\n")

    messages: list[ChatCompletionMessageParam] = memory.init_messages_with_system_prompt(sys_prompt, user_prompt)
    tools_schema_list = tool.gen_des_schema.get_tools_schema(tool_class_list)

    # 模型的第一轮调用
    assist_msg: ChatCompletionMessage = llm.run_llm_once(messages, tools_schema_list)
    assist_msg.content = assist_msg.content or "" # 避免 content 是 None 导致后续处理出错

    if (assist_msg.tool_calls and assist_msg.function_call):
        global_logger.info(f"无需调用工具，我可以直接回复：\n\n{assist_msg.content}")
        return

    # 如果需要调用工具，则进行模型的多轮调用，直到模型判断无需调用工具
    while (assist_msg.tool_calls or assist_msg.function_call):
        global_logger.info(f"""第{len(messages)}轮大模型输出信息： 
        \n\nassistant_output.content::   \n\n{pprint.pformat(assist_msg.content)}
        \n\nassistant_output.tool_calls::\n\n{pprint.pformat([toolcall.model_dump() for toolcall in assist_msg.tool_calls]   if assist_msg.tool_calls else [])}\n""")

        await action_processer.process_tool_calls(messages, assist_msg)
        # 让模型基于工具输出继续生成下一轮输出
        assist_msg = llm.run_llm_once(messages, tools_schema_list)
        assist_msg.content = assist_msg.content or "" # 避免 content 是 None 导致后续处理出错
        
    global_logger.info(f"大模型的最终答案：\n\n{assist_msg.content}")
    
    return messages
