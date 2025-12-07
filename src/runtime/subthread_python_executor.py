import inspect
import os
import threading
import sys
import traceback
from typing import Any, Dict, Optional
from src.runtime.schemas import ExecutionStatus, ExecutionResult
from src.runtime import cwd
from src.utils import global_logger, traceable


def _worker_with_buffer(
    command: str,
    _globals: dict[str, Any] | None,
    _locals: Optional[Dict],
    timeout: Optional[int],
    stdout_buffer: list[str],
    result_container: list[ExecutionResult],
) -> None:
    """Execute a command in a thread with output captured via buffer."""
    cwd.create_cwd('./wsm/2/g7-2')

    class _BufferWriter:
        def __init__(self, buffer: list[str]):
            self.buffer = buffer

        def write(self, msg: str):
            if msg:
                self.buffer.append(msg)

        def flush(self):
            pass

    old_stdout = sys.stdout
    old_stderr = sys.stderr

    sys.stdout = _BufferWriter(stdout_buffer)
    sys.stderr = sys.stdout
    try:
        exec(command, _globals, _locals)
        global_logger.info("---------- 2.1.1 子线程正常结束：子线程构建成功的 ExecutionResult")
        res = ExecutionResult(
            arg_command=command,
            arg_globals=_globals or {},
            arg_timeout=timeout,
            exit_status=ExecutionStatus.SUCCESS,
        )
    except Exception as e:
        global_logger.info("---------- 2.1.2 子线程异常结束：子线程捕获堆栈，构建失败的 ExecutionResult")
        def filter_exec_traceback(exc_str:str = None):
            if exc_str is None:
                exc_str = traceback.format_exc()
            
            # 按行拆分栈信息，过滤出 <string> 相关的行（exec 内部代码）
            lines = exc_str.splitlines()
            exec_lines = []
            # 标记是否进入 exec 内部栈段（处理连续的栈行）
            in_exec_block = False
            
            for line in lines:
                # 核心特征：包含 "<string>"（exec 执行字符串代码的标记）
                if "Traceback" in line:
                    exec_lines.append(line)
                elif "<string>" in line:
                    in_exec_block = True
                    exec_lines.append(line)
                # 保留 exec 栈段的后续行（如出错代码行、异常描述）
                elif in_exec_block:
                    # 终止条件：遇到新的栈帧（以 "File " 开头但不含 <string>）
                    if line.startswith("File ") and "<string>" not in line:
                        in_exec_block = False
                        continue
                    exec_lines.append(line)
            # 重新拼接过滤后的字符串
            return "\n".join(exec_lines)
        res = ExecutionResult(
            arg_command=command,
            arg_globals=_globals or {},
            arg_timeout=timeout,
            exit_status=ExecutionStatus.FAILURE,
            exception_repr=repr(e),
            exception_type=type(e).__name__,
            exception_value=str(e),
            exception_traceback=filter_exec_traceback(),
        )
    finally:
        result_container.append(res)
        sys.stdout = old_stdout
        sys.stderr = old_stderr

@traceable
def run_structured_in_thread(
    command: str,
    _globals: dict[str, Any] | None = None,
    _locals: Optional[Dict] = None,
    timeout: Optional[int] = None,
) -> ExecutionResult:
    _locals = _globals
    stdout_buffer: list[str] = []
    result_container: list[ExecutionResult] = []

    t = threading.Thread(
        target=_worker_with_buffer,
        args=(command, _globals, _locals, timeout, stdout_buffer, result_container),
    )
    t.start()
    t.join(timeout)
    if t.is_alive():
        global_logger.info("---------- 1. 超时情况：由主线程构建 ExecutionResult")
        # 线程无法强制终止，只能标记为超时
        final_res = ExecutionResult(
            arg_command=command,
            arg_timeout=timeout,
            arg_globals=_globals or {},
            exit_status=ExecutionStatus.TIMEOUT,
        )
    else:
        global_logger.info("---------- 2. 正常或异常退出：从线程获取 ExecutionResult")
        if result_container:
            global_logger.info("---------- 2.1 子线程正常退出： exec正常、exec异常")
            final_res: ExecutionResult = result_container[0]
        else:
            global_logger.info("---------- 2.2 子线程崩溃退出：如 SegFault")
            final_res = ExecutionResult(
                arg_command=command,
                arg_timeout=timeout,
                arg_globals=_globals or {},
                exit_status=ExecutionStatus.CRASHED,
            )
    final_res.exit_code = None  # 线程没有 exitcode
    final_res.ret_stdout = "".join(stdout_buffer)
    final_res.ret_tool2llm = ExecutionStatus.get_return_llm(final_res.exit_status, final_res)
    return final_res

if __name__ == "__main__":
    test_code = """
import os
print(os.getcwd())
    """
    test_code = r"""
import json

def analyze_schema_structure(schema):
    if not schema:
        print('Schema is empty.')
        return

    print('=== 数据结构分析 ===')
    print(f'根对象: {schema.get("title")}')
    print(f'描述: {schema.get("description")}')

    defs = schema.get('$defs', {})
    entities = ['Task', 'Carrier', 'Location', 'Material', 'PathSegment', 'RiskPoint']

    for entity in entities:
        if entity in defs:
            props = defs[entity]['properties']
            required = defs[entity].get('required', [])
            print(f'\n【{entity}】')
            print(f'  属性数量: {len(props)}, 必填项: {len(required)}')
            print(f'  核心字段: {list(props.keys())[:5]}...')

try:
    with open('schema.json', 'r', encoding='utf-8') as f:
        schema = json.load(f)
    analyze_schema_structure(schema)
except Exception as e:
    print(f'Error analyzing schema: {e}')    
    """
    result = run_structured_in_thread(test_code, {},  timeout=10)
    print('----------- 子线程执行结果 -----------')
    print(result)
    result = run_structured_in_thread("1/0", {},  timeout=10)
    print('----------- 子线程执行结果 -----------')
    print(result)