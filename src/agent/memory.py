from openai.types.chat.chat_completion_message_param import (
    ChatCompletionDeveloperMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionAssistantMessageParam,
    ChatCompletionToolMessageParam,
    ChatCompletionFunctionMessageParam,    
    ChatCompletionMessageParam,
) 
from src.utils import global_logger, traceable

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
    return messages

