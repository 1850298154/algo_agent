import logging
import os
from src.utils import create_folder, path_manager
from src.utils.lg_decorator_util.setup_logger import  setup_logger
from src.utils.lg_decorator_util.log_call_start_end import log_function

# ------------------------------
# 预定义模块logger（不变）
# ------------------------------
# 子进程会出问题， 重新生成时间和文件夹
sub_folder_for_logs = create_folder.create_subfolder_with_time_tag(dir_rel_to_proj=path_manager.PathEnum.LOG_DIR_NAME.value)

all_logger = setup_logger(
    logger_name="root.all", 
    log_file=os.path.join(sub_folder_for_logs, "all.log"), 
    level=logging.DEBUG, 
    is_open_console=False)

global_logger = setup_logger(
    logger_name="root.all.print", 
    log_file=os.path.join(sub_folder_for_logs, "print.log"), 
    level=logging.DEBUG)

traceable = lambda func: log_function(
    logger_name="root.all.trace",
    log_file=os.path.join(sub_folder_for_logs, "trace.log"),
    exclude_args=["password", "token", "secret"],
    level=logging.DEBUG
)(func)
