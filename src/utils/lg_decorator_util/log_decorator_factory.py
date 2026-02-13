import logging
import os
import pprint
import time
import inspect
from functools import wraps
import traceback
from typing import Callable, Optional, Dict, Any, Union, get_type_hints, Type, Awaitable
from datetime import datetime
from src.utils.lg_decorator_util.format_value import  format_value
from src.utils.lg_decorator_util.setup_logger import  setup_logger

# ------------------------------
# 新增：抽离公共逻辑（同步/异步共用）
# ------------------------------
def _get_function_context(func: Callable, args: tuple) -> Dict[str, Any]:
    """获取函数上下文信息（同步/异步共用）"""
    func_name = func.__name__
    module = inspect.getmodule(func)
    module_name = module.__name__ if module else "None"
    class_name = "None"
    lineno = inspect.getsourcelines(func)[1]
    file_path = inspect.getfile(func)
    # file_path += "\n\n"
    # file_path +=(inspect.getsourcefile(func))
    # file_path += "\n\n"
    # file_path += func.__globals__.get("__file__", "None")
    # file_path += "\n\n"

    if args:
        first_arg = args[0]
        if hasattr(first_arg, func_name) and not inspect.isfunction(first_arg):
            class_name = first_arg.__class__.__name__
        elif inspect.isclass(first_arg) and func_name in dir(first_arg):
            class_name = first_arg.__name__

    stack_full_path = f"{module_name}.{class_name}.{func_name}"
    file_info = f"{os.path.basename(file_path)}:{lineno}"
    file_info = f"{file_path}:{lineno}"
    start_time = time.perf_counter()
    start_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    return {
        "func_name": func_name,
        "stack_full_path": stack_full_path,
        "start_time": start_time,
        "start_datetime": start_datetime,
        "file_info": file_info
    }

def _log_call_start(logger: logging.Logger, level: int, context: Dict[str, Any], args: tuple, kwargs: dict, exclude_args: list):
    """记录调用开始日志（同步/异步共用）"""
    args_dict = pprint.pformat(args)
    kwargs_filtered = pprint.pformat({k: v for k, v in kwargs.items() if k not in exclude_args})
    
    logger.log(
        level,
        f"\n| 【调用开始】 "
        f"\n| 开始： {context['start_datetime']} "
        f"\n| 文件： {context['file_info']}"
        f"\n| 栈帧： {context['stack_full_path']} "
        f"\n| 位置参数：   {args_dict} "
        f"\n| 关键字参数： {kwargs_filtered}"
    )

def _log_call_stack(logger: logging.Logger, record_stack: bool):
    """记录调用栈（同步/异步共用）"""
    if record_stack:
        stack_info = inspect.stack()
        def is_in_project(file_path):
            project_root = os.path.abspath(os.getcwd())  # 获取项目根目录的绝对路径
            stack_abs_path = os.path.abspath(file_path)
            # Windows下忽略大小写，路径分隔符统一
            return os.path.normcase(stack_abs_path).startswith(os.path.normcase(project_root))
        
        stack_str = "\n".join([f"          {frame.filename}:{frame.lineno} {frame.function}" 
                                for frame in stack_info 
                                if is_in_project(frame.filename) and not frame.function == "wrapper"])
        logger.debug(f"【调用栈】 \n{stack_str}")

def _log_call_success(logger: logging.Logger, level: int, context: Dict[str, Any], result: Any):
    """记录调用成功日志（同步/异步共用）"""
    elapsed_time = (time.perf_counter() - context["start_time"]) * 1000
    formatted_result = format_value(result)
    logger.log(
        level,
        f"\n| 【调用成功】"
        f"\n| 耗时： {elapsed_time:.3f}ms "
        f"\n| 文件： {context['file_info']} "
        f"\n| 栈帧： {context['stack_full_path']}  "
        f"\n| 返回值： {formatted_result}"
    )

def _log_call_failure(logger: logging.Logger, level: int, context: Dict[str, Any], e: Exception):
    """记录调用失败日志（同步/异步共用）"""
    elapsed_time = (time.perf_counter() - context["start_time"]) * 1000
    exception_type = type(e).__name__
    exception_msg = str(e)
    if inspect.trace()[-1]:
        exc_filepath = inspect.trace()[-1].filename
        exc_lineno   = inspect.trace()[-1].lineno
        exc_func     = inspect.trace()[-1].function
    traceback_str = traceback.format_exc()

    logger.error(
        f"【调用失败】"
        f"\n| 耗时： {elapsed_time:.3f}ms "
        f"\n| 文件： {context['file_info']} "
        f"\n| 栈帧： {context['stack_full_path']} "
        f"\n| 异常位置： {exc_filepath}:{exc_lineno} {exc_func} "
        f"\n| 异常类型： {exception_type} "
        f"\n| 异常信息： {exception_msg} "
        f"\n| 堆栈信息： _________________________"
        f"\n{traceback_str}¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯",
        # exc_info=True,
    )

# ------------------------------
# 增强版日志装饰器（支持协程 + 异常兜底）
# ------------------------------
def log_decorator_factory(
    logger_name: str,
    log_file: str,
    level: int = logging.DEBUG,
    exclude_args: Optional[list] = None,
    record_stack: bool = True,
    default_return_value: Any = None
) -> Callable:
    logger = setup_logger(logger_name, log_file, level)
    exclude_args = exclude_args or []

    def decorator(func: Callable) -> Union[Callable, Awaitable]:
        @wraps(func)  # 保留原函数元数据
        def sync_wrapper(*args, **kwargs) -> Any:
            """同步函数的wrapper"""
            # 1. 获取上下文 + 记录调用开始
            context = _get_function_context(func, args)
            _log_call_start(logger, level, context, args, kwargs, exclude_args)
            _log_call_stack(logger, record_stack)

            try:
                # 2. 执行同步函数
                result = func(*args, **kwargs)
                # 3. 记录成功日志
                _log_call_success(logger, level, context, result)
                return result
            except Exception as e:
                # 4. 记录失败日志 + 兜底
                _log_call_failure(logger, level, context, e)
                raise  # 继续抛出异常（也可返回default_return_value）

        @wraps(func)  # 保留原函数元数据
        async def async_wrapper(*args, **kwargs) -> Any:
            """协程函数的wrapper（新增）"""
            # 1. 复用公共逻辑：获取上下文 + 记录调用开始
            context = _get_function_context(func, args)
            _log_call_start(logger, level, context, args, kwargs, exclude_args)
            _log_call_stack(logger, record_stack)

            try:
                # 2. 执行协程函数（关键：必须用await）
                result = await func(*args, **kwargs)
                # 3. 复用公共逻辑：记录成功日志
                _log_call_success(logger, level, context, result)
                return result
            except Exception as e:
                # 4. 复用公共逻辑：记录失败日志 + 兜底
                _log_call_failure(logger, level, context, e)
                raise  # 继续抛出异常（也可返回default_return_value）

        # ========== 核心判断：根据函数类型返回对应的wrapper ==========
        if inspect.iscoroutinefunction(func):
            return async_wrapper  # 协程函数返回异步wrapper
        else:
            return sync_wrapper   # 同步函数返回同步wrapper

    return decorator
