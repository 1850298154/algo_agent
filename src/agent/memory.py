from src.utils import global_logger, traceable
from prompt import react_system_prompt

@traceable
def init_messages_with_system_prompt(user_input: str) -> list[dict[str, str]]:
    messages = [
        {
            "content": react_system_prompt,
            "role": "system",
        },
        {
            "content": user_input,
            "role": "user",
        }
    ]
    return messages
