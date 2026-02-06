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

import pprint

from src.utils import global_logger, traceable

from src.agent import llm
from src.agent import action 
from src.agent import memory 
from src.agent import tool 

def user_query(user_input: str) -> None:
    user_hint = "用户输入："
    global_logger.info(f"{user_hint} ： {user_input}\n\n")

    messages: list[ChatCompletionMessageParam] = memory.init_messages_with_system_prompt(user_input)
    tools_schema_list = tool.schema.get_tools_schema([
        tool.python_tool.ExecutePythonCodeTool,
        # tool.todo_tool.RecursivePlanTreeTodoTool,
        ])

    # 模型的第一轮调用
    assist_msg: ChatCompletionMessage = llm.generate_assistant_output_append(messages, tools_schema_list)
    if (assist_msg.tool_calls is not None 
        and assist_msg.function_call is not None):
        global_logger.info(f"无需调用工具，我可以直接回复：{assist_msg.content}")
        return

    # 如果需要调用工具，则进行模型的多轮调用，直到模型判断无需调用工具
    while (assist_msg.tool_calls is not None 
            or assist_msg.function_call is not None):
        if assist_msg.function_call is not None:
            function_call: FunctionCall = assist_msg.function_call
            func_output = action.call_tools_safely(function_call.name, function_call.arguments)
            global_logger.info(f"工具 function call 输出信息： {func_output}\n")
            global_logger.info("-" * 60)
            messages.append(
                ChatCompletionFunctionMessageParam(
                    content=func_output,
                    name=function_call.name,
                    role="function",
                )
            )
        if assist_msg.tool_calls is not None and assist_msg.tool_calls :
            # 使用 isinstance 过滤并重新生成列表
            tool_calls_list: list[ChatCompletionMessageFunctionToolCall] = [
                tc for tc in (assist_msg.tool_calls or []) 
                if isinstance(tc, ChatCompletionMessageFunctionToolCall)
            ]            
            for i in range(len(tool_calls_list)):

                tool_output = action.call_tools_safely(tool_calls_list[i].function.name, tool_calls_list[i].function.arguments)
                global_logger.info(f"工具 tool call 输出信息： {tool_output}\n")
                global_logger.info("-" * 60)
                messages.append(
                    ChatCompletionToolMessageParam(
                        content=tool_output,
                        role="tool",
                        tool_call_id=tool_calls_list[i].id,
                    )
                )
        assist_msg = llm.generate_assistant_output_append(messages, tools_schema_list)
        if assist_msg.content is None:
            assist_msg.content = ""
        global_logger.info(
            f"""第{len(messages) // 2}轮大模型输出信息： 
\n\nassistant_output.content:: \n\n {pprint.pformat(assist_msg.content)}
\n\nassistant_output.tool_calls::\n\n {pprint.pformat([toolcall.model_dump() for toolcall in assist_msg.tool_calls] if assist_msg.tool_calls else [])}\n"""
        )
    global_logger.info(f"最终答案： {assist_msg.content}")
