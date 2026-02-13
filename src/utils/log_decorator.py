import logging
import os
from src.utils.path_util import static_path
from src.utils.lg_decorator_util.setup_logger import  setup_logger
from src.utils.lg_decorator_util.log_decorator_factory import log_decorator_factory
from src.utils.path_util import path_enum

# ------------------------------
# 预定义模块logger（不变）
# ------------------------------
# 子进程会出问题， 重新生成时间和文件夹

all_logger = setup_logger(
    logger_name="root.all", 
    log_file= static_path.File.ALL_LOG_PATH.resolve().as_posix(), 
    level=logging.DEBUG, 
    is_open_console=False)

global_logger = setup_logger(
    logger_name="root.all.print", 
    log_file= static_path.File.PRINT_LOG_PATH.resolve().as_posix(), 
    level=logging.DEBUG)

traceable = lambda func: log_decorator_factory(
    logger_name="root.all.trace",
    log_file= static_path.File.TRACE_LOG_PATH.resolve().as_posix(),
    exclude_args=["password", "token", "secret"],
    level=logging.DEBUG
)(func)
