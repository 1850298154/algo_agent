import copy
import os
import pickle
from re import A
from typing import Any, Dict, Optional, Union
from src.utils.log_decorator import global_logger, traceable
from src.utils.path_util import dynamic_path

def dump_globals(filter_out_globals, success_cnt) -> dict[str, Any]:
    path = dynamic_path.RunVarPath(success_cnt=success_cnt).path()
    with open(path, 'wb') as f:
        pickle.dump(filter_out_globals, f, protocol=pickle.HIGHEST_PROTOCOL)

def load_globals(path: str) -> dict[str, Any]:
    # # 获取所有的.pkl文件，按照文件名中的数字排序，加载最新的一个.pkl文件
    # pkl_files = [f 
    #              for f in os.listdir(globals_var_success_dir) 
    #              if f.endswith('.pkl')]
    # pkl_files.sort()
    # if not pkl_files:
    #     global_logger.warning(f"没有找到任何.pkl文件，无法加载globals变量。请确保至少有一个成功的globals变量被保存。")
    #     return {}
    # latest_file = pkl_files[-1]
    # path = os.path.join(globals_var_success_dir, latest_file)
    with open(path, 'rb') as f:
        return pickle.load(f)
