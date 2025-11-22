import multiprocessing
from multiprocessing.connection import PipeConnection
import threading
import sys
import traceback
from typing import Any, Dict, Optional
from src.runtime.schemas import ExecutionStatus, ExecutionResult

class PipeWriter:
    def __init__(self, conn):
        self.conn = conn

    def write(self, msg):
        if msg:
            # 通道1：标记为 'stdout'，传输实时输出
            self.conn.send(("stdout", msg))

    def flush(self):
        pass

def worker_with_pipe(command, _globals, _locals, conn):
    sys.stdout = PipeWriter(conn)
    try:
        exec(command, _globals, _locals)
        # 正常结束：子进程构建成功的 ExecutionResult
        # 注意：std_output 暂时留空，由父进程将流式输出合并进来
        res = ExecutionResult(
            command=command,
            status=ExecutionStatus.SUCCESS,
            std_output="", 
            globals=_globals or {},
        )
        # 通道2：标记为 'result'，传输最终对象
        conn.send(("result", res))
    except Exception:
        # 异常结束：子进程捕获堆栈，构建失败的 ExecutionResult
        exc_msg = traceback.format_exc()
        res = ExecutionResult(
            command=command,
            status=ExecutionStatus.FAILURE, 
            timeout=None,
            std_output=exc_msg, # 将错误堆栈放入 output 部分
            globals=_globals or {},
        )
        conn.send(("result", res))
    finally:
        conn.close()

def run_structured_in_subprocess(
    command: str,
    _globals: dict[str, Any] | None = None,
    _locals: Optional[Dict] = None,
    timeout: Optional[int] = None
) -> ExecutionResult:
    parent_conn, child_conn = multiprocessing.Pipe()
    buffer = []
    result_container = []

    def reader(conn: PipeConnection, buffer: list, result_container: list):
        try:
            while True:
                # 阻塞读取，直到 EOF
                msg = conn.recv()
                # 协议分发
                if isinstance(msg, tuple) and len(msg) == 2:
                    tag, data = msg
                    if tag == "stdout":
                        buffer.append(data)
                    elif tag == "result":
                        result_container.append(data)
                else:
                    buffer.append(str(msg))
        except (EOFError, OSError):
            pass

    p = multiprocessing.Process(target=worker_with_pipe, args=(command, _globals, _locals, child_conn))
    p.start()
    
    # 必须关闭父进程持有的子端句柄，否则 reader 无法收到 EOF
    child_conn.close()

    t = threading.Thread(target=reader, args=(parent_conn, buffer, result_container))
    t.start()

    p.join(timeout)

    if p.is_alive():
        # --- 超时情况：由父进程构建 ExecutionResult ---
        p.terminate()
        # 确保进程真正终止
        p.join()
        # 主动关闭连接以停止 reader
        parent_conn.close()
        t.join()
        print('---------- timeout ----------')
        final_res = ExecutionResult(
            command=command,
            timeout=timeout,
            globals={},
            status=ExecutionStatus.TIMEOUT,
            std_output="".join(buffer) + "\nTimeout reached.",
        )
    else:
        # --- 正常或异常结束：从子进程获取 ExecutionResult ---
        t.join()
        full_stdout = "".join(buffer)
        
        if result_container:
            print('---------- process finished ----------')
            # 获取子进程发回的 Result 对象
            child_res = result_container[0]
            # 合并流式输出和子进程的错误信息(如果有)
            final_output = full_stdout + child_res.std_output
            
            # 重构最终结果（合并了父进程收集的 stdout 和子进程的 status/error）
            final_res = ExecutionResult(
                command=command,
                timeout=timeout,
                globals={},
                status=child_res.status,
                std_output=final_output
            )
            final_res = child_res
        else:
            print('---------- process crashed ----------')
            # 进程崩溃（如 SegFault），未发送结果即退出
            final_res = ExecutionResult(
                command=command,
                timeout=timeout,
                globals={},
                status=getattr(ExecutionStatus, "FAILURE", "FAILURE"),
                std_output=full_stdout + f"\nProcess crashed with exit code {p.exitcode}",
            )
            final_res = child_res

    return final_res

# ...existing code...

def test_structured_executor():
    my_globals = {"a": 123, "b": [1, 2, 3]}
    my_locals = {"a": 123, "b": [1, 2, 3]}
    # 测试超时
    print("----- timeout test -----")
    res=run_structured_in_subprocess("""
import time
print("Start sleeping...", flush=True)
time.sleep(10)
print("Finished sleeping.", flush=True)
""",my_globals,my_locals,timeout=3)  # 输出: TimeoutError
    print(type(res))
    res=res.model_dump()
    # res.pop("globals")
    print(res)
    
    
    print("----- time ok test -----")
    res=run_structured_in_subprocess("""import time
c = 10
import scipy
print("scipy imported")
""",my_globals,None,timeout=20000)  # 输出: TimeoutError
    print(type(res))
    res=res.model_dump()
    # res.pop("globals")
    print(res)
    
    print("----- time exception test -----")
    res=run_structured_in_subprocess("""
a = 123
b = 0
c = a/b
""",my_globals,None,timeout=20000)  # 输出: TimeoutError
    print(type(res))
    res=res.model_dump()
    # res.pop("globals")
    print(res)
    
    
if __name__ == "__main__":
    test_structured_executor()
    
    