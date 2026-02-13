from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()


ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")

client = OpenAI(
    api_key=ZHIPU_API_KEY,
    base_url="https://open.bigmodel.cn/api/paas/v4/"
)
glm_4_6_v_model = "glm-4.6v"
glm_4_6_model = "glm-4.6"
glm_4_7_flashx_model = "glm-4.7-flashx"
glm_4_7_model = "glm-4.7"
glm_5_model = "glm-5"

default_glm_model = glm_5_model
"""
模型编码列表：
https://docs.bigmodel.cn/cn/guide/start/concept-param

模型能力介绍：
https://docs.bigmodel.cn/cn/guide/start/model-overview
"""

if __name__ == "__main__":
    response = client.chat.completions.create(
        # model=glm_4_7_model,
        model=glm_5_model,
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