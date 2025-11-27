
import os
from datetime import datetime

def get_or_create_subfolder(*, fix_relate_from_project=None, gen_time_path_from_project="./ws"):
    if fix_relate_from_project:
        fix_relate_from_project = os.path.abspath(fix_relate_from_project)
        os.makedirs(fix_relate_from_project, exist_ok=True)
        return fix_relate_from_project
    
    gen_time_path = gen_time_path_from_project
    gen_time_path = os.path.abspath(gen_time_path)
        
    # 确保父目录存在
    os.makedirs(gen_time_path, exist_ok=True)
    # 获取当前子文件夹数量（仅统计目录，排除文件）
    subfolder_count = len([f for f in os.listdir(gen_time_path) if os.path.isdir(os.path.join(gen_time_path, f))])

    # 计算下一个序号，并格式化为4位（不足补0）
    next_seq = subfolder_count + 1
    seq_str = f"{next_seq:04d}"  # 关键：用 :04d 格式化为4位，不足补0
    
    # 生成精确到微秒的时间字符串
    time_str = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    # 拼接子文件夹名（序号+时间）
    subfolder_name = f"{seq_str}_{time_str}"
    # 完整路径
    subfolder_path = os.path.join(gen_time_path, subfolder_name)
    # 创建子文件夹
    os.makedirs(subfolder_path, exist_ok=False)
    return subfolder_path

if __name__ == "__main__":
    subfolder_path = get_or_create_subfolder(gen_time_path_from_project="logs")
    print(subfolder_path)