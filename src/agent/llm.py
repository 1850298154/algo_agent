from openai import OpenAI

from src.utils import global_logger, traceable

from .secret import model_api_key

client = OpenAI(
    api_key=model_api_key,    
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope SDK的base_url
)

@traceable
def generate_chat_completion(messages, tools=None):
    completion = client.chat.completions.create(
        model="qwen-plus",  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        # https://help.aliyun.com/zh/model-studio/models
        messages=messages,
        tools=tools,
    )
    return completion

@traceable
def get_assistant_output(completion):
    assistant_output = completion.choices[0].message
    return assistant_output