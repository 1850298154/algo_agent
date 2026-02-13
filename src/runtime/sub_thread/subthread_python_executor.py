import inspect
import os
import threading
import sys
import traceback
from typing import Any, Dict, Optional, List

# 引入新定义的 Schema
from src.runtime.sub_thread.subthread_schemas import (
    ExecutionStatus, 
    ExecutionSuccess,
    ExecutionFailure,
    ExecutionTimeout,
    ExecutionCrashed,
    ExecutionResult, # 这是个 Union 类型别名
    ExecutionResultFromSubThread, # 这是个 Union 类型别名
)
from src.runtime.ctx_mgr import cwd
from src.runtime.ctx_mgr import timer_recorder
from src.runtime.before_thread import plt_back_chinese
from src.utils.log_decorator import global_logger, traceable
from src.utils.path_util import path_enum
from src.utils.path_util import static_path


def _worker_with_buffer(
    command: str,
    _globals: dict[str, Any] | None,
    _locals: Optional[Dict],
    timeout: Optional[float],
    exec_time_container: list[float],
    stdout_buffer: list[str],
    result_container: list[ExecutionResultFromSubThread],
) -> None:
    """
    在线程中执行命令。
    根据执行情况（成功/异常），向 result_container 中添加具体的 ExecutionResult 子类实例。
    """

    class _BufferWriter:
        def __init__(self, buffer: list[str]):
            self.buffer = buffer

        def write(self, msg: str):
            if msg:
                self.buffer.append(msg)

        def flush(self):
            pass

    res: ExecutionResultFromSubThread
    try:
        with cwd.Change_STDOUT_STDERR(_BufferWriter(stdout_buffer)):
            with timer_recorder.TimerRecorder(exec_time_container):
                exec(command, _globals, _locals)
        
        global_logger.info("---------- 2.1.1 子线程正常结束：构建 Success Result")
        
        # 实例化成功对象
        # 注意：这里会触发 schemas.py 中的 field_validate_globals 进行深拷贝
        res = ExecutionSuccess(
            arg_command=command,
            arg_timeout=timeout,
            arg_chg_globals=_globals or {},
            exec_timeout=exec_time_container[0] if exec_time_container else -1,
            ret_stdout="".join(stdout_buffer),
        )
        
    except Exception as e:
        global_logger.info("---------- 2.1.2 子线程异常结束：构建 Failure Result")
        
        def _filter_exec_traceback():
            exc_str = traceback.format_exc()
            # 按行拆分栈信息，过滤出 <string> 相关的行（exec 内部代码）
            lines = exc_str.splitlines()
            exec_lines = []
            # # 标记是否进入 exec 内部栈段（处理连续的栈行）
            # in_exec_block = False
            
            for line in lines:
                # 核心特征：包含 "<string>"（exec 执行字符串代码的标记）
                if "Traceback" in line:
                    exec_lines.append(line)
                elif "<string>" in line:
                    # in_exec_block = True
                    exec_lines.append(line)
                # 保留 exec 栈段的后续行（如出错代码行、异常描述）
                # elif in_exec_block:
                elif exec_lines and "<string>" in exec_lines[-1]:
                    # 终止条件：遇到新的栈帧（以 "File " 开头但不含 <string>）
                    if line.startswith("File ") and "<string>" not in line:
                        # in_exec_block = False
                        continue
                    exec_lines.append(line)
            # 重新拼接过滤后的字符串
            return "\n".join(exec_lines)

        # 实例化失败对象
        res = ExecutionFailure(
            arg_command=command,
            arg_timeout=timeout,
            exec_timeout=exec_time_container[0] if exec_time_container else -1,
            ret_stdout="".join(stdout_buffer),
            exception_repr=repr(e),
            exception_type=type(e).__name__,
            exception_value=str(e),
            exception_traceback=_filter_exec_traceback()
        )
    finally:
        # 将结果放入容器传回主线程
        # 注意：此时 res.ret_stdout 还是空的，因为 buffer 可能还没写完或需要在主线程合并
        result_container.append(res)

@traceable
def run_structured_in_thread(
    command: str,
    _globals: dict[str, Any] | None = None,
    _locals: Optional[Dict] = None,
    timeout: Optional[float] = None,
) -> ExecutionResult:
    _locals = _globals
    exec_time_container: list[float] = []
    stdout_buffer: list[str] = []
    result_container: list[ExecutionResult] = []

    t = threading.Thread(
        target=_worker_with_buffer,
        args=(command, _globals, _locals, timeout, exec_time_container, stdout_buffer, result_container),
    )
    
    target_dir_fullpath = static_path.Dir.PY_OUTPUT_DIR.resolve().as_posix()
    
    # 切换目录执行
    with cwd.ChangeDirectory(target_dir_fullpath):
        t.start()
        t.join(timeout)
    
    final_res: ExecutionResult

    if t.is_alive():
        global_logger.info("---------- 1. 超时情况：主线程构建 Timeout Result")
        # 线程超时，只能在主线程构建结果
        final_res = ExecutionTimeout(
            arg_command=command,
            arg_timeout=timeout,
            exec_timeout=max(
                timeout if timeout else 0, 
                exec_time_container[0] if exec_time_container else -1.0
            ),
            ret_stdout="".join(stdout_buffer),
        )
        # 注意：Python 线程无法强制 Kill，这里只是逻辑上的超时处理
    else:
        global_logger.info("---------- 2. 正常或异常退出")
        if result_container:
            global_logger.info("---------- 2.1 子线程返回结果 (Success 或 Failure)")
            final_res = result_container[0]
        else:
            global_logger.info("---------- 2.2 子线程崩溃 (Crashed)")
            # 这种情况比较少见于 Thread，通常发生于 Process，但作为兜底逻辑保留
            final_res = ExecutionCrashed(
                arg_command=command,
                arg_timeout=timeout,
                exec_timeout=exec_time_container[0] if exec_time_container else -1,
                ret_stdout="".join(stdout_buffer),
                exit_code=-1, # Thread 没有 exitcode，这里用 -1 标记未知错误
            )

    # 访问 .ret_tool2llm 属性时，会自动触发 @computed_field 计算逻辑，无需手动调用
    # 如果为了调试想看到 computed 字段，可以 print(final_res.model_dump())
    
    return final_res

if __name__ == "__main__":
    # --- 测试 Success ---
    print("\n>>> TEST: SUCCESS")
    test_code_success = "import os; print('Hello World'); x=10"
    res = run_structured_in_thread(test_code_success, {}, timeout=5)
    print(f"类型: {type(res)}")
    print(f"LLM View:\n{res.ret_tool2llm}")
    if isinstance(res, ExecutionSuccess):
        print(f"Globals Keys: {res.arg_chg_globals.keys()}")

    # --- 测试 Failure ---
    print("\n>>> TEST: FAILURE")
    test_code_fail = "print('Start'); 1/0"
    res = run_structured_in_thread(test_code_fail, {}, timeout=5)
    print(f"类型: {type(res)}")
    print(f"LLM View:\n{res.ret_tool2llm}")
    
    # --- 测试 Timeout ---
    print("\n>>> TEST: TIMEOUT")
    import time
    test_code_timeout = "import time; print('Sleep...'); time.sleep(2)"
    res = run_structured_in_thread(test_code_timeout, {}, timeout=1)
    print(f"类型: {type(res)}")
    print(f"LLM View:\n{res.ret_tool2llm}")