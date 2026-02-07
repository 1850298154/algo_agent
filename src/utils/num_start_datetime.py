
import os
from datetime import datetime
from src.utils import path_manager

def _get_num_start_datetime() -> str:
    """
    1. logs文件夹下的文件数量基准序列
    2. 生成一个新的 序号+年月日+时分秒+微秒 的字符串
    3. 格式为 0001_20240624_153045_123456
    4. 可以作为整个进程创建 工作空间路径 和 log的基准
    """
    dir_rel_to_proj:str = path_manager.PathEnum.LOG_DIR_NAME.value
    time_parent_path = os.path.abspath(dir_rel_to_proj)
    # 确保父目录存在
    os.makedirs(time_parent_path, exist_ok=True)
    # 获取当前子文件夹数量（仅统计目录，排除文件）
    subfolder_count = len([f for f in os.listdir(time_parent_path) if os.path.isdir(os.path.join(time_parent_path, f))])

    # 计算下一个序号，并格式化为4位（不足补0）
    next_seq = subfolder_count + 1
    seq_str = f"{next_seq:04d}"  # 关键：用 :04d 格式化为4位，不足补0
    
    # 生成精确到微秒的时间字符串
    time_str = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    # 拼接子文件夹名（序号+时间）
    num_datetime_name = f"{seq_str}_{time_str}"
    return num_datetime_name

GLOBAL_TIME_TAG_INSTANCE = _get_num_start_datetime()
