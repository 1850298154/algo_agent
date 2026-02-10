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


from typing import List, Tuple, Optional, Any

from src.utils.log_decorator import global_logger, traceable
from src.agent.action import action_call_tool
from src.agent.action import action_type
from src.agent.msg import msg_mem


def collect_call_descriptors(assist_msg: ChatCompletionMessage) -> List[action_type.CallDescriptor]:
    """从 assist_msg 中收集需要并发执行的调用描述 (kind, name, arguments, tool_call_id)"""
    descriptors: List[action_type.CallDescriptor] = []
    if assist_msg.function_call is not None:
        function_call: FunctionCall = assist_msg.function_call
        descriptors.append(
            action_type.CallDescriptor(
                kind=action_type.CallKind.FUNCTION,
                name=function_call.name,
                arguments=function_call.arguments,
                tool_call_id=None,
            )
        )

    if assist_msg.tool_calls:
        tool_calls_list: List[ChatCompletionMessageFunctionToolCall] = [
            tc
            for tc in (assist_msg.tool_calls or [])
            if isinstance(tc, ChatCompletionMessageFunctionToolCall)
        ]
        for tc in tool_calls_list:
            descriptors.append(
                action_type.CallDescriptor(
                    kind=action_type.CallKind.TOOL,
                    name=tc.function.name,
                    arguments=tc.function.arguments,
                    tool_call_id=tc.id,
                )
            )
    return descriptors


async def execute_calls_concurrently_async(
    call_descriptors: List[action_type.CallDescriptor],
) -> List[str]:
    """并发执行所有调用并返回结果列表，顺序与 call_descriptors 对应"""
    tasks = [
        asyncio.create_task(
            action_call_tool.execute_single_call_async(cd.name, cd.arguments)
        )
        for cd in call_descriptors
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results


def append_results_to_messages(
    messages: msg_mem.MessageMemory,
    call_descriptors: List[action_type.CallDescriptor],
    results: List[Any],
) -> None:
    """将每个调用的输出按顺序追加到 messages"""
    for cd, result in zip(call_descriptors, results):
        if isinstance(result, Exception):
            func_output = f"工具执行异常: {result}"
        else:
            func_output = result

        if cd.kind == action_type.CallKind.FUNCTION:
            messages.add_message(
                ChatCompletionFunctionMessageParam(
                    content=func_output,
                    role=cd.kind.value,
                    name=cd.name,
                )
            )
        else:  # tool
            messages.add_message(
                ChatCompletionToolMessageParam(
                    content=func_output,
                    role=cd.kind.value,
                    tool_call_id=cd.tool_call_id,
                )
            )
