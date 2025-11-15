# import sys

# # import os.path
# # # ---------------------- 写法1：import os.path ----------------------
# # print("=== 写法1：import os.path ===")
# # # 验证变量绑定：os 和 os.path 都能直接访问（import 语句自动绑定）
# # print(f"能否直接访问 os：{ 'os' in globals() }")  # True（顶层包被绑定到变量 os）
# # print(f"能否直接访问 os.path：{ 'os.path' in globals() }")  # False（仅绑定顶层包，子模块不单独绑定）
# # print(f"os.path 是否加载：{'os.path' in sys.modules}")  # False（子模块未加载）
# # print(f"os.path 的类型：{type(os.path)}")  # <class 'module'>（子模块已加载）

# # # 验证加载状态
# # print(f"os.path 的类型：{type(os.path)}")  # <class 'module'>（延迟加载）
# # print(f"os 是否加载：{'os' in sys.modules}")  # True
# # print(f"os.path 是否加载：{'os.path' in sys.modules}")  # True（导入时已加载）
# """
# === 写法1：import os.path ===
# 能否直接访问 os：True
# 能否直接访问 os.path：False
# os.path 是否加载：True
# os.path 的类型：<class 'module'>
# os.path 的类型：<class 'module'>
# os 是否加载：True
# os.path 是否加载：True
# """

# # import os
# # # ---------------------- 写法2：import os ----------------------
# # print("\n=== 写法2：import os ===")
# # # 重新启动 Python 执行（避免缓存影响），仅执行 import os
# # print(f"能否直接访问 os：{ 'os' in globals() }")  # True（顶层包被绑定）
# # print(f"能否直接访问 os.path：{ 'os.path' in globals() }")  # False（仅绑定顶层包，子模块不单独绑定）
# # print(f"os.path 是否加载：{'os.path' in sys.modules}")  # False（子模块未加载）
# # print(f"os.path 的类型：{type(os.path)}")  # <class 'module'>（子模块已加载）

# # # 访问 os.path 时才加载
# # print(f"os.path 的类型：{type(os.path)}")  # <class 'module'>（延迟加载）
# # print(f"os 是否加载：{'os' in sys.modules}")  # True
# # print(f"os.path 是否加载：{'os.path' in sys.modules}")  # True（访问后加载）
# """
# === 写法2：import os ===
# 能否直接访问 os：True
# 能否直接访问 os.path：False
# os.path 是否加载：True
# os.path 的类型：<class 'module'>
# os.path 的类型：<class 'module'>
# os 是否加载：True
# os.path 是否加载：True
# """

# import sys
# # import os.path
# # # ---------------------- 写法1：import os.path ----------------------
# # print("=== 写法1：import os.path ===")
# # # 验证变量绑定：os 和 os.path 都能直接访问（import 语句自动绑定）
# # print(f"能否直接访问 os：{ 'os' in globals() }")  # True（顶层包被绑定到变量 os）
# # print(f"能否直接访问 os.path：{ 'os.path' in globals() }")  # False（仅绑定顶层包，子模块不单独绑定）
# # print(f"os.path 的类型：{type(os.path)}")  # <class 'module'>（子模块已加载）

# # # 验证加载状态
# # print(f"os 是否加载：{'os' in sys.modules}")  # True
# # print(f"os.path 是否加载：{'os.path' in sys.modules}")  # True（导入时已加载）
# """
# === 写法1：import os.path ===
# 能否直接访问 os：True
# 能否直接访问 os.path：False
# os.path 的类型：<class 'module'>
# os 是否加载：True
# os.path 是否加载：True
# """
# import os
# # ---------------------- 写法2：import os ----------------------
# print("\n=== 写法2：import os ===")
# # 重新启动 Python 执行（避免缓存影响），仅执行 import os
# print(f"能否直接访问 os：{ 'os' in globals() }")  # True（顶层包被绑定）
# print(f"os.path 是否加载：{'os.path' in sys.modules}")  # False（子模块未加载）

# # 访问 os.path 时才加载
# print(f"os.path 的类型：{type(os.path)}")  # <class 'module'>（延迟加载）
# print(f"os.path 是否加载：{'os.path' in sys.modules}")  # True（访问后加载）
# """
# === 写法2：import os ===
# 能否直接访问 os：True
# os.path 是否加载：True
# os.path 的类型：<class 'module'>
# os.path 是否加载：True
# """
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

# if __name__ == "__main__":
#     print_python_info()

# """
# ========================================
# Python 版本信息：
# 完整版本号：3.12.11 (main, Sep 18 2025, 19:45:51) [MSC v.1944 64 bit (AMD64)]
# 主版本号：3
# 次版本号：12
# 微版本号：11
# 发布级别：final
# 序列号：0

# ========================================
# Python 路径信息：
# Python 可执行文件路径：D:\zyt\git_ln\algo_agent\.venv\Scripts\python.exe
# Python 安装目录：D:\zyt\git_ln\algo_agent\.venv

# Python 模块搜索路径（sys.path）：
#    1. d:\zyt\git_ln\algo_agent\tests\playground
#    2. C:\Users\zooos\AppData\Roaming\uv\python\cpython-3.12.11-windows-x86_64-none\python312.zip
#    3. C:\Users\zooos\AppData\Roaming\uv\python\cpython-3.12.11-windows-x86_64-none\DLLs
#    4. C:\Users\zooos\AppData\Roaming\uv\python\cpython-3.12.11-windows-x86_64-none\Lib
#    5. C:\Users\zooos\AppData\Roaming\uv\python\cpython-3.12.11-windows-x86_64-none
#    6. D:\zyt\git_ln\algo_agent\.venv
#    7. D:\zyt\git_ln\algo_agent\.venv\Lib\site-packages
# ========================================

# """

# 自定义空字典作为 globals 和 locals
g = {}
l = {}

# 待执行的代码：包含顶层变量、函数（函数内有局部变量）
code = """
a = 10  # 顶层变量（全局级）
def func():
    b = 20  # 函数内局部变量
    print(b)  # 20
func()
"""

# 执行 exec，传入空 g 和 l
exec(code, g, l)

# 查看执行后的结果
# print("globals 字典:", g)  # 包含顶层变量 a 和函数 func
# print("locals 字典:", l)   # 空字典！（顶层变量不写入 locals，函数内局部变量仅在函数执行时有效）

import os
import threading

# 主程序的进程ID和线程ID
print("主程序 - 进程ID:", os.getpid())
print("主程序 - 线程ID:", threading.get_ident())

# 自定义globals，用于后续验证变量是否在当前进程
g = {}

# 用exec执行代码，打印进程/线程ID，同时定义变量
exec("""
import os
import threading
print("exec内 - 进程ID:", os.getpid())
print("exec内 - 线程ID:", threading.get_ident())
exec_var = "我是exec定义的变量"
""", g)

# 验证：exec定义的变量能直接在主程序中通过globals读取（同一进程内存共享）
print("主程序读取exec变量:", g["exec_var"])