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

def run_structured(
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
                if conn.poll(0.1):
                    try:
                        data = conn.recv()
                        buffer.append(data)
                    except EOFError:
                        break
                else:
                    if not conn.closed and not conn.poll():
                        continue
                    break
        except OSError as e:
            print(f"连接失效：{e}")
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
        parent_conn.close()
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
    res = run_structured(
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