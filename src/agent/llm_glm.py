import openai
from openai.types.chat.chat_completion import ChatCompletionMessage
from openai.types.chat.chat_completion import ChatCompletion
from src.utils import global_logger, traceable

from dotenv import load_dotenv
import os
load_dotenv()

ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")


from openai import OpenAI
client = OpenAI(
    api_key=ZHIPU_API_KEY,
    base_url="https://open.bigmodel.cn/api/paas/v4/"
)

@traceable
def _generate_chat_completion(messages: list[dict], tools_schema_list=None) -> ChatCompletion:
    completion: ChatCompletion = client.chat.completions.create(
        model="glm-4.6",  
# 模型列表：https://docs.bigmodel.cn/cn/guide/develop/openai/introduction#%E5%9F%BA%E7%A1%80%E9%85%8D%E7%BD%AE | OpenAI API 兼容 - 智谱AI开放文档
# https://docs.bigmodel.cn/cn/guide/start/latest-glm-4.6v | 最新模型：GLM-4.6V - 智谱AI开放文档1
        messages=messages,
        tools=tools_schema_list,
        function_call=None,
        parallel_tool_calls=True,
    )
    return completion


def _extract_assistant_output_from_chat(messages: list[dict], tools_schema_list=None) -> ChatCompletionMessage:
    completion: ChatCompletion = _generate_chat_completion(messages, tools_schema_list)
    assistant_output: ChatCompletionMessage = completion.choices[0].message
    # assistant_output.finish_reason == "stop" or "length"
    return assistant_output


def generate_assistant_output_append(messages: list[dict], tools_schema_list=None) -> ChatCompletionMessage:
    global_logger.info("-" * 60)
    assistant_output: ChatCompletionMessage = _extract_assistant_output_from_chat(messages, tools_schema_list)
    
    if assistant_output.content is None:
        assistant_output.content = ""
    messages.append(assistant_output)
    return assistant_output


def has_tool_call(assistant_output: ChatCompletionMessage) -> bool:
    return assistant_output.tool_calls is not None


def has_function_call(assistant_output: ChatCompletionMessage) -> bool:
    return assistant_output.function_call is not None

