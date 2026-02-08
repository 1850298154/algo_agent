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
import asyncio

from src.utils import global_logger, traceable

from src.agent import llm
from src.agent import action 
from src.agent import memory 
from src.agent import tool 

async def user_query(sys_prompt: str, user_prompt: str, tool_class_list: list[tool.base_tool.BaseTool]) -> None:
    user_hint = "用户输入："
    global_logger.info(f"{user_hint} ： {user_prompt}\n\n")

    messages: list[ChatCompletionMessageParam] = memory.init_messages_with_system_prompt(user_prompt, sys_prompt)
    tools_schema_list = tool.gen_des_schema.get_tools_schema(tool_class_list)

    # 模型的第一轮调用（在线程中执行以避免阻塞）
    assist_msg: ChatCompletionMessage = await asyncio.to_thread(llm.generate_assistant_output_append, messages, tools_schema_list)
    if (assist_msg.tool_calls is not None 
        and assist_msg.function_call is not None):
        global_logger.info(f"无需调用工具，我可以直接回复：{assist_msg.content}")
        return

    # 如果需要调用工具，则进行模型的多轮调用，直到模型判断无需调用工具
    while (assist_msg.tool_calls is not None 
            or assist_msg.function_call is not None):
        # 收集所有要并发执行的调用（function + tool calls）
        call_descriptors: list[tuple[str, str, str, str | None]] = []  # (kind, name, arguments, tool_call_id)
        if assist_msg.function_call is not None:
            function_call: FunctionCall = assist_msg.function_call
            call_descriptors.append(("function", function_call.name, function_call.arguments, None))

        if assist_msg.tool_calls is not None and assist_msg.tool_calls:
            tool_calls_list: list[ChatCompletionMessageFunctionToolCall] = [
                tc for tc in (assist_msg.tool_calls or []) 
                if isinstance(tc, ChatCompletionMessageFunctionToolCall)
            ]
            for tc in tool_calls_list:
                call_descriptors.append(("tool", tc.function.name, tc.function.arguments, tc.id))

        # 并发执行所有调用（在线程中执行阻塞工具）
        tasks = [
            asyncio.to_thread(action.call_tools_safely, name, arguments)
            for (_kind, name, arguments, _id) in call_descriptors
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # 将每个调用的输出按顺序追加到 messages
        for (kind, name, arguments, tool_call_id), result in zip(call_descriptors, results):
            if isinstance(result, Exception):
                func_output = f"工具执行异常: {result}"
            else:
                func_output = result
            if kind == "function":
                global_logger.info(f"工具 function call 输出信息： {func_output}\n")
                global_logger.info("-" * 60)
                messages.append(
                    ChatCompletionFunctionMessageParam(
                        content=func_output,
                        name=name,
                        role="function",
                    )
                )
            else:  # tool
                global_logger.info(f"工具 tool call 输出信息： {func_output}\n")
                global_logger.info("-" * 60)
                messages.append(
                    ChatCompletionToolMessageParam(
                        content=func_output,
                        role="tool",
                        tool_call_id=tool_call_id,
                    )
                )

        # 让模型基于工具输出继续生成（也在线程中执行）
        assist_msg = await asyncio.to_thread(llm.generate_assistant_output_append, messages, tools_schema_list)
        if assist_msg.content is None:
            assist_msg.content = ""
        global_logger.info(
            f"""第{len(messages) // 2}轮大模型输出信息： 
\n\nassistant_output.content:: \n\n {pprint.pformat(assist_msg.content)}
\n\nassistant_output.tool_calls::\n\n 
{pprint.pformat(
    [toolcall.model_dump() for toolcall in assist_msg.tool_calls]   
    if assist_msg.tool_calls 
    else [])
}\n"""
        )
    global_logger.info(f"最终答案： {assist_msg.content}")
    
    return messages