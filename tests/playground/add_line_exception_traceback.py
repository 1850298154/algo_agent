
import linecache


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
            # my_locals = {}
            # 执行代码（可选传入 globals/locals 隔离命名空间）
            exec(compiled_code, my_globals, my_locals)
            print("当前环境的global :", my_globals.keys())  # 输出：__main__（因为脚本直接运行）
            print("当前环境的local :", my_locals.keys())  # 输出：__main__（因为脚本直接运行）
            # print("当前环境的 __name__:", my_globals["__name__"])  # 输出：__main__（因为脚本直接运行）

        except Exception as e:
            # 获取完整报错信息（字符串格式）
            def test():
                full_error = traceback.format_exc()
                return full_error
            full_error = test()
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

""" 如果使用了 locals 参数，则函数无法出现在 globals 中
======= 代码块 6 ==============================:
编译成功，开始执行...
  1 |
 2 | def myadd(a, b):
 3 |     return a+b/0
 4 |
 5 | def main():
 6 |     print('global :', globals().keys())
 7 |     print('local :',  locals().keys())
 8 |     print("核心逻辑执行", myadd(1, 2))
 9 | print('global :', globals().keys())
10 | print('local :',  locals().keys())
11 | main()
编译成功，开始执行... <code object <module> at 0x0000017D43E37DE0, file "dynamic_code.py", line 1>
global : dict_keys(['__name__', '__builtins__'])
local : dict_keys(['myadd', 'main'])
global : dict_keys(['__name__', '__builtins__'])
local : dict_keys([])
完整报错信息：
--------------------------------------------------
Traceback (most recent call last):
  File "d:\zyt\git_ln\algo_agent\tests\playground\add_line_exception_traceback.py", line 115, in selftest
    exec(compiled_code, my_globals, my_locals)
  File "dynamic_code.py", line 11, in <module>
  File "dynamic_code.py", line 8, in main
NameError: name 'myadd' is not defined

--------------------------------------------------
['Traceback (most recent call last):', '  File "d:\\zyt\\git_ln\\algo_agent\\tests\\playground\\add_line_exception_traceback.py", line 115, in selftest', '    exec(compiled_code, my_globals, my_locals)', '  File "dynamic_code.py", line 11, in <module>', '  File "dynamic_code.py", line 8, in main', "NameError: name 'myadd' is not defined"]
--------------------------------------------------
Traceback (most recent call last):
  File "dynamic_code.py", line 11, in <module>
  File "dynamic_code.py", line 8, in main
NameError: name 'myadd' is not defined
--------------------------------------------------

"""