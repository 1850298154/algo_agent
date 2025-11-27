import logging
import os
import pprint
import time
import inspect
import json
from functools import wraps
import traceback
from typing import Callable, Optional, Dict, Any, Union, get_type_hints, Type
from datetime import datetime
from typing_extensions import get_origin, get_args  # 处理泛型（如 List、Dict）

from src.utils import create_folder


# ------------------------------
# 全局logger配置（不变）
# ------------------------------
def setup_logger(logger_name: str, log_file: Optional[str] = None, level: int = logging.DEBUG) -> logging.Logger:
    # ========== 关键修改： 自动创建日志目录 ==========
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir, exist_ok=True)  # exist_ok=True 避免目录已存在时报错
            print(f"日志目录不存在，已自动创建： {log_dir}")
        except Exception as e:
            print(f"创建日志目录失败： {e}")
            raise  # 抛出异常，避免后续创建文件失败
    if logger_name in logging.root.manager.loggerDict:
        return logging.getLogger(logger_name)

    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    logger.propagate = False

    # fmt = (
    #     "[%(asctime)s] [%(process)d:%(thread)d] [%(name)s] [%(levelname)s] "
    #     "[%(module)s.%(funcName)s:%(lineno)d] %(message)s"
    # ) # 没有 class
    fmt = "[%(asctime)s] [%(process)d:%(thread)d] [%(name)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s"
    fmt = "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s"
    fmt = "[%(asctime)s]  %(message)s"
    formatter = logging.Formatter(
        fmt=fmt,
        # datefmt="%Y-%m-%d %H:%M:%S.%f"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if log_file:
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,
            backupCount=5,
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

# ------------------------------
# 工具函数： 格式化复杂参数/返回值（不变）
# ------------------------------
def format_value(value: Any) -> str:
    @wraps(pprint.pformat)
    def pf(*args, **kwargs):
        """Format a Python object into a pretty-printed representation."""
        output_format_str = pprint.pformat(*args, **kwargs)
        # print(output_format_str+'\n')
        return output_format_str
    try:
        return pf(value)
        # return json.dumps(value, ensure_ascii=False, indent=2)
    except (TypeError, ValueError):
        if hasattr(value, "__dict__"):
            obj_dict = {k: v for i, (k, v) in enumerate(value.__dict__.items()) if i < 10}
            return f"[{value.__class__.__name__}] {json.dumps(obj_dict, ensure_ascii=False)}..."
        elif isinstance(value, (set, tuple)):
            return f"{type(value).__name__}({list(value)[:20]}..." if len(value) > 20 else f"{value}"
        else:
            str_val = str(value)
            return str_val[:500] + "..." if len(str_val) > 500 else str_val

# ------------------------------
# 新增工具函数： 根据返回值类型获取默认值
# ------------------------------
def get_default_return_value(func: Callable) -> Any:
    """
    根据函数返回值注解，生成对应的默认值（兜底用）
    支持： 基础类型、泛型（List/Dict/Tuple）、自定义类、None
    """
    try:
        # 获取返回值注解（处理无注解、字符串注解）
        type_hints = get_type_hints(func)
        return_type = type_hints.get("return", None)

        if return_type is None or return_type is type(None):
            # 无返回值注解或返回None： 返回None
            return None

        # 处理基础类型
        if return_type == int:
            return 0
        elif return_type == float:
            return 0.0
        elif return_type == str:
            return ""
        elif return_type == bool:
            return False
        elif return_type == list:
            return []
        elif return_type == dict:
            return {}
        elif return_type == tuple:
            return ()
        elif return_type == set:
            return set()

        # 处理泛型（如 List[int]、Dict[str, Any]）
        origin_type = get_origin(return_type)
        if origin_type:
            if origin_type == list:
                return []
            elif origin_type == dict:
                return {}
            elif origin_type == tuple:
                return ()
            elif origin_type == set:
                return set()

        # 处理自定义类（返回空实例）
        if inspect.isclass(return_type):
            try:
                return return_type()  # 尝试无参实例化
            except (TypeError, Exception):
                # 无参实例化失败： 返回None
                return None

        # 其他未覆盖类型： 返回None
        return None
    except Exception as e:
        # 解析类型注解失败： 返回None
        logging.warning(f"获取默认返回值失败： {str(e)}")
        return None

# ------------------------------
# 增强版日志装饰器（含异常兜底）
# ------------------------------
def log_function(
    logger_name: str,
    log_file: Optional[str] = None,
    level: int = logging.DEBUG,
    exclude_args: Optional[list] = None,
    record_stack: bool = True,
    default_return_value: Any = None  # 手动指定默认返回值（优先级高于自动推导）
) -> Callable:
    logger = setup_logger(logger_name, log_file, level)
    exclude_args = exclude_args or []

    def decorator(func: Callable) -> Callable:
        @wraps(func) # @wraps 的作用： 保留原函数元数据
        def wrapper(*args, **kwargs) -> Any:
            # 1. 获取核心上下文信息
            func_name = func.__name__
            module_name = inspect.getmodule(func).__name__
            class_name = "None"
            lineno = inspect.getsourcelines(func)[1]
            file_path = inspect.getfile(func)  # 新增：获取文件路径

            if args:
                first_arg = args[0]
                if hasattr(first_arg, func_name) and not inspect.isfunction(first_arg):
                    class_name = first_arg.__class__.__name__
                elif inspect.isclass(first_arg) and func_name in dir(first_arg):
                    class_name = first_arg.__name__

            stack_full_path = f"{module_name}.{class_name}.{func_name}"
            file_info = f"{os.path.basename(file_path)}:{lineno}"  # 新增：文件名:行号
            start_time = time.perf_counter()
            start_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

            # 2. 格式化参数
            # args_dict = {}
            # if args:
            #     if class_name != "None":
            #         args_dict["self/cls"] = f"{class_name}实例"
            #         args_dict.update({f"arg_{i+1}": format_value(arg) for i, arg in enumerate(args[1:])})
            #     else:
            #         args_dict.update({f"arg_{i+1}": format_value(arg) for i, arg in enumerate(args)})
            args_dict = pprint.pformat(args)
            # kwargs_filtered = {k: format_value(v) for k, v in kwargs.items() if k not in exclude_args}
            kwargs_filtered = pprint.pformat(kwargs)

            # 3. 记录调用开始
            logger.log(
                level,
                f"【调用开始】 栈路径： {stack_full_path} | 开始时间： {start_datetime} "
                f"| 位置参数： {args_dict} | 关键字参数： {kwargs_filtered}"
            )

            if record_stack:
                stack_info = inspect.stack()
                # stack_info = inspect.stack()[2:]
                def is_in_project(file_path):
                    project_root = os.path.abspath(os.getcwd())  # 获取项目根目录的绝对路径
                    stack_abs_path = os.path.abspath(file_path)
                    # Windows下忽略大小写，路径分隔符统一
                    return os.path.normcase(stack_abs_path).startswith(os.path.normcase(project_root))
                
                stack_str = "\n".join([f"          {frame.filename}:{frame.lineno} {frame.function}" 
                                        for frame in stack_info 
                                        if is_in_project(frame.filename) and not frame.function == "wrapper"])
                logger.debug(f"【调用栈】 \n{stack_str}")

            try:
                # 4. 执行原函数
                result = func(*args, **kwargs)

                # 5. 记录调用成功
                elapsed_time = (time.perf_counter() - start_time) * 1000
                formatted_result = format_value(result)
                logger.log(
                    level,
                    f"【调用成功】 栈路径： {stack_full_path} | 耗时： {elapsed_time:.3f}ms "
                    f"| 返回值： {formatted_result}"
                )
                return result

            except Exception as e:
                # 6. 异常处理： 记录日志 + 返回兜底默认值
                elapsed_time = (time.perf_counter() - start_time) * 1000
                exception_type = type(e).__name__
                exception_msg = str(e)
                exc_lineno = inspect.trace()[-1][2] if inspect.trace() else lineno
                traceback_str = traceback.format_exc()

                # 记录异常（保留完整堆栈）
                logger.error(
                    f"【调用失败】 栈路径： {stack_full_path} | 耗时： {elapsed_time:.3f}ms "
                    f"| 异常位置： {module_name}.{class_name}.{func_name}:{exc_lineno} "
                    f"| 异常类型： {exception_type} | 异常信息： {exception_msg} | 堆栈信息： {traceback_str}",
                    exc_info=True
                )

                # # 确定兜底返回值（手动指定优先，否则自动推导）
                # fallback_value = default_return_value if default_return_value is not None else get_default_return_value(func)
                # logger.warning(
                #     f"【异常兜底】 栈路径： {stack_full_path} | 返回默认值： {format_value(fallback_value)}"
                # )

                # return fallback_value  # 兜底返回，不抛出异常
                
                raise  # 修改为继续抛出异常

        return wrapper

    return decorator

# ------------------------------
# 预定义模块logger（支持手动指定默认值）
# ------------------------------
# agent_logger = lambda func: log_function(
#     logger_name="agent",
#     log_file="logs/agent.log",
#     level=logging.DEBUG
# )(func)

# # 召回模块： 手动指定默认返回值为[]（避免无结果时返回None）
# retrieval_logger = lambda func: log_function(
#     logger_name="retrieval",
#     log_file="logs/retrieval.log",
#     level=logging.DEBUG,
#     record_stack=True,
#     default_return_value=[]  # 异常时返回空列表
# )(func)

# algorithm_logger = lambda func: log_function(
#     logger_name="algorithm",
#     level=logging.DEBUG,
#     default_return_value=None  # 算法异常时返回None
# )(func)

# # 子进程会出问题， 重新生成时间和文件夹
# sub_folder_for_logs = create_folder.get_or_create_subfolder(gen_time_path_from_project="logs")
sub_folder_for_logs = "logs"
traceable_logger_file = os.path.join(sub_folder_for_logs, "trace.log")
traceable = lambda func: log_function(
    logger_name="all.trace",
    log_file=traceable_logger_file,
    exclude_args=["password", "token", "secret"],
    level=logging.DEBUG
)(func)

global_logger_file = os.path.join(sub_folder_for_logs, "print.log")
global_logger = setup_logger(
    logger_name="all.print", log_file=global_logger_file, level=logging.DEBUG)

all_logger_file = os.path.join(sub_folder_for_logs, "all.log")
all_logger = setup_logger(
    logger_name="all", log_file=all_logger_file, level=logging.DEBUG)



# test
if __name__ == "__main__":
    @traceable
    def test_function(a: int, b: str, c: Dict[str, Any]) -> Dict[str, Any]:
        """测试函数，故意抛出异常"""
        # return {"result": a + int(b) + c["key"]}
        return True

    # 正常调用
    ret = test_function(1, "2", {"key": 3})
    global_logger.debug(f"结果是{ret}")

    # # 异常调用
    # print(test_function(1, "2", {"key": "not_an_int"}))