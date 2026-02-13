import streamlit as st
import json

async def msg_role_view(msg):
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    elif msg["role"] == "assistant":
        # if "reasoning_content" in msg:
        #     st.chat_message("reasoning_content", avatar="🧑‍💻").write(msg["reasoning_content"])
        
        st.chat_message("assistant").write(msg["content"])
        
        if "tool_calls" in msg and msg["tool_calls"]:
            # st.chat_message("tool_calls").write(msg["tool_calls"])
            for tool_call in msg["tool_calls"]:
                # st.chat_message("tool_calls").write(tool_call)
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
        st.chat_message("tool").write(msg["content"])
    else:
        st.chat_message("unknown").write(msg)
