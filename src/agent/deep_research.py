import pprint
from openai.types.chat.chat_completion import ChatCompletionMessage

from src.utils import global_logger, traceable

import llm
import action
import memory
import tool
import tool.schema
import tool.python_tool
import tool.todo_tool


def user_query(user_input):
    user_hint = "用户输入："
    global_logger.info(f"{user_hint} ： {user_input}\n\n")

    messages = memory.init_messages_with_system_prompt(user_input)
    tools_schema_list = tool.schema.get_tools_schema([
        tool.python_tool.ExecutePythonCodeTool,
        # tool.todo_tool.RecursivePlanTreeTodoTool,
        ])

    # 模型的第一轮调用
    assistant_output: ChatCompletionMessage = llm.generate_assistant_output_append(messages, tools_schema_list)
    if not llm.has_tool_call(assistant_output) and not llm.has_function_call(assistant_output):
        global_logger.info(f"无需调用工具，我可以直接回复：{assistant_output.content}")
        return

    # 如果需要调用工具，则进行模型的多轮调用，直到模型判断无需调用工具
    while llm.has_tool_call(assistant_output) or llm.has_function_call(assistant_output):
        if llm.has_function_call(assistant_output):
            tool_info = {
                "content": "",
                "role": "function",
                "tool_call_id": "",
                # 其他非必须
                "tool_call_name": assistant_output.function_call.name,
                "tool_call_arguments": assistant_output.function_call.arguments,
            }            
            action.call_tools_safely(tool_info)
            tool_output = tool_info["content"]
            global_logger.info(f"工具 function call 输出信息： {tool_output}\n")
            global_logger.info("-" * 60)
            messages.append(tool_info)
        if llm.has_tool_call(assistant_output):
            for i in range(len(assistant_output.tool_calls)):
                # 如果判断需要调用查询天气工具，则运行查询天气工具
                tool_info = {
                    "content": "",
                    "role": "tool",
                    "tool_call_id": assistant_output.tool_calls[i].id,
                    # 其他非必须
                    "tool_call_name": assistant_output.tool_calls[i].function.name,
                    "tool_call_arguments": assistant_output.tool_calls[i].function.arguments,
                }

                action.call_tools_safely(tool_info)

                tool_output = tool_info["content"]
                global_logger.info(f"工具 tool call 输出信息： {tool_output}\n")
                global_logger.info("-" * 60)
                messages.append(tool_info)
        assistant_output = llm.generate_assistant_output_append(messages, tools_schema_list)
        if assistant_output.content is None:
            assistant_output.content = ""
        global_logger.info(
            f"""第{len(messages) // 2}轮大模型输出信息： 
\n\nassistant_output.content:: \n\n {pprint.pformat(assistant_output.content)}
\n\nassistant_output.tool_calls::\n\n {pprint.pformat(assistant_output.tool_calls.model_dump())}\n"""
        )
    global_logger.info(f"最终答案： {assistant_output.content}")

# 测试
if __name__ == "__main__":
    data_info = """
你所在的工作路径下面，可以用python工具  ExecutePythonCodeTool  写一段包含读取json文件的代码，读取一下文件
例如：“
import json
with open('schema.json', 'r', encoding='utf-8') as file:
    schema = json.load(file)
    print(json.dumps(schema, indent=2))
”，读取以下文件：
1. **schema.json** - 完整的数据结构Schema定义
2. **{data_file}** 场景数据。
3. 不要输出文件内容，因为数量会很大，只需按照schema.json中定义的字段读取部分内容进行分析。
""".format(
        data_file="deep_research_scene_data.json"
        ) 
    # 要把数据放到工作路径下，  同时修改工作路径的代码
    
    user_query_prompt = f"""
"""
    
    tool_use_prompt = """
1. 必须使用python工具进行算法编码输出得到计算答案，不能直接给出答案。
2. 在每一次读取或者计算结束，将数据画图存下来起一个带编号的有意义的名字，
3. 并将当前工作路径和图片名字拼接起来输出图片的绝对路径输出出来。
4. 如果存储文件也要使用utf-8编码存储。
"""
    all_prompt = f"{data_info}\n\n{user_query_prompt}\n\n{tool_use_prompt}"
    user_query(all_prompt)
