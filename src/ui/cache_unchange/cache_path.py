import streamlit as st
from pathlib import Path
from src.utils import create_folder
from src.utils import path_manager

# @st.cache_data  
def get_save_dir() -> Path:
    from src.utils import log_decorator
    # 2. 定义保存目录（确保目录存在）
    save_dir = Path(create_folder.create_subfolder_with_time_tag(dir_rel_to_proj=path_manager.PathEnum.WST_DIR_NAME.value)) / "uploaded_files"  # 将上传文件保存在日志目录下的子目录中，方便关联日志和文件

    save_dir.mkdir(exist_ok=True)  # 不存在则创建，存在则不报错
    save_list = list(save_dir.iterdir())
    print('save_list', save_list)
    return save_dir
