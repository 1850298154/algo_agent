from src.agent.deep_research_api import run_agent_generator

if __name__ == "__main__":
    p_playwright = """
你可以调用 执行 python 代码的工具，使用 Playwright 编写各种操作，并将结果页面截图保存下来png，然后调用 model="glm-4.6v" 视觉大语言模型观察，进一步推到怎么做。比如：碰到需要京东电商网页要求用户登录的界面，通过"glm-4.6v"观察 Playwright 存储的图片，遇到访问限制、反爬虫机制、或者需要登录、或者需要验证码验证、或者需要滑块验证等等验证，请编写代码，使用人机协作的方式，不仅要弹出浏览器让用户登录，还需要弹出弹出一个独立的桌面窗口，提示用户在浏览器中完成登录操作，登录完成后用户点击“我已登录，继续”按钮，程序才继续执行后续操作（注意需要 print 打印用户的选择， 方便自己调用 python exec 后拿到终端输出，可以判断用户的行为）。确保该桌面窗口不会因网页刷新而丢失，并且能够跨平台运行（Windows / macOS / Linux）。完成登录确认后，继续执行后续的网页操作，例如搜索商品并截图保存。 如下是参考代码：
"""
    p_hitl = r"""
from playwright.async_api import async_playwright, Page
import asyncio
import tkinter as tk
from tkinter import messagebox


class LoginConfirmDialog:
    # 一个独立桌面窗口（不注入网页），用户点“我已登录”才放行。
    # - 跨平台：Windows / macOS / Linux（Python 自带 tkinter）
    # - 不会因网页刷新而丢失
    def __init__(self, title: str = "Agent Human-in-the-Loop"):
        self._title = title
        self._confirmed = False

    def show(self, tip: str = "请在浏览器中完成登录（含验证码等），完成后点击“我已登录，继续”。") -> bool:
        root = tk.Tk()
        root.title(self._title)
        root.geometry("520x180")
        root.resizable(False, False)

        # 置顶（尽量）
        try:
            root.attributes("-topmost", True)
        except Exception:
            pass

        frame = tk.Frame(root, padx=16, pady=16)
        frame.pack(fill="both", expand=True)

        lbl = tk.Label(frame, text=tip, justify="left", wraplength=480)
        lbl.pack(anchor="w")

        btn_row = tk.Frame(frame, pady=18)
        btn_row.pack(fill="x")

        def on_confirm():
            self._confirmed = True
            root.destroy()

        def on_cancel():
            self._confirmed = False
            root.destroy()

        confirm_btn = tk.Button(btn_row, text="我已登录，继续", width=18, command=on_confirm)
        confirm_btn.pack(side="left")

        cancel_btn = tk.Button(btn_row, text="取消/退出", width=12, command=on_cancel)
        cancel_btn.pack(side="left", padx=10)

        root.protocol("WM_DELETE_WINDOW", on_cancel)
        root.mainloop()
        return self._confirmed


async def wait_for_user_confirm_desktop() -> bool:
    # tkinter 是阻塞的，用线程跑，避免卡住 asyncio
    dialog = LoginConfirmDialog()
    return await asyncio.to_thread(dialog.show)


async def ensure_login(page: Page) -> None:
    print("👉 请在浏览器中完成登录；将弹出桌面窗口等待你确认。")
    ok = await wait_for_user_confirm_desktop()
    if not ok:
        raise RuntimeError("User cancelled login confirmation")

    # 可选：确认后给一点缓冲
    await page.wait_for_timeout(800)


async def main():
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            "jd_profile",
            headless=False,
            args=["--disable-blink-features=AutomationControlled"],
        )

        page = await context.new_page()
        await page.goto("https://www.jd.com", wait_until="domcontentloaded")

        # 1) 登录（人机协作确认，不注入网页）
        await ensure_login(page)
        print("✅ 用户确认登录完成，进入后续流程")

        # 2) 后续操作（示例：搜索并截图）
        await page.goto("https://search.jd.com/Search?keyword=RTX%204090", wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        await page.screenshot(path="jd_4090.png", full_page=True)

        await context.close()


if __name__ == "__main__":
    asyncio.run(main())
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
根据以上提示，请你作为一个使用 GLM-V4.6 视觉大语言模型 的智能助手，帮助用户完成他们的查询任务。请确保你理解用户的需求，并根据提示中的信息提供准确和有用的回答。记得，得出答案的时候，需要告诉我是从哪个网页界面，把存下来图片的连接记得print或者告诉我。用户问题：
    """
    # p_user = "去 Hacker News 首页，找到排名前三的 AI 相关新闻，并把标题和链接整理给我。"
    p_user = "帮我查一下京东上 RTX 4090 显卡现在的最低价格是多少。"
    
    user_input = p_playwright + p_hitl + p_glmv46 + p_concat + p_user
    from src.runtime import subthread_python_executor
    subthread_python_executor.work_dir = './wsm/5glm/5jd'
    subthread_python_executor.work_dir = './wsm/5glm/5-2jd'
    run_agent_generator(user_input)