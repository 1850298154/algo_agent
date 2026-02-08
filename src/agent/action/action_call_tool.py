
from openai.types.chat.chat_completion import (
    ChatCompletionMessage,
)
from openai.types.chat.chat_completion_message import (
    FunctionCall,
    ChatCompletionMessageToolCallUnion,
)
from openai.types.chat.chat_completion_message_function_tool_call import (
    ChatCompletionMessageFunctionToolCall,
)
from openai.types.chat.chat_completion_message_param import (
    ChatCompletionDeveloperMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionAssistantMessageParam,
    ChatCompletionToolMessageParam,
    ChatCompletionFunctionMessageParam,    
    ChatCompletionMessageParam,
) 

import json
import traceback
import pprint
import asyncio

from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple, Optional, Any

from src.utils import global_logger, traceable
from src.agent.tool.python_tool import ExecutePythonCodeTool 
from src.agent.tool.todo_tool import RecursivePlanTreeTodoTool


@traceable
def _call_tools_safely(tool_name: str,tool_arguments: str) -> str:
    def call_tools(tool_name: str,tool_arguments: str) -> str:
        function_name = tool_name
        arguments = json.loads(tool_arguments)
        if False:pass
        elif function_name == ExecutePythonCodeTool.tool_name():
            execute_python_code_tool = ExecutePythonCodeTool(**arguments)
            tool_content = execute_python_code_tool.run()
        elif function_name == RecursivePlanTreeTodoTool.tool_name():
            recursive_plan_tree_todo_tool = RecursivePlanTreeTodoTool(**arguments)
            tool_content = recursive_plan_tree_todo_tool.run()
        return  tool_content
    try:
        return call_tools(tool_name, tool_arguments)
    except Exception as e:
        # 获取完整的错误信息（包括堆栈）
        error_msg = traceback.format_exc()        
        tool_err = f"{tool_name} 工具函数调用失败，工具参数是 {tool_arguments} ，执行工具时候发生的错误信息: {error_msg}"
        global_logger.error(tool_err, exc_info=True)
        return tool_err


async def execute_single_call_async(name: str, arguments: Any) -> str:
    """执行一次工具或 function 调用（需要为协程）"""
    return _call_tools_safely(name, arguments)

