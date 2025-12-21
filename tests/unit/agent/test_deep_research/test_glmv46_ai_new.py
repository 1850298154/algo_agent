from src.agent.deep_research_api import user_query

if __name__ == "__main__":
    p_playwright = """
写python代码时候，使用Playwright编写各种操作，并将结果页面截图保存作为你的观察和反馈。如果碰到需要用户登录的界面，需要可以使用持久化上下文以保持登录状态，可以暂停2分钟让用户登录输入账号密码。
"""
    p_glmv46 = r"""
import os
print(os.getcwd())
ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")


from openai import OpenAI
client = OpenAI(
    api_key=ZHIPU_API_KEY,
    base_url="https://open.bigmodel.cn/api/paas/v4/"
)

import base64
def encode_image(image_path: str) -> str:
    # 将图像编码为 base64 字符串
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# 图像理解示例
image_base64 = encode_image("hn_first_news.png")

# 定义函数描述
tools = [
    {
        "type": "function",
        "function": {
            "name": "do_something",
            "description": "工具描述xxx",
            "parameters": {
                "type": "object",
                "properties": {
                    "arg1": {
                        "type": "string",
                        "description": "参数描述xx"
                    }
                },
                "required": ["arg1"]
            }
        }
    }
]

response = client.chat.completions.create(
    model="glm-4.6v",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "请描述这张图片的内容，找到xx内容，同时必须调用do_something函数，传入参数值。"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_base64}"
                    }
                }
            ]
        }
    ],
    tools=tools,
    temperature=0.7
)
print(response.choices[0].message)  # 输出例子： ChatCompletionMessage(content='\n我将调用`xx`工具查询北京的天气，参数`xxx`设为"yyy"。\n', role='assistant', tool_calls=[ChatCompletionMessageFunctionToolCall(id='call_-8054084952333305293', function=Function(arguments='{"xxx": "yyy"}', name='xx'), type='function', index=0)], reasoning_content='用户要求我查看图片xxxx，同时必须调xxx函数工具do something。首先，我需要描述图片内容。图片显示的是...。\n\n接下来，根据用户要求，我需要调用xxx函数do something。函数需要xxx参数，这里应该是“xx”。所以我会调用这个函数，然后结合图片描述和xx信息来回答。')
"""
    p_concat = """
根据以上提示，请你作为一个使用GLM-V4.6模型的智能助手，帮助用户完成他们的查询任务。请确保你理解用户的需求，并根据提示中的信息提供准确和有用的回答。用户问题：
    """
    p_user = "去 Hacker News 首页，找到排名前三的 AI 相关新闻，并把标题和链接整理给我。"
    user_input = p_playwright + p_glmv46 + p_concat + p_user
    from src.runtime.subthread_python_executor import work_dir
    work_dir = './wsm/5glm/1'
    user_query(user_input)