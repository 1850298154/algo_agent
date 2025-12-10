
import sys
import os
from datetime import datetime
from src.utils import global_logger
from src.utils import create_folder


def create_cwd(cwd=None):
    """
    子进程的包装函数，用于在执行实际任务前更改工作目录。
    """
    cwd = create_folder.get_or_create_subfolder(fix_relate_from_project=cwd)

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
    

class ChangeDirectory:
    """目录切换上下文管理器，退出时自动恢复原目录"""
    def __init__(self, target_dir):
        self.target_dir = target_dir  # 目标目录
        self.original_dir = None      # 保存原目录
    
    def __enter__(self):
        # 1. 记录当前工作目录（原目录）
        self.original_dir = os.getcwd()
        # 2. 确保目标目录存在（可选，根据你的需求）
        cwd = create_folder.get_or_create_subfolder(fix_relate_from_project=self.target_dir)
        global_logger.info(f"切换目录到: {cwd}")
        # 3. 切换到目标目录
        os.chdir(cwd)
        # 返回当前上下文（可选，可用于链式操作）
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # 无论是否发生异常，都恢复原目录
        if self.original_dir:
            os.chdir(self.original_dir)
            global_logger.info(f"恢复目录到: {self.original_dir}")
        # 若返回 False，异常会向上抛出；返回 True 则抑制异常（按需选择）
        return False

class Change_STDOUT_STDERR:
    """标准输出切换上下文管理器，退出时自动恢复原输出"""
    def __init__(self, new_stdout, new_stderr=None):
        self.original_stdout = sys.stdout   # 保存原标准输出
        self.original_stderr = sys.stderr   # 保存原标准错误输出
        self.new_stdout = new_stdout  # 新的标准输出
        self.new_stderr = new_stderr or new_stdout  # 新的标准错误输出
    
    def __enter__(self):
        # 1. 记录当前标准输出（原输出）
        # 2. 切换到新的标准输出
        sys.stdout = self.new_stdout
        sys.stderr = self.new_stderr
        # 返回当前上下文（可选，可用于链式操作）
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # 无论是否发生异常，都恢复原标准输出
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr
        # 若返回 False，异常会向上抛出；返回 True 则抑制异常（按需选择）
        return False

# ------------------- 使用示例 -------------------
if __name__ == "__main__":
    # create_cwd()
    # 初始目录
    print("初始目录:", os.getcwd())
    
    # 使用 with 切换目录，执行完自动恢复
    with ChangeDirectory('./wsm/3/g8-1'):
        print("with内目录:", os.getcwd())
        # 在这里执行你的业务逻辑（比如文件操作、数据处理等）
        # ...
    
    # 退出with后，目录已恢复
    print("恢复后目录:", os.getcwd())