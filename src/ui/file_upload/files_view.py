import streamlit as st

from src.ui.file_upload import (
    files_model,
    files_store,
)
from src.ui.cache_unchange import (
    cache_path,
)
async def files_upload_view():

    st.subheader("数据上传与战略分析决策")  
    files_model.uploaded_files = st.file_uploader("上传多个文件", accept_multiple_files=True) 
    if files_model.uploaded_files:
        files_store.save_uploaded_files()
