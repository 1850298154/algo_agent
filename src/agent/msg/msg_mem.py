from openai.types.chat.chat_completion_message_param import (
    ChatCompletionDeveloperMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionAssistantMessageParam,
    ChatCompletionToolMessageParam,
    ChatCompletionFunctionMessageParam,    
    ChatCompletionMessageParam,
) 
from openai.types.chat.chat_completion import ChatCompletionMessage
from openai.types.chat.chat_completion import (
    ChatCompletion,
    CompletionUsage,
)

from src.agent.action import action_type
from src.utils.log_decorator import global_logger, traceable

from pydantic import BaseModel, Field
from typing import List, Optional, Literal
import pprint

class MessageMemory(BaseModel):
    messages: List[ChatCompletionMessageParam|ChatCompletionMessage] = Field(
        default_factory=list,
        description="对话消息列表，按照时间顺序存储每一轮对话的消息，包括系统、用户、AI、工具调用等角色的发言",
    )
    usage: Optional[CompletionUsage] = Field(
        default=None,
        description="对话过程中累计的 Token 使用情况，包括 prompt_tokens、completion_tokens 和 total_tokens",
    )
    finish_reason: Optional[Literal["stop", "length", "tool_calls", "content_filter", "function_call"]] = Field(
        default=None,
        description="对话结束原因",
    )
    
    def add_message(self, 
                    message: ChatCompletionMessageParam|ChatCompletionMessage, 
                    finish_reason: Optional[Literal["stop", "length", "tool_calls", "content_filter", "function_call"]] = None
                    ) -> None:
        self.messages.append(message)
        self.finish_reason = finish_reason
        if isinstance(message, ChatCompletionMessage):
            self._print_assistant_messages(message)
        elif message['role'] == action_type.CallKind.FUNCTION.value:
            self._print_function_messages(message)
        elif message['role'] == action_type.CallKind.TOOL.value:
            self._print_tool_messages(message)
        else:
            global_logger.info(f"新类型消息 type =  {type(message)} \n = {message}\n")
            global_logger.info(f"新类型消息： {pprint.pformat(message)}\n")
            global_logger.info("-" * 60)
    def _print_assistant_messages(self, assist_msg) -> None:
        global_logger.info(f"""第{len(self.messages)}轮大模型输出信息： 
                           \n\nassistant_output.content::   \n\n{pprint.pformat(assist_msg.content)}
                           \n\nassistant_output.tool_calls::\n\n{pprint.pformat( [toolcall.model_dump() for toolcall in assist_msg.tool_calls]    if assist_msg.tool_calls else [] )}
                           \n\n本轮工具调用结束""")
    def _print_function_messages(self, message:ChatCompletionFunctionMessageParam) -> None:
        global_logger.info(f"函数 function call 输出信息： {pprint.pformat(message)}\n")
        global_logger.info("-" * 60)
    def _print_tool_messages(self, message:ChatCompletionToolMessageParam) -> None:
        global_logger.info(f"工具 tool call 输出信息： {pprint.pformat(message)}\n")
        global_logger.info("-" * 60)

@traceable
def init_messages_with_system_prompt(sys_prompt: str, user_prompt: str) -> list[ChatCompletionMessageParam]:
    messages: list[ChatCompletionMessageParam] = [
        ChatCompletionSystemMessageParam(
            content=sys_prompt,
            role="system",
            name="system",
        ),
        ChatCompletionUserMessageParam(
            content=user_prompt,
            role="user",
            name="user",
        ),
    ]
    return MessageMemory(messages=messages)

