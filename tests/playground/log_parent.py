import logging
from logging.handlers import RotatingFileHandler

# 第一步：配置父日志器 log3（接收 log1、log2 的日志）
def setup_loggers():
    # 1. 获取/创建日志器
    log3 = logging.getLogger("log3")  # 父日志器
    log1 = logging.getLogger("log3.log1")  # 子日志器1
    log2 = logging.getLogger("log3.log2")  # 子日志器2

    # 2. 设置日志级别（日志器级别需 ≤ 处理器级别才会输出）
    log3.setLevel(logging.DEBUG)
    log1.setLevel(logging.DEBUG)
    log2.setLevel(logging.DEBUG)

    # 3. 创建日志格式
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 4. 给 log3 添加文件处理器（输出到 log3.log）
    log3_handler = RotatingFileHandler(
        "log3.log", maxBytes=1024*1024, backupCount=5, encoding="utf-8"
    )
    log3_handler.setLevel(logging.DEBUG)
    log3_handler.setFormatter(formatter)
    log3.addHandler(log3_handler)

    # 5. 给 log1、log2 分别添加独立的文件处理器（输出到各自文件）
    # log1 处理器（输出到 log1.log）
    log1_handler = RotatingFileHandler(
        "log1.log", maxBytes=1024*1024, backupCount=5, encoding="utf-8"
    )
    log1_handler.setLevel(logging.DEBUG)
    log1_handler.setFormatter(formatter)
    log1.addHandler(log1_handler)

    # log2 处理器（输出到 log2.log）
    log2_handler = RotatingFileHandler(
        "log2.log", maxBytes=1024*1024, backupCount=5, encoding="utf-8"
    )
    log2_handler.setLevel(logging.DEBUG)
    log2_handler.setFormatter(formatter)
    log2.addHandler(log2_handler)

    # 禁用日志器的向上传播（避免重复输出到 root 日志器）
    # log3.propagate = False

    return log1, log2, log3

# 第二步：使用日志器
if __name__ == "__main__":
    log1, log2, log3 = setup_loggers()

    # 输出日志
    log1.info("这是 log1 的信息日志")
    log1.error("这是 log1 的错误日志")

    log2.info("这是 log2 的信息日志")
    log2.warning("这是 log2 的警告日志")

    log3.info("这是 log3 自身的信息日志")

    print("日志输出完成！请查看 log1.log、log2.log、log3.log 文件")