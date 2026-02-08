
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

from dataclasses import dataclass
from typing import List, Tuple, Optional, Any
from src.agent.action import action_dispatcher 

async def process_tool_calls(messages: List[ChatCompletionMessageParam], assist_msg: ChatCompletionMessage):
    """
    封装：1) collect_call_descriptors 2) execute_calls_concurrently_async 3) append_results_to_messages
    返回 (call_descriptors, results)
    """
    # 1. 收集所有需要并发执行的调用描述
    call_descriptors = action_dispatcher.collect_call_descriptors(assist_msg)
    # 2. 并发执行所有调用（协程）
    results = await action_dispatcher.execute_calls_concurrently_async(call_descriptors)
    # 3. 将每个调用的输出按顺序追加到 messages
    action_dispatcher.append_results_to_messages(messages, call_descriptors, results)
    return call_descriptors, results
