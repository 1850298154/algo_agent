
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

import asyncio

from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple, Optional, Any

from src.utils import global_logger, traceable
from src.agent.action import action_call_tool 

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

async def execute_calls_concurrently_async(call_descriptors: List[CallDescriptor]) -> List[str]:
    """并发执行所有调用并返回结果列表，顺序与 call_descriptors 对应"""
    tasks = [asyncio.create_task(action_call_tool.execute_single_call_async(cd.name, cd.arguments)) for cd in call_descriptors]
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

