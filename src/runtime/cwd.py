
import os
from datetime import datetime
from src.utils import global_logger
from src.utils import create_folder


def create_cwd(cwd=None):
    """
    子进程的包装函数，用于在执行实际任务前更改工作目录。
    """
    cwd = create_folder.get_or_create_subfolder(fix_relate_from_project=cwd)

    # global_logger.info(f"子进程 PID: {os.getpid()} 要将工作目录更改为: {cwd}")
    if not cwd:
        return False
    try:
        os.chdir(cwd)
        # global_logger.info(f"子进程 PID: {os.getpid()} 已将工作目录更改为: {os.getcwd()}")
        return True
    except OSError as e:
        # global_logger.error(f"子进程 PID: {os.getpid()} 更改工作目录失败: {e}")
        # 根据需要处理错误，例如发送错误信息到主进程或直接退出
        return False
    except Exception as e:
        # global_logger.error(f"子进程 PID: {os.getpid()} 更改工作目录时发生异常: {e}")
        return False
    

if __name__ == "__main__":
    create_cwd()