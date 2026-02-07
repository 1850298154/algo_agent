
import os
from datetime import datetime
from src.utils import num_start_datetime
from src.utils import path_manager

def create_subfolder_with_time_tag(dir_rel_to_proj:str) -> str:
    time_parent_path = os.path.abspath(dir_rel_to_proj)
    # 确保父目录存在
    os.makedirs(time_parent_path, exist_ok=True)
    # 使用全局唯一的时间标签作为子文件夹名（序号+时间）
    subfolder_name = num_start_datetime.GLOBAL_TIME_TAG_INSTANCE
    # 完整路径
    subfolder_path = os.path.join(time_parent_path, subfolder_name)
    # 创建子文件夹，如果存在则不报错，直接使用
    os.makedirs(subfolder_path, exist_ok=True)
    return subfolder_path
