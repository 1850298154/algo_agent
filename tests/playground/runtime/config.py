CODE_TO_EXEC = """print("===== 执行代码开始 =====")
# 导入所需模块
import json
import os
import requests
import sys

def print_python_info():
    # 打印 Python 版本信息
    print("=" * 40)
    print("Python 版本信息：")
    print(f"完整版本号：{sys.version}")
    print(f"主版本号：{sys.version_info.major}")
    print(f"次版本号：{sys.version_info.minor}")
    print(f"微版本号：{sys.version_info.micro}")
    print(f"发布级别：{sys.version_info.releaselevel}")
    print(f"序列号：{sys.version_info.serial}")
    
    print("\n" + "=" * 40)
    print("Python 路径信息：")
    # 打印 Python 可执行文件路径（关键路径）
    print(f"Python 可执行文件路径：{sys.executable}")
    # 打印 Python 安装目录（通过可执行文件路径推导）
    import os
    python_install_dir = os.path.dirname(os.path.dirname(sys.executable))
    print(f"Python 安装目录：{python_install_dir}")
    # 打印当前 Python 搜索路径（sys.path）
    print(f"\nPython 模块搜索路径（sys.path）：")
    for i, path in enumerate(sys.path, 1):
        print(f"  {i:2d}. {path}")
    print("=" * 40)

print_python_info()


# ====================== 1. 标准库 os 函数示例 ======================
print("\\n✅ 【os 模块】当前工作目录：", os.getcwd())
print("✅ 【os 模块】当前目录下的文件：", os.listdir("."))
print("✅ 【os 模块】系统名称：", os.name)  # posix（Linux/Mac）或 nt（Windows）

# ====================== 2. 标准库 json 函数示例 ======================
# json.dumps：字典转 JSON 字符串
user_info = {"name": "张三", "age": 25, "is_student": False}
json_str = json.dumps(user_info, ensure_ascii=False, indent=2)
print("\\n✅ 【json 模块】字典转 JSON：\\n", json_str)

# json.loads：JSON 字符串转字典
json_dict = json.loads(json_str)
print("✅ 【json 模块】JSON 转字典：", json_dict["name"])

# ====================== 3. 第三方包 requests 函数示例 ======================
# requests.get：GET 请求
response = requests.get("https://www.baidu.com", timeout=5)
print("\\n✅ 【requests 模块】百度首页状态码：", response.status_code)
print("✅ 【requests 模块】响应编码：", response.encoding)

# requests.post：POST 请求（模拟表单提交）
post_data = {"username": "test", "password": "123456"}
post_response = requests.post("https://httpbin.org/post", data=post_data, timeout=5)
print("✅ 【requests 模块】POST 响应 JSON：\\n", post_response.json()["form"])

# ====================== 4. 自定义包 my_package 函数示例 ======================
from my_package import hello, add  # 假设新增了 add 函数
hello()
print("✅ 【自定义模块】10 + 20 =", add(10, 20))
"""

# 自定义包名列表（需确保包在 sys.path 中）
CUSTOM_PACKAGES = ["my_package"]  # 替换为你的自定义包名

# 需要打印源码的模块名列表（新增标准库模块 os、json）
PRINT_SOURCES = [
    "sys",          # 内置模块（C 实现）
    "os",           # 标准库模块（Python 实现）
    "json",         # 标准库模块（Python 实现）
    "requests",     # 第三方包
    "my_package"    # 自定义包
]

