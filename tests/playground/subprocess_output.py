import multiprocessing
import threading
import sys
from io import StringIO
from typing import Any, Dict, Optional
from src.runtime.schemas import ExecutionStatus, ExecutionResult

def worker_with_pipe(command, _globals, _locals, conn):
    sys.stdout = mystdout = StringIO()
    try:
        exec(command, _globals, _locals)
        conn.send(mystdout.getvalue())
    except Exception as e:
        conn.send(mystdout.getvalue() + f"\nException: {e}")
    finally:
        conn.close()

def run_structured(command: str, _globals: dict[str, Any] | None = None, _locals: Optional[Dict] = None, timeout: Optional[int] = None) -> ExecutionResult:
    parent_conn, child_conn = multiprocessing.Pipe()
    buffer = []

    def reader(conn, buffer):
        try:
            while True:
                if conn.poll(0.1):
                    data = conn.recv()
                    buffer.append(data)
                else:
                    break
        except EOFError:
            pass

    p = multiprocessing.Process(target=worker_with_pipe, args=(command, _globals, _locals, child_conn))
    p.start()

    t = threading.Thread(target=reader, args=(parent_conn, buffer))
    t.start()

    p.join(timeout)
    if p.is_alive():
        p.terminate()
        status = ExecutionStatus.TIMEOUT
    else:
        status = ExecutionStatus.SUCCESS

    t.join()
    std_output = "".join(buffer)

    return ExecutionResult(
        command=command,
        timeout=timeout,
        globals={},
        status=status,
        std_output=std_output,
    )
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
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

def run_structured(command: str, _globals: dict[str, Any] | None = None, _locals: Optional[Dict] = None, timeout: Optional[int] = None) -> ExecutionResult:
    parent_conn, child_conn = multiprocessing.Pipe()
    buffer = []

    def reader(conn, buffer):
        try:
            while True:
                if conn.poll(0.1):
                    data = conn.recv()
                    buffer.append(data)
                else:
                    if not conn.closed and not conn.poll():
                        continue
                    break
        except EOFError:
            pass

    p = multiprocessing.Process(target=worker_with_pipe, args=(command, _globals, _locals, child_conn))
    p.start()

    t = threading.Thread(target=reader, args=(parent_conn, buffer))
    t.start()

    p.join(timeout)
    if p.is_alive():
        p.terminate()
        status = ExecutionStatus.TIMEOUT
    else:
        status = ExecutionStatus.SUCCESS

    t.join()
    std_output = "".join(buffer)

    return ExecutionResult(
        command=command,
        timeout=timeout,
        globals={},
        status=status,
        std_output=std_output,
    )










def run_structured(command: str, _globals: dict[str, Any] | None = None, _locals: Optional[Dict] = None, timeout: Optional[int] = None) -> ExecutionResult:
    parent_conn, child_conn = multiprocessing.Pipe()
    buffer = []

    def reader(conn, buffer):
        try:
            while True:
                if conn.poll(0.1):
                    try:
                        data = conn.recv()
                        buffer.append(data)
                    except EOFError:
                        break
                else:
                    # 如果连接关闭则退出
                    if not conn.closed and not conn.poll():
                        continue
                    break
        except EOFError:
            pass

    p = multiprocessing.Process(target=worker_with_pipe, args=(command, _globals, _locals, child_conn))
    p.start()

    t = threading.Thread(target=reader, args=(parent_conn, buffer))
    t.start()

    p.join(timeout)
    if p.is_alive():
        p.terminate()
        status = ExecutionStatus.TIMEOUT
        parent_conn.close()  # 关键：关闭主进程的 Pipe 连接，reader 能退出
    else:
        status = ExecutionStatus.SUCCESS

    t.join()
    std_output = "".join(buffer)

    return ExecutionResult(
        command=command,
        timeout=timeout,
        globals={},
        status=status,
        std_output=std_output,
    )
if __name__ == "__main__":
    _globals = {}
    res = run_structured("""
import time
print("Start sleeping...", flush=True)
time.sleep(10)
print("Finished sleeping.", flush=True)
""", _globals={}, timeout=3)

    print(res)
