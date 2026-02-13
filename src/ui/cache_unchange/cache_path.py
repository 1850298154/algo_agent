import streamlit as st
from pathlib import Path
from src.utils.path_util import static_path
from src.utils.path_util import path_enum

@st.cache_data  
def get_cached_save_dir() -> Path:
    # 2. 定义保存目录（确保目录存在）
    save_dir = static_path.Dir.UPLOAD_DIR
    save_list = list(save_dir.iterdir())
    print('save_list', save_list)
    return save_dir
