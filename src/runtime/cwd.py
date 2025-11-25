
import os
from src.utils import global_logger

import os
from datetime import datetime

def _create_subfolder(base_path):
    # 确保父目录存在
    os.makedirs(base_path, exist_ok=True)
    # 获取当前子文件夹数量（仅统计目录，排除文件）
    subfolder_count = len([f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))])

    # 计算下一个序号，并格式化为4位（不足补0）
    next_seq = subfolder_count + 1
    seq_str = f"{next_seq:04d}"  # 关键：用 :04d 格式化为4位，不足补0
    
    # 生成精确到微秒的时间字符串
    time_str = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    # 拼接子文件夹名（序号+时间）
    subfolder_name = f"{seq_str}_{time_str}"
    # 完整路径
    subfolder_path = os.path.join(base_path, subfolder_name)
    # 创建子文件夹
    os.makedirs(subfolder_path, exist_ok=False)
    return subfolder_path


def create_cwd():
    """
    子进程的包装函数，用于在执行实际任务前更改工作目录。
    """
    cwd = "./ws" 
    # 转变成绝对路径（可选），兼容win和linux
    cwd = os.path.abspath(cwd)
    cwd = _create_subfolder(cwd)
    global_logger.info(f"子进程 PID: {os.getpid()} 要将工作目录更改为: {cwd}")
    if not cwd:
        return False
    try:
        os.chdir(cwd)
        global_logger.info(f"子进程 PID: {os.getpid()} 已将工作目录更改为: {os.getcwd()}")
        return True
    except OSError as e:
        global_logger.error(f"子进程 PID: {os.getpid()} 更改工作目录失败: {e}")
        # 根据需要处理错误，例如发送错误信息到主进程或直接退出
        return False
    except Exception as e:
        global_logger.error(f"子进程 PID: {os.getpid()} 更改工作目录时发生异常: {e}")
        return False
    

if __name__ == "__main__":
    create_cwd()