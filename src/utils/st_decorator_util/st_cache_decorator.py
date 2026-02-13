import os
import sys
from datetime import datetime
from typing import Callable, Any
# # 模拟 path_enum（如果你的项目中已有，可删除这部分模拟代码）
# class ProjPathEnum:
#     class LOG_DIR_NAME:
#         value = "logs"
# path_enum = ProjPathEnum

# -------------------------- 核心装饰器定义 --------------------------
# def conditional_cache(package_name: str = 'streamlit') -> Callable:
def conditional_cache() -> Callable:
    def decorator(func: Callable) -> Callable:
        package_name: str = 'streamlit'
        # 检查包是否已导入
        if package_name in sys.modules:
            # 动态导入包
            pkg = __import__(package_name)
            print(f"{package_name} 已经导入，版本：{pkg.__version__}")
            
            # 使用包的cache_data装饰函数
            @pkg.cache_data()
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                return func(*args, **kwargs)
            return wrapper
        else:
            print(f"{package_name} 尚未导入，保持原始逻辑")
            # 未导入则直接返回原函数
            return func
    return decorator

# # -------------------------- 原有业务函数 --------------------------
# def __get_num_start_datetime__() -> str:
#     """
#     1. logs文件夹下的文件数量基准序列
#     2. 生成一个新的 序号+年月日+时分秒+微秒 的字符串
#     3. 格式为 0001_20240624_153045_123456
#     4. 可以作为整个进程创建 工作空间路径 和 log的基准
#     """
#     dir_rel_to_proj: str = path_enum.LOG_DIR_NAME.value
#     time_parent_path = os.path.abspath(dir_rel_to_proj)
#     # 确保父目录存在
#     os.makedirs(time_parent_path, exist_ok=True)
#     # 获取当前子文件夹数量（仅统计目录，排除文件）
#     subfolder_count = len([f for f in os.listdir(time_parent_path) if os.path.isdir(os.path.join(time_parent_path, f))])

#     # 计算下一个序号，并格式化为4位（不足补0）
#     next_seq = subfolder_count + 1
#     seq_str = f"{next_seq:04d}"  # 关键：用 :04d 格式化为4位，不足补0
    
#     # 生成精确到微秒的时间字符串
#     time_str = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
#     # 拼接子文件夹名（序号+时间）
#     num_datetime_name = f"{seq_str}_{time_str}"
#     return num_datetime_name

# # -------------------------- 使用装饰器 --------------------------
# # 应用装饰器，指定要检查的包名（默认streamlit，可自定义）
# @conditional_cache(package_name='streamlit')
# def _get_num_start_datetime() -> str:
#     return __get_num_start_datetime__()

# # -------------------------- 测试执行 --------------------------
# GLOBAL_TIME_TAG_INSTANCE = _get_num_start_datetime()
# print('全局时间标签实例:', GLOBAL_TIME_TAG_INSTANCE)
# pass