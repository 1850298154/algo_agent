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

import sys
# import os.path
# # ---------------------- 写法1：import os.path ----------------------
# print("=== 写法1：import os.path ===")
# # 验证变量绑定：os 和 os.path 都能直接访问（import 语句自动绑定）
# print(f"能否直接访问 os：{ 'os' in globals() }")  # True（顶层包被绑定到变量 os）
# print(f"能否直接访问 os.path：{ 'os.path' in globals() }")  # False（仅绑定顶层包，子模块不单独绑定）
# print(f"os.path 的类型：{type(os.path)}")  # <class 'module'>（子模块已加载）

# # 验证加载状态
# print(f"os 是否加载：{'os' in sys.modules}")  # True
# print(f"os.path 是否加载：{'os.path' in sys.modules}")  # True（导入时已加载）
"""
=== 写法1：import os.path ===
能否直接访问 os：True
能否直接访问 os.path：False
os.path 的类型：<class 'module'>
os 是否加载：True
os.path 是否加载：True
"""
import os
# ---------------------- 写法2：import os ----------------------
print("\n=== 写法2：import os ===")
# 重新启动 Python 执行（避免缓存影响），仅执行 import os
print(f"能否直接访问 os：{ 'os' in globals() }")  # True（顶层包被绑定）
print(f"os.path 是否加载：{'os.path' in sys.modules}")  # False（子模块未加载）

# 访问 os.path 时才加载
print(f"os.path 的类型：{type(os.path)}")  # <class 'module'>（延迟加载）
print(f"os.path 是否加载：{'os.path' in sys.modules}")  # True（访问后加载）
"""
=== 写法2：import os ===
能否直接访问 os：True
os.path 是否加载：True
os.path 的类型：<class 'module'>
os.path 是否加载：True
"""
