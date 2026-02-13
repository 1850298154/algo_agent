import streamlit as st
import shutil
import os
from pathlib import Path

from torch import log_

from src.ui.file_upload import files_model
from src.ui.cache_unchange import cache_path



def save_uploaded_files():
    # 3. 批量高效保存文件（核心逻辑）
    if files_model.uploaded_files:
        st.write(f"开始保存 {len(files_model.uploaded_files)} 个文件...")
        
        for file in files_model.uploaded_files:
            try:
                # 直接覆盖同名文件（不做重命名）
                save_dir = cache_path.get_cached_save_dir()
                save_dir.mkdir(parents=True, exist_ok=True)
                file_path = save_dir / file.name
                
                # 最快保存方式：shutil.copyfileobj（C实现，分块拷贝）
                with open(file_path, "wb") as f:
                    # 重置文件指针（避免上传的文件流指针偏移导致漏写）
                    file.seek(0)
                    # 块大小设为 1MB（超大文件可设更大，如 4MB）
                    shutil.copyfileobj(file, f, length=1024*1024)
                
                st.success(f"✅ {file.name} 保存成功 → {file_path}")
            
            except Exception as e:
                st.error(f"❌ {file.name} 保存失败：{str(e)}")
            finally:
                # 关闭文件流（释放资源，避免句柄泄露）
                file.close()
    file_list = list(cache_path.get_cached_save_dir().iterdir())
    print('file_list', file_list, len(file_list))
    pass

