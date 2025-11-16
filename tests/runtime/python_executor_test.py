import os
from src.runtime.python_executor import run
# 打印路径
print("当前路径:", os.getcwd())
#  Python 搜索路径
print("Python 搜索路径:", os.sys.path)

def test_python_executor():

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

def test_exception():
    my_globals = {"a": 123, "b": [1, 2, 3]}
    my_locals = {"a": 123, "b": [1, 2, 3]}
    res=run("a+=100000",my_globals,my_locals)  # 输出: 123
    print(res)
    res=run("print(a)",my_globals,my_locals)  # 输出: [1, 2, 3]
    print(res)
    res=run("print(b)",my_globals,my_locals)  # 输出: [1, 2, 3]
    print(res)
    res=run("print(a)",my_globals,my_locals)  # 输出: [1, 2, 3]
    print(res)
    res=run("print(c)",my_globals,my_locals)  # 输出: NameError("name 'c' is not defined")
    print(res)


def selftest():
    import traceback
    codes = [
        """
def add(a, b):
    return a + b

# 错误：传入 3 个参数（函数仅接收 2 个）
result = add(1, 2, 3)
print(result)
        """,
        """
# 相对导入（假设当前逻辑是“作为主模块运行”）
from .utils import func  # 常见于模块内的导入语法
        """,        
"from __future__ import print_function",    
    ]

    for code in codes:
        try:
            my_globals = {}
            my_locals = {}
            # 执行代码（可选传入 globals/locals 隔离命名空间）
            exec(code, my_globals, my_locals)
        except Exception as e:
            # 获取完整报错信息（字符串格式）
            full_error = traceback.format_exc()
            print("完整报错信息：")
            print("-" * 50)
            print(full_error)
            print("-" * 50)
            # 也可以直接打印（无需手动格式化）
            # traceback.print_exc()
            
if __name__ == "__main__":
    # test_python_executor()
    # test_exception()
    selftest()
