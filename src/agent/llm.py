import openai
from openai.types.chat.chat_completion import Choice
from openai.types.chat.chat_completion import ChatCompletion
from src.utils import global_logger, traceable

from secret import model_api_key

client = openai.OpenAI(
    api_key=model_api_key,    
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope SDK的base_url
)

@traceable
def generate_chat_completion(messages: list[dict], tools=None) -> ChatCompletion:
    completion: ChatCompletion = client.chat.completions.create(
        model="qwen-plus",  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        # https://help.aliyun.com/zh/model-studio/models
        messages=messages,
        tools=tools,
    )
    return completion

@traceable
def get_assistant(messages: list[dict]) -> Choice:
    completion: ChatCompletion = generate_chat_completion(messages)
    assistant_output: Choice = completion.choices[0].message
    # assistant_output.finish_reason == "stop" or "length"
    return assistant_output
