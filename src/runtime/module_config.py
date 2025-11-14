# 自定义包名列表（需确保包在 sys.path 中）
CUSTOM_PACKAGES = ["my_package"]  # 替换为你的自定义包名

# 需要打印源码的模块名列表（内置/第三方/自定义均可）
PRINT_SOURCES = [
    "sys",          # 内置模块（测试用）
    "requests",     # 第三方包（需提前 pip install requests）
    "my_package"    # 自定义包
]

# 待执行的代码字符串（可根据需求修改）
CODE_TO_EXEC = """
# 1. 测试内置包 sys
print("✅ 内置包 sys 版本：", sys.version)

# 2. 测试第三方包 requests
response = requests.get("https://www.baidu.com", timeout=5)
print("✅ 第三方包 requests 访问百度状态码：", response.status_code)

# 3. 测试自定义包 my_package（假设包内有 hello 函数）
from my_package import hello
hello()
"""