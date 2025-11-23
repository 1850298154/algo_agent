from traceback import print_exc


def recursive_crash(depth=0):
    # 打印当前递归深度（可选，用于观察）
    if depth % 100 == 0:
        print(f"当前递归深度：{depth}")
    # 无限递归调用，直到触发深度限制
    recursive_crash(depth + 1)

# # 运行崩溃（约 1000 层后报错）
# try:
#     recursive_crash()
# except RecursionError as e:
#     print("递归崩溃栈跟踪：")
#     print(print_exc())
#     print(f"\n崩溃原因：{e}")
r"""
(algo-agent) D:\zyt\git_ln\algo_agent>D:/zyt/git_ln/algo_agent/.venv/Scripts/python.exe d:/zyt/git_ln/algo_agent/tests/playground/crashed.py
d:\zyt\git_ln\algo_agent\tests\playground\crashed.py:37: SyntaxWarning: invalid escape sequence '\z'
  D:\zyt\git_ln\algo_agent\tests\playground>python crashed.py
当前递归深度：0
当前递归深度：100
当前递归深度：200
当前递归深度：300
当前递归深度：400
当前递归深度：500
当前递归深度：600
当前递归深度：700
当前递归深度：800
当前递归深度：900
递归崩溃栈跟踪：
Traceback (most recent call last):
  File "d:\zyt\git_ln\algo_agent\tests\playground\crashed.py", line 13, in <module>
    recursive_crash()
  File "d:\zyt\git_ln\algo_agent\tests\playground\crashed.py", line 9, in recursive_crash
    recursive_crash(depth + 1)
  File "d:\zyt\git_ln\algo_agent\tests\playground\crashed.py", line 9, in recursive_crash
    recursive_crash(depth + 1)
  File "d:\zyt\git_ln\algo_agent\tests\playground\crashed.py", line 9, in recursive_crash
    recursive_crash(depth + 1)
  [Previous line repeated 996 more times]
RecursionError: maximum recursion depth exceeded
None

崩溃原因：maximum recursion depth exceeded
"""


def fast_memory_oom():
    large_str = ""
    count = 0
    while True:
        # 每次拼接 10MB 的字符串（"a" * 1024*1024*10，每个字符 1 字节，实际占用 ~10MB）
        large_str += "a" * (1024 * 1024 * 1024 * 4)
        count += 1
        print(f"已拼接 {count} 次，当前字符串大小约 {count*4} GB")

# try:
#     fast_memory_oom()
# except MemoryError as e:
#     print("内存溢出栈跟踪：")
#     print(print_exc())
#     print(f"\n崩溃原因：{e}")
r"""
D:\zyt\git_ln\algo_agent\tests\playground>python crashed.py
当前递归深度：0
当前递归深度：100
当前递归深度：200
当前递归深度：300
当前递归深度：400
当前递归深度：500
当前递归深度：600
当前递归深度：700
当前递归深度：800
当前递归深度：900
递归崩溃栈跟踪：
Traceback (most recent call last):
  File "D:\zyt\git_ln\algo_agent\tests\playground\crashed.py", line 13, in <module>
    recursive_crash()
    ~~~~~~~~~~~~~~~^^
  File "D:\zyt\git_ln\algo_agent\tests\playground\crashed.py", line 9, in recursive_crash
    recursive_crash(depth + 1)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^
  File "D:\zyt\git_ln\algo_agent\tests\playground\crashed.py", line 9, in recursive_crash
    recursive_crash(depth + 1)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^
  File "D:\zyt\git_ln\algo_agent\tests\playground\crashed.py", line 9, in recursive_crash
    recursive_crash(depth + 1)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^
  [Previous line repeated 996 more times]
RecursionError: maximum recursion depth exceeded
None

崩溃原因：maximum recursion depth exceeded
已拼接 1 次，当前字符串大小约 4 GB
已拼接 2 次，当前字符串大小约 8 GB
已拼接 3 次，当前字符串大小约 12 GB
已拼接 4 次，当前字符串大小约 16 GB
已拼接 5 次，当前字符串大小约 20 GB
已拼接 6 次，当前字符串大小约 24 GB
已拼接 7 次，当前字符串大小约 28 GB
已拼接 8 次，当前字符串大小约 32 GB
已拼接 9 次，当前字符串大小约 36 GB
已拼接 10 次，当前字符串大小约 40 GB
已拼接 11 次，当前字符串大小约 44 GB
已拼接 12 次，当前字符串大小约 48 GB
已拼接 13 次，当前字符串大小约 52 GB
已拼接 14 次，当前字符串大小约 56 GB
内存溢出栈跟踪：
Traceback (most recent call last):
  File "D:\zyt\git_ln\algo_agent\tests\playground\crashed.py", line 30, in <module>
    fast_memory_oom()
    ~~~~~~~~~~~~~~~^^
  File "D:\zyt\git_ln\algo_agent\tests\playground\crashed.py", line 25, in fast_memory_oom
    large_str += "a" * (1024 * 1024 * 1024 * 4)
MemoryError
None

崩溃原因：


"""


# import os
# try:
#     print("触发 SegFault")
#     os._exit(139)
#     print("SegFault")
# except Exception as e:
#     print(f"\n崩溃原因：{e}")
r"""
(algo-agent) D:\zyt\git_ln\algo_agent>D:/zyt/git_ln/algo_agent/.venv/Scripts/python.exe d:/zyt/git_ln/algo_agent/tests/playground/crashed.py
触发 SegFault

(algo-agent) D:\zyt\git_ln\algo_agent>
"""