from src.utils import global_logger, traceable

import llm
import action
import memory


@traceable
def user_query(user_input):
    user_hint = "用户输入："
    # user_input = input(user_hint)
    global_logger.info(f"{user_hint} ： {user_input}\n\n")

    messages = memory.init_messages(user_input)
    global_logger.info("-" * 60)
    
    # 模型的第一轮调用
    loop_cnt = 1
    first_response = llm.get_assistant(messages)
    global_logger.info(f"\n第{loop_cnt}轮大模型输出信息：{first_response}\n")
    
    if assistant_output.content is None:
        assistant_output.content = ""
    messages.append(assistant_output)
    
    
    # 如果不需要调用工具，则直接返回最终答案
    if (
        assistant_output.tool_calls == None
    ):  # 如果模型判断无需调用工具，则将assistant的回复直接打印出来，无需进行模型的第二轮调用
        global_logger.info(f"无需调用工具，我可以直接回复：{assistant_output.content}")
        return
    # 如果需要调用工具，则进行模型的多轮调用，直到模型判断无需调用工具
    while assistant_output.tool_calls != None:
        # 如果判断需要调用查询天气工具，则运行查询天气工具
        tool_info = {
            "content": "",
            "role": "tool",
            "tool_call_id": assistant_output.tool_calls[0].id,
            "tool_call_name": assistant_output.tool_calls[0].function.name,
            "tool_call_arguments": assistant_output.tool_calls[0].function.arguments,
        }

        action.call_tools_safely(tool_info, assistant_output)

        tool_output = tool_info["content"]
        global_logger.info(f"工具输出信息： {tool_output}\n")
        global_logger.info("-" * 60)
        messages.append(tool_info)
        loop_response = llm.generate_chat_completion(messages)
        assistant_output = loop_response.choices[0].message
        if assistant_output.content is None:
            assistant_output.content = ""
        messages.append(assistant_output)
        loop_cnt += 1
        global_logger.info(f"第{loop_cnt}轮大模型输出信息： {assistant_output}\n")
    global_logger.info(f"最终答案： {assistant_output.content}")

# 测试
if __name__ == "__main__":
    user_query("你好")