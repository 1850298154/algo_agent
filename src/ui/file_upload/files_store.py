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
                # 避免文件名重复：在文件名后加序号（可选但推荐）
                file_path = cache_path.get_save_dir() / file.name
                counter = 1
                while file_path.exists():
                    # 处理重复文件名：如 "test.txt" → "test_1.txt"
                    stem = file_path.stem
                    suffix = file_path.suffix
                    file_path = cache_path.get_save_dir() / f"{stem}_{counter}{suffix}"
                    counter += 1
                
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
    file_list = list(cache_path.get_save_dir().iterdir())
    print('file_list', file_list, len(file_list))
    pass