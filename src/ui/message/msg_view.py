from requests import session
import streamlit as st
from src.agent.msg import msg_mem

from src.ui.file_upload import files_model
from src.ui.cache_unchange import (
    cache_path,
)
from src.ui.message import (
    msg_gen,
    msg_view,
)
from src.ui.cache_unchange import (
    cache_path,
    cache_msg,
)
from src.ui.message.msg_role import (
    role_view,
)
from src.ui.file_upload import (
    files_model,
    files_store,
)
from src.ui.cache_unchange import (
    cache_path,
)
from src.utils.path_util import static_path


async def msg_view():
    # === 5. 聊天界面（支持流式模拟） ===  
    st.subheader("5. 聊天界面（支持流式模拟）")  
      
    st.chat_message("ai").write("这是系统消息：欢迎使用聊天界面！上传数据，给你最佳的分析和策略！")  
    if "msg_mem_obj" in st.session_state:      
        # 确认是否是同一个 id
        print(f"session msg_mem_obj id: {id(st.session_state.msg_mem_obj)}")
        msg_mem_obj: msg_mem.MessageMemory = st.session_state.msg_mem_obj
        for msg in msg_mem_obj.messages[1:]:  
            await role_view.msg_role_view(msg)
    
    if user_prompt := st.chat_input("请输入消息"):  
        if "msg_mem_obj" not in st.session_state:  
            user_prompt += ("\n\n上传的数据是："+
            "；".join(["文件名："+file.name + 
                 "，文件大小：" + str(file.size) + " 字节，" + 
                 "文件类型：" + file.type 
                 for file in files_model.uploaded_files]) + 
            "。\n上传数据的目录、执行python代码的启动路径和程序运行输出的工作路径都是："+static_path.Dir.UPLOAD_DIR.resolve().as_posix())
            st.session_state.msg_mem_obj = cache_msg.get_cached_msg(user_prompt)

        st.chat_message("user").write(user_prompt)  
        # with st.chat_message("assistant"):  
        async for ret_msg_mem_obj in msg_gen.gen_msg(st.session_state.msg_mem_obj):  
            ret_msg_list = ret_msg_mem_obj.messages
            ret_msg = ret_msg_list[-1]
            await role_view.msg_role_view(ret_msg)
        if st.session_state.msg_mem_obj.finish_reason == "stop":
            st.chat_message("system").write("对话已结束，检测到 finish_reason=stop")
        if st.session_state.msg_mem_obj.need_msg_stop_control(st.session_state.msg_mem_obj.msg_ctr_cfg):
            st.chat_message("system").write(st.session_state.msg_mem_obj.msg_ctr_cfg.model_dump())
            