
import os
from datetime import datetime

def get_or_create_subfolder(*, 
    fix_relate_from_project=None, 
    time_relate_from_project="./wsm"):

    if fix_relate_from_project:
        fix_path = os.path.abspath(fix_relate_from_project)
        os.makedirs(fix_path, exist_ok=True)
        return fix_path
    subfolder_path = create_subfolder_with_auto_time(time_relate_from_project)
    return subfolder_path

def create_subfolder_with_auto_time(dir_rel_to_proj:str) -> str:
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
    subfolder_name = f"{seq_str}_{time_str}"
    # 完整路径
    subfolder_path = os.path.join(time_parent_path, subfolder_name)
    # 创建子文件夹
    os.makedirs(subfolder_path, exist_ok=False)
    return subfolder_path

if __name__ == "__main__":
    subfolder_path = get_or_create_subfolder(time_relate_from_project="logs")
    print(subfolder_path)