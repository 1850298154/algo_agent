import streamlit as st

from src.ui.file_upload import (
    files_model,
    files_store,
)
from src.ui.cache_unchange import (
    cache_path,
)
async def files_upload_view():
    # === 侧边栏：模拟配置 ===  
    with st.sidebar:  
        st.markdown("### 配置")  
        enable_stream = st.checkbox("启用流式输出", value=True)  
    
    # === 页面标题 ===  
    st.title("🎈 上传文件")  
    st.caption(f"当前工作目录: {cache_path.get_save_dir()}")  

    # === 3. 文件上传与文本输入 ===  
    st.subheader("3. 文件上传与文本输入")  
    files_model.uploaded_files = st.file_uploader("上传多个文件", accept_multiple_files=True) 
    if files_model.uploaded_files:
        files_store.save_uploaded_files()
    files_model.files_discrip = st.text_input(  
        label="对文件的描述或提问",  
        placeholder="请输入问题",  
        disabled=not files_model.uploaded_files,  
    )  