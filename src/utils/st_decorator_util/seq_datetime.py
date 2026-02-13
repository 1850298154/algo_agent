
import os
import sys
from datetime import datetime
from src.utils.path_util import path_enum
from src.utils.st_decorator_util import st_cache_decorator
from src.utils.st_decorator_util.st_cache_decorator import conditional_cache

# @st_cache_decorator.conditional_cache(package_name='streamlit')
# @st_cache_decorator.conditional_cache
@st_cache_decorator.conditional_cache()
def _get_num_start_datetime() -> str:
    dir_rel_to_proj:str = path_enum.ProjPathEnum.LOG_DIR_NAME.value
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
print('全局时间标签实例:', GLOBAL_TIME_TAG_INSTANCE)
pass
