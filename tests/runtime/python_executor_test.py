import os
# 打印路径
print("当前路径:", os.getcwd())
from src.runtime.python_executor import run

my_globals = {"a": 123, "b": [1, 2, 3]}
my_locals = {"a": 123, "b": [1, 2, 3]}

res=run("a+=100000",my_globals,my_locals)  # 输出: 123
print(res)
res=run("print(a)",my_globals,my_locals)  # 输出: [1, 2, 3]
print(res)

print(my_globals)
print(my_locals)

my_globals["a"] = -100000000
res=run("a+=100000",my_globals,my_locals)  # 输出: 123
print(res)
res=run("print(a)",my_globals,my_locals)  # 输出: [1, 2, 3]
print(res)

g = {'x': 42}
exec("x += 1", g)
print(g['x'])  # 输出: 43
# print(g)  # 输出: 43
import os.path
import os.path
print(os.getcwd())
"""
100123


-99900000

43

(algo-agent) D:\zyt\git_ln\algo_agent>D:/zyt/git_ln/algo_agent/.venv/Scripts/python.exe d:/zyt/git_ln/algo_agent/src/runtime/python_executor.py

100123


200123

43

"""