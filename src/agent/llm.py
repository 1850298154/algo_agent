from openai.types.chat.chat_completion import ChatCompletionMessage
from openai.types.chat.chat_completion import ChatCompletion
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

from src.utils import global_logger, traceable
from src.agent.llm_client import glm

@traceable
def _generate_chat_completion(messages: list[ChatCompletionMessageParam], tools_schema_list=None) -> ChatCompletion:
    completion: ChatCompletion = glm.client.chat.completions.create(
        messages=messages,
        model=glm.glm_4_7_model,
        tools=tools_schema_list,
        parallel_tool_calls=True,
    )
    return completion


def _extract_assistant_output_from_chat(messages: list[ChatCompletionMessageParam], tools_schema_list=None) -> ChatCompletionMessage:
    completion: ChatCompletion = _generate_chat_completion(messages, tools_schema_list)
    assistant_output: ChatCompletionMessage = completion.choices[0].message
    # assistant_output.finish_reason == "stop" or "length"
    return assistant_output


def generate_assistant_output_append(messages: list[ChatCompletionMessageParam], tools_schema_list=None) -> ChatCompletionMessage:
    global_logger.info("-" * 60)
    assistant_message: ChatCompletionMessage = _extract_assistant_output_from_chat(messages, tools_schema_list)
    
    if assistant_message.content is None:
        assistant_message.content = ""
    messages.append(cast(ChatCompletionMessageParam, assistant_message))
    return assistant_message


