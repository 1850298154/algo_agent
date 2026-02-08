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
from src.agent import action 
from src.agent import memory 
from src.agent import tool 

from enum import Enum
from dataclasses import dataclass

class CallKind(Enum):
    FUNCTION = "function"
    TOOL = "tool"

@dataclass
class CallDescriptor:
    kind: CallKind
    name: str
    arguments: Optional[Any]
    tool_call_id: Optional[str] = None
    

def collect_call_descriptors(assist_msg: ChatCompletionMessage) -> List[CallDescriptor]:
    """从 assist_msg 中收集需要并发执行的调用描述 (kind, name, arguments, tool_call_id)"""
    descriptors: List[CallDescriptor] = []
    if assist_msg.function_call is not None:
        function_call: FunctionCall = assist_msg.function_call
        descriptors.append(CallDescriptor(
            kind=CallKind.FUNCTION,
            name=function_call.name,
            arguments=function_call.arguments,
            tool_call_id=None
        ))

    if assist_msg.tool_calls:
        tool_calls_list: List[ChatCompletionMessageFunctionToolCall] = [
            tc for tc in (assist_msg.tool_calls or [])
            if isinstance(tc, ChatCompletionMessageFunctionToolCall)
        ]
        for tc in tool_calls_list:
            descriptors.append(CallDescriptor(
                kind=CallKind.TOOL,
                name=tc.function.name,
                arguments=tc.function.arguments,
                tool_call_id=tc.id
            ))
    return descriptors

async def _execute_single_call(name: str, arguments: Any) -> str:
    """执行一次工具或 function 调用（需要为协程）"""
    return action.call_tools_safely(name, arguments)

async def execute_calls_concurrently(call_descriptors: List[CallDescriptor]) -> List[str]:
    """并发执行所有调用并返回结果列表，顺序与 call_descriptors 对应"""
    tasks = [asyncio.create_task(_execute_single_call(cd.name, cd.arguments)) for cd in call_descriptors]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results

def append_results_to_messages(messages: List[ChatCompletionMessageParam],
                               call_descriptors: List[CallDescriptor],
                               results: List[Any]) -> None:
    """将每个调用的输出按顺序追加到 messages"""
    for cd, result in zip(call_descriptors, results):
        if isinstance(result, Exception):
            func_output = f"工具执行异常: {result}"
        else:
            func_output = result

        if cd.kind == CallKind.FUNCTION:
            global_logger.info(f"工具 function call 输出信息： {func_output}\n")
            global_logger.info("-" * 60)
            messages.append(
                ChatCompletionFunctionMessageParam(
                    content=func_output,
                    name=cd.name,
                    role=cd.kind.value,
                )
            )
        else:  # tool
            global_logger.info(f"工具 tool call 输出信息： {func_output}\n")
            global_logger.info("-" * 60)
            messages.append(
                ChatCompletionToolMessageParam(
                    content=func_output,
                    role=cd.kind.value,
                    tool_call_id=cd.tool_call_id,
                )
            )

async def user_query(sys_prompt: str, user_prompt: str, tool_class_list: list[tool.base_tool.BaseTool]) -> None:
    user_hint = "用户输入："
    global_logger.info(f"{user_hint} ： {user_prompt}\n\n")

    messages: list[ChatCompletionMessageParam] = memory.init_messages_with_system_prompt(user_prompt, sys_prompt)
    tools_schema_list = tool.gen_des_schema.get_tools_schema(tool_class_list)

    # 模型的第一轮调用（异步）
    assist_msg: ChatCompletionMessage = llm.run_llm_once(messages, tools_schema_list)
    if (assist_msg.tool_calls is not None 
        and assist_msg.function_call is not None):
        global_logger.info(f"无需调用工具，我可以直接回复：{assist_msg.content}")
        return

    # 如果需要调用工具，则进行模型的多轮调用，直到模型判断无需调用工具
    while (assist_msg.tool_calls is not None 
            or assist_msg.function_call is not None):
        call_descriptors = collect_call_descriptors(assist_msg)

        # 并发执行所有调用（协程）
        results = await execute_calls_concurrently(call_descriptors)

        # 将每个调用的输出按顺序追加到 messages
        append_results_to_messages(messages, call_descriptors, results)

        # 让模型基于工具输出继续生成（异步）
        assist_msg = llm.run_llm_once(messages, tools_schema_list)
        if assist_msg.content is None:
            assist_msg.content = ""
        global_logger.info(
            f"""第{len(messages) // 2}轮大模型输出信息： 
\n\nassistant_output.content:: \n\n {pprint.pformat(assist_msg.content)}
\n\nassistant_output.tool_calls::\n\n 
{pprint.pformat(
    [toolcall.model_dump() for toolcall in assist_msg.tool_calls]   
    if assist_msg.tool_calls 
    else [])
}\n"""
        )
    global_logger.info(f"最终答案： {assist_msg.content}")
    
    return messages