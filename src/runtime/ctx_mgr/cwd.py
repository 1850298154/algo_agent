
import sys
import os
from datetime import datetime
from src.utils import global_logger
from src.utils import create_folder

class ChangeDirectory:
    """目录切换上下文管理器，退出时自动恢复原目录"""
    def __init__(self, target_dir_fullpath: str):
        self.target_dir = target_dir_fullpath  # 目标目录
        # 1. 记录当前工作目录（原目录）
        self.original_dir = os.getcwd()      # 保存原目录
    
    def __enter__(self):
        # 2. 确保目标目录存在（可选，根据你的需求）
        global_logger.info(f"切换目录到: {self.target_dir}")
        # 3. 切换到目标目录
        os.chdir(self.target_dir)
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
