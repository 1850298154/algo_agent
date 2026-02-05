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
from src.agent.prompt import react_system_prompt

@traceable
def init_messages_with_system_prompt(user_input: str) -> list[ChatCompletionMessageParam]:
    messages: list[ChatCompletionMessageParam] = [
        ChatCompletionSystemMessageParam(
            content=react_system_prompt,
            role="system",
            name="system",
        ),
        ChatCompletionUserMessageParam(
            content=user_input,
            role="user",
            name="user",
        ),
    ]
    return messages

