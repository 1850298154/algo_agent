import openai
from openai.types.chat.chat_completion import ChatCompletionMessage
from openai.types.chat.chat_completion import ChatCompletion
from src.utils import global_logger, traceable

from secret import model_api_key

client = openai.OpenAI(
    api_key=model_api_key,    
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope SDK的base_url
)

@traceable
def _generate_chat_completion(messages: list[dict], tools_schema_list=None) -> ChatCompletion:
    completion: ChatCompletion = client.chat.completions.create(
        model="qwen-plus",  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        # https://help.aliyun.com/zh/model-studio/models
        # api: https://help.aliyun.com/zh/model-studio/qwen-api-reference
        messages=messages, # api 说明 https://zhuanlan.zhihu.com/p/692336625
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

