import linecache
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


def add_line_numbers(
    code_str,
    start=1,
    indent=" | ",
    skip_empty_lines=False,  # 是否跳过空行（不编号）
    line_num_format=None  # 自定义行号格式（如 "[{}] "）
):
    lines = code_str.splitlines()
    if not lines:
        return ""
    
    numbered_lines = []
    current_line_num = start
    
    # 自定义行号格式（优先级高于默认）
    if line_num_format is None:
        max_line_num = start + len(lines) - (1 if skip_empty_lines else 0)
        line_num_width = len(str(max_line_num))
        line_num_format = f"{{:>{line_num_width}}}{indent}"  # 默认右对齐
    
    for line in lines:
        # 处理空行：跳过编号或仅保留空行（不递增行号）
        stripped_line = line.strip()
        if skip_empty_lines and not stripped_line:
            numbered_lines.append(" " * len(line_num_format.format(start)) + line)  # 空行对齐
            continue
        
        # 非空行：添加编号
        numbered_line = line_num_format.format(current_line_num) + line
        numbered_lines.append(numbered_line)
        
        # 空行不递增行号（仅当 skip_empty_lines=False 时生效）
        if not skip_empty_lines or stripped_line:
            current_line_num += 1
    
    return "\n".join(numbered_lines)

# 测试 1：跳过空行（空行不编号，行号连续）
print("=== 跳过空行 ===")
code_with_empty = """def func():
    pass

# 空行上方是注释
result = func()

"""
print(add_line_numbers(code_with_empty, skip_empty_lines=True))

# 测试 2：自定义行号格式（如 "[1] "）
print("\n=== 自定义格式 ===")
print(add_line_numbers(code_with_empty, line_num_format="[{}] "))
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

"print('__name__', __name__)",    

"""
def main():
    print("核心逻辑执行")

# 主入口：只有模块被直接运行时才执行
if __name__ == "__main__":
    main()  # 预期执行，但实际会跳过
""",

"""
def myadd(a, b):
    return a+b/0

def main():
    print('global :', globals().keys())
    print('local :',  locals().keys())
    print("核心逻辑执行", myadd(1, 2))
print('global :', globals().keys())
print('local :',  locals().keys())
main()
"""
    ]

    for cnt, code in enumerate(codes, 1):
        print(f"======= 代码块 {cnt} ==============================:")
        try:
            compiled_code = compile(
                source=code,
                filename="dynamic_code.py",  # 虚拟文件名
                mode="exec"  # 对应ast.parse的mode="exec"
            )
            
            print("编译成功，开始执行...\n",add_line_numbers(code))
            print("编译成功，开始执行...",compiled_code)
            my_globals = {'__name__': '__main__'}  # 模拟主模块运行环境
            my_locals = my_globals # 让函数出现在 globals 中的两种方法：要么只传 globals，要么让 locals 复用 globals。
            # 执行代码（可选传入 globals/locals 隔离命名空间）
            exec(compiled_code, my_globals, my_locals)
            print("当前环境的global :", my_globals.keys())  # 输出：__main__（因为脚本直接运行）
            print("当前环境的local :", my_locals.keys())  # 输出：__main__（因为脚本直接运行）
            # print("当前环境的 __name__:", my_globals["__name__"])  # 输出：__main__（因为脚本直接运行）

        except Exception as e:
            # 获取完整报错信息（字符串格式）
            full_error = traceback.format_exc()
            print("完整报错信息：")
            print("-" * 50)
            print(full_error)
            print("-" * 50)
            print(full_error.splitlines())  # 只打印最后一行错误信息
            print("-" * 50)
            lines=full_error.splitlines()
            lines = lines[0:1] + lines[3:]
            print("\n".join(lines))  # 只打印最后一行错误信息
            print("-" * 50)
            # 也可以直接打印（无需手动格式化）
            # traceback.print_exc()
        finally:
            # 清理缓存（避免占用内存，可选）
            linecache.clearcache()            
if __name__ == "__main__":
    # test_python_executor()
    # test_exception()
    selftest()
# exec("print('__name__', __name__)")
# exec("print('__name__', __name__)",{}, {})
# """
# 输出：
# __name__ __main__
# __name__ builtins
# """
# a= 100000
# exec("a+=123")
# print(a) # 100123