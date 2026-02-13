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
        # ge=3,  # 最小值为3，避免无效配置
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
        # examples=["结束对话", "退出", "终止"],
    )
    
    # 扩展控制：强制终止开关
    force_terminate: bool = Field(
        default=False,
        description="是否强制终止对话（紧急开关），设为True时忽略其他规则直接结束",
    )

