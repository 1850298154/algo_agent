import linecache
import os
from src.runtime.python_executor import (
    run, 
    run_structured, 
    ExecutionResult, 
    ExecutionStatus, 
    )

def test_python_executor():

    my_globals = {"a": 123, "b": [1, 2, 3]}
    my_locals = {"a": 123, "b": [1, 2, 3]}

    res=run("a+=100000",my_globals,my_locals)  # 输出:  空
    print(res)
    res=run("print(a)",my_globals,my_locals)  # 输出:  100123
    print(res)

    print(my_globals) # 还是 a:123 ，优先修改locals
    print(my_locals) # a: 100123

    my_globals["a"] = -100000000
    res=run("a+=100000",my_globals,my_locals)  # 输出:  空
    print(res)
    res=run("print(a)",my_globals,my_locals)  # 输出:  200123， 用的是locals
    print(res)

    g = {'x': 42}
    exec("x += 1", g)
    print(g['x'])  # 输出: 43, 用的是globals
    print(g)  # 输出: {'x': 43}  # 添加输出g的内容
    import os.path
    import os.path
    print(os.getcwd())

def test_exception():
    my_globals = {"a": 123, "b": [1, 2, 3]}
    my_locals = {"a": 123, "b": [1, 2, 3]}
    res=run("a+=100000",my_globals,my_locals)  # 输出:  空
    print(res)
    res=run("print(a)",my_globals,my_locals)  # 输出: 100123
    print(res)
    res=run("print(b)",my_globals,my_locals)  # 输出: [1, 2, 3]
    print(res)
    res=run("print(a)",my_globals,my_locals)  # 输出: 100123
    print(res)
    res=run("print(c)",my_globals,my_locals)  # 输出: NameError("name 'c' is not defined")
    print(res)


def test_structured_executor():
    my_globals = {"a": 123, "b": [1, 2, 3]}
    my_locals = {"a": 123, "b": [1, 2, 3]}
    # res=run_structured("a+=100000",my_globals,my_locals)  # 输出: 123
    # print(type(res))
    # res=res.model_dump()
    # res.pop("globals")
    # print(res)
    # res=run_structured("print(a)",my_globals,my_locals)  # 输出: [1, 2, 3]
    # print(type(res))
    # res=res.model_dump()
    # res.pop("globals")
    # print(res)
    # res=run_structured("print(b)",my_globals,my_locals)  # 输出: [1, 2, 3]
    # print(type(res))
    # res=res.model_dump()
    # res.pop("globals")
    # print(res)
    
    # # 测试 NameError
    # res=run_structured("print(c)",my_globals,my_locals)  # 输出: NameError("name 'c' is not defined")
    # print(type(res))
    # res=res.model_dump()
    # res.pop("globals")
    # print(res)

    # 测试超时
    print("----- timeout test -----")
    res=run_structured("""import time
c = 10
time.sleep(5)""",my_globals,my_locals,timeout=1)  # 输出: TimeoutError
    print(type(res))
    res=res.model_dump()
    # res.pop("globals")
    print(res)
    
    
    print("----- time ok test -----")
    res=run_structured("""import time
c = 10
import scipy
""",my_globals,None,timeout=20000)  # 输出: TimeoutError
    print(type(res))
    res=res.model_dump()
    # res.pop("globals")
    print(res)
    
    
if __name__ == "__main__":
    # test_python_executor()
    # test_exception()
    test_structured_executor()
    
    