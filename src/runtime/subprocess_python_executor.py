from enum import Enum, unique
import multiprocessing
from multiprocessing.connection import PipeConnection
import threading
import sys
import traceback
from typing import Any, Dict, Optional
from src.runtime.schemas import ExecutionStatus, ExecutionResult
from src.runtime import cwd
from src.utils import global_logger, traceable


@unique
class _PipeType(str, Enum):
    STDOUT = "stdout"
    RESULT = "result"


def _worker_with_pipe(
    command: str,
    _globals: dict[str, Any] | None,
    _locals: Optional[Dict],
    timeout: Optional[int],
    child_conn: PipeConnection,
) -> None:
    """Execute a command in a subprocess with output captured via pipes."""
    # cwd.create_cwd('./wsm/1/g4-1')
    cwd.create_cwd('./wsm/2/g7-2')
    
    class _PipeWriter:
        def __init__(self, child_conn: PipeConnection):
            self.child_conn = child_conn

        def write(self, msg: str):
            if msg:
                # 通道1：标记为 'stdout'，传输实时输出
                # x1 = (f"\n\n\n\n[DEBUG] 子进程msg输出:-----------------------------------\n {msg}\n\n\n\n")
                # x2 = (f"\n\n\n\n[DEBUG] 子进程msg.encode('utf-8')输出:-----------------------------------\n {msg.encode('utf-8')}\n\n\n\n")
                # x3 = (f"\n\n\n\n[DEBUG] 子进程msg.encode('utf-8').decode('unicode_escape')输出:-----------------------------------\n {msg.encode('utf-8').decode('unicode_escape')}\n\n\n\n")
                # decoded_msg = msg.encode('utf-8').decode('unicode_escape')
                # _x_ = x1+x2+x3
                self.child_conn.send((_PipeType.STDOUT, msg))

        def flush(self):
            pass

    sys.stdout = _PipeWriter(child_conn)
    sys.stderr = sys.stdout
    try:
        exec(command, _globals, _locals)
        # global_logger.info("---------- 2.1.1 子进程正常结束：子进程构建成功的 ExecutionResult")
        res = ExecutionResult(
            arg_command=command,
            arg_globals=_globals or {},
            arg_timeout=timeout,
            exit_status=ExecutionStatus.SUCCESS,
        )
    except Exception as e:
        # global_logger.info("---------- 2.1.2 子进程异常结束：子进程捕获堆栈，构建失败的 ExecutionResult")
        res = ExecutionResult(
            arg_command=command,
            arg_globals=_globals or {},
            arg_timeout=timeout,
            exit_status=ExecutionStatus.FAILURE,
            exception_repr=repr(e),
            exception_type=type(e).__name__,
            exception_value=str(e),
            exception_traceback=traceback.format_exc(),
        )
    finally:
        # 通道2：标记为 'result'，传输最终对象
        child_conn.send((_PipeType.RESULT, res))
        child_conn.close()

@traceable
def run_structured_in_subprocess(
    command: str,
    _globals: dict[str, Any] | None = None,
    _locals: Optional[Dict] = None,
    timeout: Optional[int] = None,
) -> ExecutionResult:
    # 必须保持一致， 因为支持 exec 后续访问全局函数，同时也要将globals拿回来
    _locals = _globals  
    parent_conn, child_conn = multiprocessing.Pipe()
    subprocess_stdout_buffer: list[str] = []
    subprocess_result_container: list[ExecutionResult] = []

    def _reader(
        parent_conn: PipeConnection,
        subprocess_stdout_buffer: list[str],
        subprocess_result_container: list[ExecutionResult],
    ) -> None:
        """从子进程读取消息并分发处理"""
        try:
            while True:
                # 阻塞读取，直到 EOF
                msg: tuple[_PipeType, str | ExecutionResult] = parent_conn.recv()
                # 协议分发
                if isinstance(msg, tuple) and len(msg) == 2:
                    tag, data = msg
                    if tag == _PipeType.STDOUT:
                        subprocess_stdout_buffer.append(data)
                    elif tag == _PipeType.RESULT:
                        subprocess_result_container.append(data)
                else:
                    global_logger.error("Invalid message format: %s", msg)
                    subprocess_stdout_buffer.append(str(msg))
        except (EOFError, OSError) as e:
            global_logger.info(
                f"Pipe reader error: type={type(e).__name__}, value={str(e)}, kv={repr(e)}"  # , traceback={traceback.format_exc()}"
            )
            pass

    p = multiprocessing.Process(
        target=_worker_with_pipe, args=(command, _globals, _locals, timeout, child_conn)
    )
    p.start()

    # 必须关闭父进程持有的子端句柄，否则 reader 无法收到 EOF
    child_conn.close()

    t = threading.Thread(
        target=_reader,
        args=(parent_conn, subprocess_stdout_buffer, subprocess_result_container),
    )
    t.start()

    # 等待子进程结束或超时
    p.join(timeout)  
    if p.is_alive():
        global_logger.info("---------- 1. 超时情况：由父进程构建 ExecutionResult")
        # 确保进程真正终止
        p.terminate()  
        # 主动关闭连接以停止 reader
        p.join()  
        parent_conn.close()
        t.join()
        global_logger.info("---------- 1. 子进程超时退出：超时 %d 秒", timeout)
        final_res = ExecutionResult(
            arg_command=command,
            arg_timeout=timeout,
            arg_globals=_globals or {},
            exit_status=ExecutionStatus.TIMEOUT,
        )
    else:
        global_logger.info("---------- 2. 正常或异常退出：从子进程获取 ExecutionResult")
        t.join()

        if subprocess_result_container:
            global_logger.info("---------- 2.1 子进程正常退出： exec正常、exec异常")
            final_res: ExecutionResult = subprocess_result_container[0]
        else:
            global_logger.info("---------- 2.2 子进程崩溃退出：如 SegFault")
            final_res = ExecutionResult(
                arg_command=command,
                arg_timeout=timeout,
                arg_globals=_globals or {},
                exit_status=ExecutionStatus.CRASHED,
            )
    final_res.exit_code = p.exitcode  # 填充 exitcode 字段
    final_res.ret_stdout = "".join(subprocess_stdout_buffer)  # 填充 stdout 字段
    final_res.ret_tool2llm = ExecutionStatus.get_return_llm(final_res.exit_status, final_res)  # 填充 stdout 字段
    return final_res

if __name__ == "__main__":
    test_code = """
import os
print(os.getcwd())
    """
    test_code = r"""
import json

# 分析 schema.json 中的核心实体结构
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

# 加载并分析 schema
try:
    with open('schema.json', 'r', encoding='utf-8') as f:
        schema = json.load(f)
    analyze_schema_structure(schema)
except Exception as e:
    print(f'Error analyzing schema: {e}')    
    """
    result = run_structured_in_subprocess(test_code, {},  timeout=600)
    print('----------- 子进程执行结果 -----------')
    print(result)
