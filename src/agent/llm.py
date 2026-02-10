from openai.types.chat.chat_completion import (
    ChatCompletionMessage,
    ChatCompletion,
    Choice,
    CompletionUsage
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
from openai.types.chat.chat_completion_tool_union_param import (
    ChatCompletionFunctionToolParam, 
    ChatCompletionCustomToolParam,
    ChatCompletionToolUnionParam,
)
from openai.types.chat.chat_completion_message_function_tool_call_param import (
    ChatCompletionMessageFunctionToolCallParam,
)

from typing import cast

from src.agent.msg import msg_mem
from src.utils.log_decorator import global_logger, traceable
from src.agent.llm_client import glm as chat_llm

@traceable
def _generate_chat_completion(message_mem: msg_mem.MessageMemory, tools_schema_list=None) -> ChatCompletion:
    completion: ChatCompletion = chat_llm.client.chat.completions.create(
        messages=message_mem.messages,
        model=chat_llm.default_glm_model,
        tools=tools_schema_list,
        parallel_tool_calls=True,
    )
    return completion


def _extract_assistant_output_from_chat(message_mem: msg_mem.MessageMemory, tools_schema_list=None) -> ChatCompletionMessage:
    completion: ChatCompletion = _generate_chat_completion(message_mem, tools_schema_list)
    choice: Choice = completion.choices[0]
    assistant_message: ChatCompletionMessage = choice.message
    
    message_mem.add_message(assistant_message, choice.finish_reason)
    return assistant_message


def _generate_assistant_output_append(message_mem: msg_mem.MessageMemory, tools_schema_list=None) -> ChatCompletionMessage:
    assistant_message: ChatCompletionMessage = _extract_assistant_output_from_chat(message_mem, tools_schema_list)

    return assistant_message


def run_llm_once(message_mem: msg_mem.MessageMemory, tools_schema_list: list) -> ChatCompletionMessage:
    """调用 LLM 生成一次 assistant 输出"""
    return _generate_assistant_output_append(message_mem, tools_schema_list)

