from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()


QWEN_API_KEY = os.getenv("QWEN_API_KEY")

client = OpenAI(
    api_key=QWEN_API_KEY,    
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope SDK的base_url
)

qwen_plus_model="qwen-plus"

"""
模型列表：
https://help.aliyun.com/zh/model-studio/getting-started/models
https://help.aliyun.com/zh/model-studio/models

api 说明： 
https://zhuanlan.zhihu.com/p/692336625
"""

if __name__ == "__main__":
    response = client.chat.completions.create(
        model=qwen_plus_model,
        messages=[
            {   "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                # "content": "Explain to me how AI works."
                "content": "10个字内简单回答什么是ai"
            }
        ]
    )

    print(response.choices[0].message)