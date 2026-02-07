import logging
import os

# ------------------------------
# 全局logger配置（不变）
# ------------------------------
def setup_logger(
    logger_name: str, 
    log_file: str, 
    level: int = logging.DEBUG, 
    is_open_console: bool = True) -> logging.Logger:
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
    logger.propagate = True

    # fmt = (
    #     "[%(asctime)s] [%(process)d:%(thread)d] [%(name)s] [%(levelname)s] "
    #     "[%(module)s.%(funcName)s:%(lineno)d] %(message)s"
    # ) # 没有 class
    fmt = "[%(asctime)s] [%(process)d:%(thread)d] [%(name)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s"
    fmt = "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s"
    fmt = "[%(asctime)s]  %(message)s"
    formatter = logging.Formatter(fmt=fmt)
    
    if is_open_console:
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