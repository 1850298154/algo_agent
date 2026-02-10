from more_itertools import last
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


from pydantic import BaseModel, Field
from typing import List, Optional
from src.agent.msg import msg_mem
from src.utils.log_decorator import global_logger


class MessageControlConfig(BaseModel):
    """
    对话控制配置类：用于统一管控对话的轮数、Token 长度、停止规则等核心参数
    """
    # 核心控制：对话轮数相关
    max_rounds: Optional[int] = Field(
        default=None,  # 默认值设置为一个非常大的数，表示无限量
        description="对话的最大轮数上限，每一个角色说一次话算作一轮（例如用户说1句+AI回复1句=2轮）",
        ge=3,  # 最小值为3，避免无效配置
    )
    
    # 核心控制：Token 长度相关
    max_tokens_all_turn: Optional[int] = Field(
        default=None,
        description="整个对话生命周期内的总 Token 长度上限（包含所有角色的发言），在大模型返回之后进行检查，达到上限后终止对话",
    )
    max_tokens_per_turn: Optional[int] = Field(
        default=None,
        description="单轮对话（单个角色单次发言）的最大 Token 长度上限，None表示不限制单轮",
    )
    
    # 扩展控制：停止词触发
    stop_words: List[str] = Field(
        default_factory=list,
        description="触发对话终止的停止词列表，只要任意角色发言包含其中词汇，立即结束对话",
        example=["结束对话", "退出", "终止"],
    )
    
    # 扩展控制：强制终止开关
    force_terminate: bool = Field(
        default=False,
        description="是否强制终止对话（紧急开关），设为True时忽略其他规则直接结束",
    )


def need_msg_stop_control(message_mem: msg_mem.MessageMemory, config: MessageControlConfig) -> bool:
    """
    对话控制函数：根据提供的 MessageControlConfig 配置，对当前对话消息列表进行检查，判断是否满足停止条件
    返回值：True 表示满足停止条件，应当结束对话；False 表示继续对话
    """
    # 0. 优先检查模型返回的结束原因，如果模型已经明确返回结束原因，则直接终止对话
    if message_mem.finish_reason:
        if message_mem.finish_reason in ["stop", "length"]:
            global_logger.info(f"对话控制：检测到 finish_reason={message_mem.finish_reason}，根据模型返回的结束原因终止对话")
            return True
        elif message_mem.finish_reason in ["content_filter"]:
            global_logger.info(f"对话控制：检测到 finish_reason={message_mem.finish_reason}，内容因违反规则被过滤，终止对话")
            return True
        else:
            global_logger.info(f"对话控制：检测到 finish_reason={message_mem.finish_reason}，但该结束原因不在预设的停止原因列表中，继续对话")
    
    # 1. 检查强制终止开关
    if config.force_terminate:
        global_logger.info("对话控制：检测到 force_terminate=True，强制终止对话")
        return True
    
    # 2. 检查对话轮数
    if config.max_rounds:
        # 计算当前轮数（每个角色说一次话算一轮）
        rounds = len(message_mem.messages)
        if rounds >= config.max_rounds:
            global_logger.info(f"对话控制：当前轮数 {rounds} 已达到或超过 max_rounds={config.max_rounds}，终止对话")
            return True
    
    # 3. 检查总 Token 长度
    if config.max_tokens_all_turn:
        total_tokens = message_mem.usage.total_tokens if message_mem.usage and message_mem.usage.total_tokens else 0
        if total_tokens >= config.max_tokens_all_turn:
            global_logger.info(f"对话控制：当前总 Token 长度 {total_tokens} 已达到或超过 max_tokens_all_turn={config.max_tokens_all_turn}，终止对话")
            return True
    
    # 4. 检查单轮 Token 长度
    if config.max_tokens_per_turn and len(message_mem.messages) >= 3:
        last_assist_msg_tokens = message_mem.usage.completion_tokens if message_mem.usage and message_mem.usage.completion_tokens else 0
        if last_assist_msg_tokens >= config.max_tokens_per_turn:
            global_logger.info(f"对话控制：当前单轮 Token 长度 {last_assist_msg_tokens} 已达到或超过 max_tokens_per_turn={config.max_tokens_per_turn}，终止对话")
            return True
    
    # 5. 检查停止词触发
    if config.stop_words:
        for msg in message_mem.messages:
            if any(stop_word in (msg.content or "") for stop_word in config.stop_words):
                global_logger.info(f"对话控制：检测到消息内容包含停止词，触发停止词列表 {config.stop_words} 中的词汇，终止对话")
                return True
    
    # 如果没有任何停止条件被触发，继续对话
    return False