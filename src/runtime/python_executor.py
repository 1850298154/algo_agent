import multiprocessing
import re
import sys
from io import StringIO
import traceback
from typing import Any, Dict, Optional, Union
from src.runtime import source_code
from src.runtime.schemas import ExecutionStatus, ExecutionResult

def sanitize_input(query: str) -> str:
    """Sanitize input to the python REPL.

    Remove whitespace, backtick & python
    (if llm mistakes python console as terminal)

    Args:
        query: The query to sanitize

    Returns:
        str: The sanitized query
    """
    query = re.sub(r"^(\s|`)*(?i:python)?\s*", "", query)
    query = re.sub(r"(\s|`)*$", "", query)
    return query

# 新增：worker 函数的辅助包装，用于捕获 globals 和状态
def worker_with_globals_capture(
    command: str,
    _globals: Optional[Dict],
    _locals: Optional[Dict],
    queue: multiprocessing.Queue,
) -> None:
    # # 深拷贝原始 globals 避免污染，创建独立执行环境
    # import copy
    # exec_globals = copy.deepcopy(_globals) if _globals is not None else None
    # exec_locals = copy.deepcopy(_locals) if _locals is not None else None
    exec_globals = _globals
    exec_locals  = _locals
    
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    # exec_result: Optional[ExecutionResult] = None
    try:
        cleaned_command = sanitize_input(command)
        exec(cleaned_command, exec_globals, exec_locals)
        exec_result = ExecutionResult(
            status=ExecutionStatus.SUCCESS,
            output=mystdout.getvalue(),
            globals=exec_globals,
            exception_type=None,
            exception_value=None,
            exception_traceback=None
        )
    except Exception as e:
        print('-----------exception---------------')
        code_and_traceback = source_code.get_code_and_traceback(command)
        exec_result = ExecutionResult(
            status=ExecutionStatus.FAILURE,
            output=mystdout.getvalue(),
            globals=exec_globals,
            exception_type=type(e).__name__,
            exception_value=repr(e),
            exception_traceback=source_code.get_exception_traceback()
        )
    finally:
        sys.stdout = old_stdout
        queue.put(exec_result)

def worker(
    command: str,
    _globals: Optional[Dict],
    _locals: Optional[Dict],
    queue: multiprocessing.Queue,
) -> None:
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    try:
        cleaned_command = sanitize_input(command)
        exec(cleaned_command, _globals, _locals)
        sys.stdout = old_stdout
        queue.put(mystdout.getvalue())
    except Exception as e:
        # 获取完整报错信息（字符串格式）
        code_and_traceback = source_code.get_code_and_traceback(command)
        sys.stdout = old_stdout
        queue.put(code_and_traceback)

# 新增：支持结构化返回的函数
def run_structured(
        command: str, 
        _globals: dict[str, Any] | None = None, 
        _locals: Optional[Dict] = None, 
        timeout: Optional[int] = None
    ) -> ExecutionResult:
    """Run command with structured result (BaseModel).
    
    Returns:
        ExecutionResult: 包含执行状态（枚举）、输出、全局变量、错误信息的结构化结果
    """
    queue: multiprocessing.Queue = multiprocessing.Queue()

    if timeout is not None:
        # 使用捕获 globals 的 worker 进程
        p = multiprocessing.Process(
            target=worker_with_globals_capture, args=(command, _globals, _locals, queue)
        )
        p.start()
        p.join(timeout)

        if p.is_alive():
            p.terminate()
            # 超时状态：单独作为一种枚举值
            return ExecutionResult(
                status=ExecutionStatus.TIMEOUT,
                output="Execution timed out",
                globals=_globals or {},
            )
    else:
        worker_with_globals_capture(command, _globals, _locals, queue)
    
    # 从队列获取结果并转换为 BaseModel（自动校验枚举值）
    exec_result = queue.get()
    return exec_result

def run(
        command: str, 
        _globals: dict[str, Any] | None = None, 
        _locals: Optional[Dict] = None, 
        timeout: Optional[int] = None
    ) -> str:

    """Run command with own globals/locals and returns anything printed.
    Timeout after the specified number of seconds."""

    queue: multiprocessing.Queue = multiprocessing.Queue()

    # Only use multiprocessing if we are enforcing a timeout
    if timeout is not None:
        # create a Process
        p = multiprocessing.Process(
            target=worker, args=(command, _globals, _locals, queue)
        )

        # start it
        p.start()

        # wait for the process to finish or kill it after timeout seconds
        p.join(timeout)

        if p.is_alive():
            p.terminate()
            return "Execution timed out"
    else:
        worker(command, _globals, _locals, queue)
    # get the result from the worker function
    return queue.get()
