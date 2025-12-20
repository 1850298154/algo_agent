import pprint
from openai.types.chat.chat_completion import ChatCompletionMessage

from src.utils import global_logger, traceable

from src.agent import llm_glm as llm 
from src.agent import action 
from src.agent import memory 
from src.agent import tool 
from src.agent.tool import schema
from src.agent.tool import python_tool 
from src.agent.tool import todo_tool 

def user_query(user_input):
    user_hint = "用户输入："
    global_logger.info(f"{user_hint} ： {user_input}\n\n")

    messages = memory.init_messages_with_system_prompt(user_input)
    tools_schema_list = schema.get_tools_schema([
        python_tool.ExecutePythonCodeTool,
        # todo_tool.RecursivePlanTreeTodoTool,
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
\n\nassistant_output.tool_calls::\n\n {pprint.pformat([toolcall.model_dump() for toolcall in assistant_output.tool_calls] if assistant_output.tool_calls else [])}\n"""
        )
    global_logger.info(f"最终答案： {assistant_output.content}")
