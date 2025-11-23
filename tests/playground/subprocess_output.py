from enum import Enum, unique
import multiprocessing
from multiprocessing.connection import PipeConnection
import threading
import sys
import traceback
from typing import Any, Dict, Optional
from src.runtime.schemas import ExecutionStatus, ExecutionResult
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

    class _PipeWriter:
        def __init__(self, child_conn: PipeConnection):
            self.child_conn = child_conn

        def write(self, msg: str):
            if msg:
                # 通道1：标记为 'stdout'，传输实时输出
                self.child_conn.send((_PipeType.STDOUT, msg))

        def flush(self):
            pass

    sys.stdout = _PipeWriter(child_conn)
    try:
        exec(command, _globals, _locals)
        global_logger.info("---------- 2.1.1 子进程正常结束：子进程构建成功的 ExecutionResult")
        res = ExecutionResult(
            arg_command=command,
            arg_globals=_globals or {},
            arg_timeout=timeout,
            exit_status=ExecutionStatus.SUCCESS,
        )
    except Exception as e:
        global_logger.info("---------- 2.1.2 子进程异常结束：子进程捕获堆栈，构建失败的 ExecutionResult")
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
                f"Pipe reader error: type={type(e).__name__}, value={str(e)}, kv={repr(e)}, traceback={traceback.format_exc()}"
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
    return final_res


# ...existing code...
import pprint


def test_structured_executor():
    my_globals = {"a": 123, "b": [1, 2, 3]}
    my_locals = {"a": 123, "b": [1, 2, 3]}
    # 测试超时
    print("----- timeout test -----")
    res = run_structured_in_subprocess(
        """
import time
print("Start sleeping...", flush=True)
time.sleep(10)
print("Finished sleeping.", flush=True)
""",
        my_globals,
        my_locals,
        timeout=3,
    )  # 输出: TimeoutError
    print(type(res))
    res = res.model_dump()
    # res.pop("globals")
    pprint.pprint(res)

    print("----- time ok test -----")
    res = run_structured_in_subprocess(
        """import time
c = 10
import scipy
print("scipy imported")
""",
        my_globals,
        None,
        timeout=20000,
    )  # 输出: TimeoutError
    print(type(res))
    res = res.model_dump()
    # res.pop("globals")
    pprint.pprint(res)

    print("----- time exception test -----")
    res = run_structured_in_subprocess(
        """
a = 123
b = 0
c = a/b
""",
        my_globals,
        None,
        timeout=20000,
    )  # 输出: TimeoutError
    print(type(res))
    res = res.model_dump()
    # res.pop("globals")
    pprint.pprint(res)

    print("----- test process crash -----")
    res = run_structured_in_subprocess(
        r"""
# 进程崩溃（如 SegFault），未发送结果即退出的例子
import os
try:
    # 触发 SegFault
    os._exit(139)
except Exception as e:
    print(f"\n崩溃原因：{e}")
""",
        my_globals,
        my_locals,
        timeout=3,
    )  # 输出: TimeoutError
    print(type(res))
    res = res.model_dump()
    # res.pop("globals")
    pprint.pprint(res)

    print("----- test process crash 2 -----")
    res = run_structured_in_subprocess(
        r"""
def recursive_crash(depth=0):
    # 打印当前递归深度（可选，用于观察）
    if depth%100==0:
        print(f"当前递归深度：{depth}")
    # 无限递归调用，直到触发深度限制
    recursive_crash(depth + 1)

# 运行崩溃（约 1000 层后报错）
try:
    recursive_crash()
except RecursionError as e:
    print(f"\n崩溃原因：{e}")
    raise e
""",
        my_globals,
        None,
        timeout=3,
    )  # 输出: TimeoutError
    print(type(res))
    res = res.model_dump()
    # res.pop("globals")
    pprint.pprint(res)

    print("----- test process crash 3 -----")
    res = run_structured_in_subprocess(
        r"""
def fast_memory_oom():
    large_str = ""
    count = 0
    while True:
        # 每次拼接 10MB 的字符串（"a" * 1024*1024*10，每个字符 1 字节，实际占用 ~10MB）
        large_str += "a" * (1024 * 1024 * 1024 * 512)
        count += 1
        if count%10 == 0:
            print(f"已拼接 {count} 次，当前字符串大小约 {count * 512} GB")

try:
    fast_memory_oom()
except MemoryError as e:
    print(f"\n崩溃原因：{e}")
""",
        my_globals,
        None,
        timeout=3,
    )  # 输出: TimeoutError
    print(type(res))
    res = res.model_dump()
    # res.pop("globals")
    pprint.pprint(res)

    print("----- test finish -----")


if __name__ == "__main__":
    test_structured_executor()


r"""

(algo-agent) D:\zyt\git_ln\algo_agent>D:/zyt/git_ln/algo_agent/.venv/Scripts/python.exe d:/zyt/git_ln/algo_agent/tests/playground/subprocess_output.py
----- timeout test -----
[2025-11-24 05:22:04,102]  ---------- 1. 超时情况：由父进程构建 ExecutionResult
[2025-11-24 05:22:04,116]  Pipe reader error: type=EOFError, value=, kv=EOFError(), traceback=Traceback (most recent call last):
  File "C:\Users\zooos\AppData\Roaming\uv\python\cpython-3.12.11-windows-x86_64-none\Lib\multiprocessing\connection.py", line 328, in _recv_bytes
    nread, err = ov.GetOverlappedResult(True)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
BrokenPipeError: [WinError 109] 管道已结束。

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "d:\zyt\git_ln\algo_agent\tests\playground\subprocess_output.py", line 88, in _reader
    msg: tuple[_PipeType, str | ExecutionResult] = parent_conn.recv()
                                                   ^^^^^^^^^^^^^^^^^^
  File "C:\Users\zooos\AppData\Roaming\uv\python\cpython-3.12.11-windows-x86_64-none\Lib\multiprocessing\connection.py", line 250, in recv
    buf = self._recv_bytes()
          ^^^^^^^^^^^^^^^^^^
  File "C:\Users\zooos\AppData\Roaming\uv\python\cpython-3.12.11-windows-x86_64-none\Lib\multiprocessing\connection.py", line 337, in _recv_bytes
    raise EOFError
EOFError

[2025-11-24 05:22:04,116]  ---------- 1. 子进程超时退出：超时 3 秒
<class 'src.runtime.schemas.ExecutionResult'>
{'arg_command': '\n'
                'import time\n'
                'print("Start sleeping...", flush=True)\n'
                'time.sleep(10)\n'
                'print("Finished sleeping.", flush=True)\n',
 'arg_globals': {'a': 123, 'b': [1, 2, 3]},
 'arg_timeout': 3,
 'exception_repr': None,
 'exception_traceback': None,
 'exception_type': None,
 'exception_value': None,
 'exit_code': -15,
 'exit_status': <ExecutionStatus.TIMEOUT: 'timeout'>,
 'ret_stdout': 'Start sleeping...\n',
 'ret_tool2llm': '代码执行超时，强制退出执行：\n执行超过3秒，未完成的代码输出为：\n'}
----- time ok test -----
[2025-11-24 05:22:04,791]  ---------- 2.1.1 子进程正常结束：子进程构建成功的 ExecutionResult
[2025-11-24 05:22:04,792]  Pipe reader error: type=EOFError, value=, kv=EOFError(), traceback=Traceback (most recent call last):
  File "C:\Users\zooos\AppData\Roaming\uv\python\cpython-3.12.11-windows-x86_64-none\Lib\multiprocessing\connection.py", line 317, in _recv_bytes
    ov, err = _winapi.ReadFile(self._handle, bsize,
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
BrokenPipeError: [WinError 109] 管道已结束。

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "d:\zyt\git_ln\algo_agent\tests\playground\subprocess_output.py", line 88, in _reader
    msg: tuple[_PipeType, str | ExecutionResult] = parent_conn.recv()
                                                   ^^^^^^^^^^^^^^^^^^
  File "C:\Users\zooos\AppData\Roaming\uv\python\cpython-3.12.11-windows-x86_64-none\Lib\multiprocessing\connection.py", line 250, in recv
    buf = self._recv_bytes()
          ^^^^^^^^^^^^^^^^^^
  File "C:\Users\zooos\AppData\Roaming\uv\python\cpython-3.12.11-windows-x86_64-none\Lib\multiprocessing\connection.py", line 337, in _recv_bytes
    raise EOFError
EOFError

[2025-11-24 05:22:04,869]  ---------- 2. 正常或异常退出：从子进程获取 ExecutionResult
[2025-11-24 05:22:04,869]  ---------- 2.1 子进程正常退出： exec正常、exec异常
<class 'src.runtime.schemas.ExecutionResult'>
{'arg_command': 'import time\nc = 10\nimport scipy\nprint("scipy imported")\n',
 'arg_globals': {'a': 123, 'b': [1, 2, 3], 'c': 10},
 'arg_timeout': 20000,
 'exception_repr': None,
 'exception_traceback': None,
 'exception_type': None,
 'exception_value': None,
 'exit_code': 0,
 'exit_status': <ExecutionStatus.SUCCESS: 'success'>,
 'ret_stdout': 'scipy imported\n',
 'ret_tool2llm': '代码执行成功，输出结果如下：\n'}
----- time exception test -----
[2025-11-24 05:22:05,220]  ---------- 2.1.2 子进程异常结束：子进程捕获堆栈，构建失败的 ExecutionResult
[2025-11-24 05:22:05,223]  Pipe reader error: type=EOFError, value=, kv=EOFError(), traceback=Traceback (most recent call last):
  File "C:\Users\zooos\AppData\Roaming\uv\python\cpython-3.12.11-windows-x86_64-none\Lib\multiprocessing\connection.py", line 317, in _recv_bytes
    ov, err = _winapi.ReadFile(self._handle, bsize,
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
BrokenPipeError: [WinError 109] 管道已结束。

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "d:\zyt\git_ln\algo_agent\tests\playground\subprocess_output.py", line 88, in _reader
    msg: tuple[_PipeType, str | ExecutionResult] = parent_conn.recv()
                                                   ^^^^^^^^^^^^^^^^^^
  File "C:\Users\zooos\AppData\Roaming\uv\python\cpython-3.12.11-windows-x86_64-none\Lib\multiprocessing\connection.py", line 250, in recv
    buf = self._recv_bytes()
          ^^^^^^^^^^^^^^^^^^
  File "C:\Users\zooos\AppData\Roaming\uv\python\cpython-3.12.11-windows-x86_64-none\Lib\multiprocessing\connection.py", line 337, in _recv_bytes
    raise EOFError
EOFError

[2025-11-24 05:22:05,292]  ---------- 2. 正常或异常退出：从子进程获取 ExecutionResult
[2025-11-24 05:22:05,292]  ---------- 2.1 子进程正常退出： exec正常、exec异常
<class 'src.runtime.schemas.ExecutionResult'>
{'arg_command': '\na = 123\nb = 0\nc = a/b\n',
 'arg_globals': {'a': 123, 'b': 0},
 'arg_timeout': 20000,
 'exception_repr': "ZeroDivisionError('division by zero')",
 'exception_traceback': 'Traceback (most recent call last):\n'
                        '  File '
                        '"d:\\zyt\\git_ln\\algo_agent\\tests\\playground\\subprocess_output.py", '
                        'line 41, in _worker_with_pipe\n'
                        '    exec(command, _globals, _locals)\n'
                        '  File "<string>", line 4, in <module>\n'
                        'ZeroDivisionError: division by zero\n',
 'exception_type': 'ZeroDivisionError',
 'exception_value': 'division by zero',
 'exit_code': 0,
 'exit_status': <ExecutionStatus.FAILURE: 'failure'>,
 'ret_stdout': '',
 'ret_tool2llm': '代码执行失败，代码报错如下：\n'
                 '原始代码：\n'
                 '1 | \n'
                 '2 | a = 123\n'
                 '3 | b = 0\n'
                 '4 | c = a/b\n'
                 '--------------------------------------------------\n'
                 '报错信息：\n'
                 'Traceback (most recent call last):\n'
                 '  File "<string>", line 4, in <module>\n'
                 'ZeroDivisionError: division by zero'}
----- test process crash -----
[2025-11-24 05:22:05,736]  Pipe reader error: type=EOFError, value=, kv=EOFError(), traceback=Traceback (most recent call last):
  File "C:\Users\zooos\AppData\Roaming\uv\python\cpython-3.12.11-windows-x86_64-none\Lib\multiprocessing\connection.py", line 328, in _recv_bytes
    nread, err = ov.GetOverlappedResult(True)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
BrokenPipeError: [WinError 109] 管道已结束。

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "d:\zyt\git_ln\algo_agent\tests\playground\subprocess_output.py", line 88, in _reader
    msg: tuple[_PipeType, str | ExecutionResult] = parent_conn.recv()
                                                   ^^^^^^^^^^^^^^^^^^
  File "C:\Users\zooos\AppData\Roaming\uv\python\cpython-3.12.11-windows-x86_64-none\Lib\multiprocessing\connection.py", line 250, in recv
    buf = self._recv_bytes()
          ^^^^^^^^^^^^^^^^^^
  File "C:\Users\zooos\AppData\Roaming\uv\python\cpython-3.12.11-windows-x86_64-none\Lib\multiprocessing\connection.py", line 337, in _recv_bytes
    raise EOFError
EOFError

[2025-11-24 05:22:05,740]  ---------- 2. 正常或异常退出：从子进程获取 ExecutionResult
[2025-11-24 05:22:05,741]  ---------- 2.2 子进程崩溃退出：如 SegFault
<class 'src.runtime.schemas.ExecutionResult'>
{'arg_command': '\n'
                '# 进程崩溃（如 SegFault），未发送结果即退出的例子\n'
                'import os\n'
                'try:\n'
                '    # 触发 SegFault\n'
                '    os._exit(139)\n'
                'except Exception as e:\n'
                '    print(f"\\n崩溃原因：{e}")\n',
 'arg_globals': {'a': 123, 'b': [1, 2, 3]},
 'arg_timeout': 3,
 'exception_repr': None,
 'exception_traceback': None,
 'exception_type': None,
 'exception_value': None,
 'exit_code': 139,
 'exit_status': <ExecutionStatus.CRASHED: 'crashed'>,
 'ret_stdout': '',
 'ret_tool2llm': '代码执行崩溃，进程异常退出：\n'}
----- test process crash 2 -----
[2025-11-24 05:22:06,169]  ---------- 2.1.2 子进程异常结束：子进程捕获堆栈，构建失败的 ExecutionResult
Process Process-5:
Traceback (most recent call last):
  File "C:\Users\zooos\AppData\Roaming\uv\python\cpython-3.12.11-windows-x86_64-none\Lib\multiprocessing\process.py", line 314, in _bootstrap
    self.run()
  File "C:\Users\zooos\AppData\Roaming\uv\python\cpython-3.12.11-windows-x86_64-none\Lib\multiprocessing\process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
  File "d:\zyt\git_ln\algo_agent\tests\playground\subprocess_output.py", line 63, in _worker_with_pipe
    child_conn.send((_PipeType.RESULT, res))
  File "C:\Users\zooos\AppData\Roaming\uv\python\cpython-3.12.11-windows-x86_64-none\Lib\multiprocessing\connection.py", line 206, in send
    self._send_bytes(_ForkingPickler.dumps(obj))
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\zooos\AppData\Roaming\uv\python\cpython-3.12.11-windows-x86_64-none\Lib\multiprocessing\reduction.py", line 51, in dumps
    cls(buf, protocol).dump(obj)
_pickle.PicklingError: Can't pickle <function recursive_crash at 0x000001A67C1EA7A0>: attribute lookup recursive_crash on __main__ failed
[2025-11-24 05:22:06,202]  Pipe reader error: type=EOFError, value=, kv=EOFError(), traceback=Traceback (most recent call last):
  File "C:\Users\zooos\AppData\Roaming\uv\python\cpython-3.12.11-windows-x86_64-none\Lib\multiprocessing\connection.py", line 328, in _recv_bytes
    nread, err = ov.GetOverlappedResult(True)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
BrokenPipeError: [WinError 109] 管道已结束。

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "d:\zyt\git_ln\algo_agent\tests\playground\subprocess_output.py", line 88, in _reader
    msg: tuple[_PipeType, str | ExecutionResult] = parent_conn.recv()
                                                   ^^^^^^^^^^^^^^^^^^
  File "C:\Users\zooos\AppData\Roaming\uv\python\cpython-3.12.11-windows-x86_64-none\Lib\multiprocessing\connection.py", line 250, in recv
    buf = self._recv_bytes()
          ^^^^^^^^^^^^^^^^^^
  File "C:\Users\zooos\AppData\Roaming\uv\python\cpython-3.12.11-windows-x86_64-none\Lib\multiprocessing\connection.py", line 337, in _recv_bytes
    raise EOFError
EOFError

[2025-11-24 05:22:06,260]  ---------- 2. 正常或异常退出：从子进程获取 ExecutionResult
[2025-11-24 05:22:06,260]  ---------- 2.2 子进程崩溃退出：如 SegFault
<class 'src.runtime.schemas.ExecutionResult'>
{'arg_command': '\n'
                'def recursive_crash(depth=0):\n'
                '    # 打印当前递归深度（可选，用于观察）\n'
                '    if depth%100==0:\n'
                '        print(f"当前递归深度：{depth}")\n'
                '    # 无限递归调用，直到触发深度限制\n'
                '    recursive_crash(depth + 1)\n'
                '\n'
                '# 运行崩溃（约 1000 层后报错）\n'
                'try:\n'
                '    recursive_crash()\n'
                'except RecursionError as e:\n'
                '    print(f"\\n崩溃原因：{e}")\n'
                '    raise e\n',
 'arg_globals': {'a': 123, 'b': [1, 2, 3]},
 'arg_timeout': 3,
 'exception_repr': None,
 'exception_traceback': None,
 'exception_type': None,
 'exception_value': None,
 'exit_code': 1,
 'exit_status': <ExecutionStatus.CRASHED: 'crashed'>,
 'ret_stdout': '当前递归深度：0\n'
               '当前递归深度：100\n'
               '当前递归深度：200\n'
               '当前递归深度：300\n'
               '当前递归深度：400\n'
               '当前递归深度：500\n'
               '当前递归深度：600\n'
               '当前递归深度：700\n'
               '当前递归深度：800\n'
               '当前递归深度：900\n'
               '\n'
               '崩溃原因：maximum recursion depth exceeded\n',
 'ret_tool2llm': '代码执行崩溃，进程异常退出：\n'}
----- test process crash 3 -----
[2025-11-24 05:22:06,650]  ---------- 2.1.1 子进程正常结束：子进程构建成功的 ExecutionResult
Process Process-6:
Traceback (most recent call last):
  File "C:\Users\zooos\AppData\Roaming\uv\python\cpython-3.12.11-windows-x86_64-none\Lib\multiprocessing\process.py", line 314, in _bootstrap
    self.run()
  File "C:\Users\zooos\AppData\Roaming\uv\python\cpython-3.12.11-windows-x86_64-none\Lib\multiprocessing\process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
  File "d:\zyt\git_ln\algo_agent\tests\playground\subprocess_output.py", line 63, in _worker_with_pipe
    child_conn.send((_PipeType.RESULT, res))
  File "C:\Users\zooos\AppData\Roaming\uv\python\cpython-3.12.11-windows-x86_64-none\Lib\multiprocessing\connection.py", line 206, in send
    self._send_bytes(_ForkingPickler.dumps(obj))
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\zooos\AppData\Roaming\uv\python\cpython-3.12.11-windows-x86_64-none\Lib\multiprocessing\reduction.py", line 51, in dumps
    cls(buf, protocol).dump(obj)
_pickle.PicklingError: Can't pickle <function fast_memory_oom at 0x0000026C387CA7A0>: attribute lookup fast_memory_oom on __main__ failed
[2025-11-24 05:22:06,678]  Pipe reader error: type=EOFError, value=, kv=EOFError(), traceback=Traceback (most recent call last):
  File "C:\Users\zooos\AppData\Roaming\uv\python\cpython-3.12.11-windows-x86_64-none\Lib\multiprocessing\connection.py", line 328, in _recv_bytes
    nread, err = ov.GetOverlappedResult(True)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
BrokenPipeError: [WinError 109] 管道已结束。

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "d:\zyt\git_ln\algo_agent\tests\playground\subprocess_output.py", line 88, in _reader
    msg: tuple[_PipeType, str | ExecutionResult] = parent_conn.recv()
                                                   ^^^^^^^^^^^^^^^^^^
  File "C:\Users\zooos\AppData\Roaming\uv\python\cpython-3.12.11-windows-x86_64-none\Lib\multiprocessing\connection.py", line 250, in recv
    buf = self._recv_bytes()
          ^^^^^^^^^^^^^^^^^^
  File "C:\Users\zooos\AppData\Roaming\uv\python\cpython-3.12.11-windows-x86_64-none\Lib\multiprocessing\connection.py", line 337, in _recv_bytes
    raise EOFError
EOFError

[2025-11-24 05:22:06,736]  ---------- 2. 正常或异常退出：从子进程获取 ExecutionResult
[2025-11-24 05:22:06,736]  ---------- 2.2 子进程崩溃退出：如 SegFault
<class 'src.runtime.schemas.ExecutionResult'>
{'arg_command': '\n'
                'def fast_memory_oom():\n'
                '    large_str = ""\n'
                '    count = 0\n'
                '    while True:\n'
                '        # 每次拼接 10MB 的字符串（"a" * 1024*1024*10，每个字符 1 字节，实际占用 '
                '~10MB）\n'
                '        large_str += "a" * (1024 * 1024 * 1024 * 512)\n'
                '        count += 1\n'
                '        if count%10 == 0:\n'
                '            print(f"已拼接 {count} 次，当前字符串大小约 {count * 512} '
                'GB")\n'
                '\n'
                'try:\n'
                '    fast_memory_oom()\n'
                'except MemoryError as e:\n'
                '    print(f"\\n崩溃原因：{e}")\n',
 'arg_globals': {'a': 123, 'b': [1, 2, 3]},
 'arg_timeout': 3,
 'exception_repr': None,
 'exception_traceback': None,
 'exception_type': None,
 'exception_value': None,
 'exit_code': 1,
 'exit_status': <ExecutionStatus.CRASHED: 'crashed'>,
 'ret_stdout': '\n崩溃原因：\n',
 'ret_tool2llm': '代码执行崩溃，进程异常退出：\n'}
----- test finish -----

(algo-agent) D:\zyt\git_ln\algo_agent>
"""
