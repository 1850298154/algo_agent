
import json
import traceback
from openai.types.chat.chat_completion import ChatCompletionMessage

from src.utils import global_logger, traceable
from src.agent.tool.python_tool import ExecutePythonCodeTool 
from src.agent.tool.todo_tool import RecursivePlanTreeTodoTool
@traceable
def call_tools_safely(tool_info: dict):
    def call_tools(tool_info: dict):
        function_name = tool_info["tool_call_name"]
        arguments = json.loads(tool_info["tool_call_arguments"])
        if False:pass
        elif function_name == ExecutePythonCodeTool.tool_name():
            execute_python_code_tool = ExecutePythonCodeTool(**arguments)
            tool_info["content"] = execute_python_code_tool.run()
        elif function_name == RecursivePlanTreeTodoTool.tool_name():
            recursive_plan_tree_todo_tool = RecursivePlanTreeTodoTool(**arguments)
            tool_info["content"] = recursive_plan_tree_todo_tool.run()
        return  tool_info
        # elif assistant_output.tool_calls[0].function.name == list_indices_tool.name:
        #     # 提取位置参数信息
        #     arguments = json.loads(assistant_output.tool_calls[0].function.arguments)
        #     tool_info["content"] = list_indices_tool.run(arguments)
        # elif assistant_output.tool_calls[0].function.name == index_show_data_tool.name:
        #     # 提取位置参数信息
        #     arguments = json.loads(assistant_output.tool_calls[0].function.arguments)
        #     tool_info["content"] = index_show_data_tool.run(arguments)
        # elif assistant_output.tool_calls[0].function.name == index_details_tool.name:
        #     # 提取位置参数信息
        #     arguments = json.loads(assistant_output.tool_calls[0].function.arguments)
        #     tool_info["content"] = index_details_tool.run(arguments)
        # elif assistant_output.tool_calls[0].function.name == search_tool.name:
        #     # 提取位置参数信息
        #     arguments = json.loads(assistant_output.tool_calls[0].function.arguments)
        #     tool_info["content"] = search_tool.run(arguments)
    
    
    try:
        return call_tools(tool_info)
    except Exception as e:
        # 获取完整的错误信息（包括堆栈）
        error_msg = traceback.format_exc()        
        global_logger.error(f"工具函数调用失败{tool_info['content']}, 错误信息: {error_msg}", exc_info=True)
        tool_info["content"] = f"工具函数调用失败{tool_info['content']}, 错误信息: {error_msg}"
        return tool_info

