import streamlit as st

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
async def msg_view():
    # === 5. 聊天界面（支持流式模拟） ===  
    st.subheader("5. 聊天界面（支持流式模拟）")  
      
    st.chat_message("ai").write("这是系统消息：欢迎使用模拟聊天界面！")  
    if "messages" in st.session_state:      
        for msg in st.session_state.messages[1:]:
            if msg["role"] == "user":
                st.chat_message("user").write(msg["content"])
            elif msg["role"] == "assistant":
                st.chat_message("assistant").markdown(msg["content"])
                st.chat_message("action").json(msg["tool_calls"])
            elif msg["role"] == "tool":
                st.chat_message("tool").markdown(msg["content"])
            else:
                st.error(f"未知角色：{msg}")
    
    if user_prompt := st.chat_input("请输入消息"):  
        if "messages" not in st.session_state:  
            st.session_state.messages = cache_msg.get_msg(user_prompt)

        st.chat_message("user").write(user_prompt)  
        # 模拟助手回复  
        with st.chat_message("assistant"):  
            my_list = ["Loading... "+str(i) + " " for i in range(10)]
            # message_placeholder = st.empty()  
            for ret_msg in msg_gen.gen_msg(st.session_state.messages):  
                # message_placeholder.markdown(full_response + "▌")  
                if ret_msg["role"] == "tool":
                    st.json(ret_msg["content"])
                elif ret_msg["role"] == "user":
                    st.chat_message("user").write(ret_msg["content"])
                elif ret_msg["role"] == "assistant":
                    st.chat_message("assistant").markdown(ret_msg["content"])
                else:
                    st.error(f"未知角色：{msg}")
