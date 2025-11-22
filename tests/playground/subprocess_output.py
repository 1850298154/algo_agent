import multiprocessing
from multiprocessing.connection import PipeConnection
import threading
import sys
from typing import Any, Dict, Optional
from src.runtime.schemas import ExecutionStatus, ExecutionResult

class PipeWriter:
    def __init__(self, conn):
        self.conn = conn

    def write(self, msg):
        # 只发送非空字符串
        if msg:
            self.conn.send(msg)

    def flush(self):
        pass

def worker_with_pipe(command, _globals, _locals, conn):
    sys.stdout = PipeWriter(conn)
    try:
        exec(command, _globals, _locals)
    except Exception as e:
        conn.send(f"\nException: {e}")
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

    def reader(conn: PipeConnection, buffer: list):
        try:
            while True:
                # 简化读取逻辑：直接阻塞读取，直到管道关闭抛出 EOFError
                # 这样可以避免轮询带来的复杂性和潜在的死循环
                data = conn.recv()
                buffer.append(data)
        except (EOFError, OSError):
            # 管道关闭或连接断开时退出循环
            pass

    p = multiprocessing.Process(target=worker_with_pipe, args=(command, _globals, _locals, child_conn))
    p.start()
    
    # 关键修复：父进程必须关闭它持有的 child_conn 句柄
    # 否则管道的写入端引用计数不为0，reader 永远收不到 EOFError，导致死锁
    child_conn.close()

    t = threading.Thread(target=reader, args=(parent_conn, buffer))
    t.start()

    p.join(timeout)
    if p.is_alive():
        p.terminate()
        status = ExecutionStatus.TIMEOUT
        # 超时情况下，主动关闭父端连接，使 reader 线程抛出异常并退出
        parent_conn.close()
    else:
        status = ExecutionStatus.SUCCESS
        # 正常结束时，由于上面已经关闭了父进程的 child_conn，
        # 且子进程退出后系统回收了子进程的 child_conn，
        # 管道写入端完全关闭，reader 会收到 EOFError 自动退出

    t.join()
    std_output = "".join(buffer)

    return ExecutionResult(
        command=command,
        timeout=timeout,
        globals={},
        status=status,
        std_output=std_output,
    )

def test_structured_executor():
    my_globals = {"a": 123, "b": [1, 2, 3]}
    my_locals = {"a": 123, "b": [1, 2, 3]}
    # 测试超时
    print("----- timeout test -----")
    res=run_structured_in_subprocess("""import time
c = 10
time.sleep(5)""",my_globals,my_locals,timeout=1)  # 输出: TimeoutError
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
    
    
if __name__ == "__main__":
    _globals = {}
    res = run_structured_in_subprocess(
        """
import time
print("Start sleeping...", flush=True)
time.sleep(10)
print("Finished sleeping.", flush=True)
""",
        _globals={},
        timeout=3
    )
    print(res)
    
        
    # test_python_executor()
    # test_exception()
    test_structured_executor()
    
    