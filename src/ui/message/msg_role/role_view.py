import streamlit as st
import json
from src.ui.md_png import md_png
from src.ui.message.msg_role import role_model
async def msg_role_view(msg:dict):
    
    md_png_content = md_png.md_local_img_to_base64(msg["content"])

    if msg["role"] == role_model.RoleNameEnum.USER:
        st.chat_message(
            name=role_model.RoleNameEnum.USER,
            avatar=role_model.AVATARS[role_model.RoleNameEnum.USER]
            ).write(md_png_content)
    
    elif msg["role"] == role_model.RoleNameEnum.ASSISTANT:
        with st.chat_message(
            name=role_model.RoleNameEnum.ASSISTANT,
            avatar=role_model.AVATARS[role_model.RoleNameEnum.ASSISTANT]
        ):
            if role_model.RoleNameEnum.REASONING_CONTENT in msg:
                st.chat_message(
                    role_model.RoleNameEnum.REASONING_CONTENT, 
                    avatar=role_model.AVATARS[role_model.RoleNameEnum.REASONING_CONTENT]
                    ).write(msg["reasoning_content"])
            
            st.chat_message(
                name=role_model.RoleNameEnum.ASSISTANT_CONTENT,
                avatar=role_model.AVATARS[role_model.RoleNameEnum.ASSISTANT_CONTENT]
                ).write(md_png_content)
        
            if "tool_calls" in msg and msg["tool_calls"]:
                with st.chat_message(
                    name=role_model.RoleNameEnum.TOOL_CALL,
                    avatar=role_model.AVATARS[role_model.RoleNameEnum.TOOL_CALL]
                    ):
                    for tool_call in msg["tool_calls"]:
                        func_content = tool_call["function"]
                        st.write("执行工具："+func_content["name"])
                        arg_dict = json.loads(func_content["arguments"])
                        if "tool_call_purpose" in arg_dict:
                            st.write("执行目标："+arg_dict["tool_call_purpose"])
                        if func_content["name"] == "execute_python_code" and "python_code_snippet" in arg_dict:
                            st.code(arg_dict['python_code_snippet'])
                        else:
                            st.write(arg_dict)
            
            if role_model.RoleNameEnum.FUNCTION_CALL in msg and msg[role_model.RoleNameEnum.FUNCTION_CALL]:
                st.chat_message(
                    name=role_model.RoleNameEnum.FUNCTION_CALL,
                    avatar=role_model.AVATARS[role_model.RoleNameEnum.FUNCTION_CALL]
                    ).write(msg[role_model.RoleNameEnum.FUNCTION_CALL])
                
            if role_model.RoleNameEnum.FINISH_REASON in msg and msg[role_model.RoleNameEnum.FINISH_REASON]:
                st.chat_message(
                    name=role_model.RoleNameEnum.FINISH_REASON,
                    avatar=role_model.AVATARS[role_model.RoleNameEnum.FINISH_REASON]
                ).write(msg[role_model.RoleNameEnum.FINISH_REASON])
    elif msg["role"] == role_model.RoleNameEnum.TOOL:
        st.chat_message(
            name=role_model.RoleNameEnum.TOOL,
            avatar=role_model.AVATARS[role_model.RoleNameEnum.TOOL]
            ).write(md_png_content)
    else:
        st.chat_message(
            name=role_model.RoleNameEnum.UNKNOWN,
            avatar=role_model.AVATARS[role_model.RoleNameEnum.UNKNOWN]
            ).write(msg)
