import streamlit as st
import json
from src.ui.md_png import md_png
async def msg_role_view(msg):
    
    png_content = md_png.md_local_img_to_base64(msg["content"])

    if msg["role"] == "user":
        st.chat_message("user").write(png_content)
    elif msg["role"] == "assistant":
        st.chat_message("assistant").write(png_content) 
        # if "reasoning_content" in msg:
        #     st.chat_message("reasoning_content", avatar="🧑‍💻").write(msg["reasoning_content"])
        
        if "tool_calls" in msg and msg["tool_calls"]:
            for tool_call in msg["tool_calls"]:
                func = tool_call.get("function")
                st.write(func["name"])
                arg =  json.loads(func["arguments"])
                if func["name"] == "execute_python_code":
                    st.write(arg["tool_call_purpose"])
                    st.code(arg['python_code_snippet'])
                else:
                    st.write(arg)
        
        if "function_call" in msg and msg["function_call"]:
            st.chat_message("function_call").write(msg["function_call"])
            
        if "finish_reason" in msg and msg["finish_reason"]:
            st.chat_message("finish_reason").write(msg["finish_reason"])
    elif msg["role"] == "tool":
        st.chat_message("tool").write(png_content)
    else:
        st.chat_message("unknown").write(msg)
