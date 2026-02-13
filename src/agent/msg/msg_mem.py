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
from src.agent.msg import msg_ctr
from src.agent.msg.msg_mem_id import msg_mem_id_factory
from src.utils.log_decorator import global_logger, traceable
from src.utils.path_util import dynamic_path

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Literal
import pprint
import json
import os


class MessageMemory(BaseModel):
    agent_name_id: str = Field(
        default_factory=msg_mem_id_factory.generate_unique,
        description="智能体名称，在集群中的唯一标识，三位数格式，重复时追加三位数后缀",
    )
    # 字段验证器：拦截手动传入的ID，执行查重和修正
    @field_validator('agent_name_id', mode='before')
    @classmethod
    def validate_agent_id(cls, v: str) -> str:
        """
        mode='before'：在Pydantic默认校验前执行，保证先修正ID再做格式校验
        :param v: 传入的agent_name_id值
        :return: 修正后的唯一ID
        """
        if not isinstance(v, str):
            v = str(v)
        # 调用公共函数做查重和修正
        return msg_mem_id_factory.if_same_transform_unique(query_id=v)

    msg_ctr_cfg: Optional[msg_ctr.MessageControlConfig] = Field(
        default=...,
        description="消息控制相关信息，记录每轮对话是否触发了消息控制，以及消息控制的具体配置参数",
    )
    
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
                    msg: ChatCompletionMessageParam|ChatCompletionMessage, 
                    finish_reason: Optional[Literal["stop", "length", "tool_calls", "content_filter", "function_call"]] = None
                    ) -> None:
        if isinstance(msg, ChatCompletionMessage):
            self.finish_reason = finish_reason
            self._print_assistant_messages(msg)
            msg = msg.model_dump()
        elif msg['role'] == action_type.CallKind.FUNCTION.value:
            self._print_function_messages(msg)
        elif msg['role'] == action_type.CallKind.TOOL.value:
            self._print_tool_messages(msg)
        else:
            global_logger.info(f"新类型消息 type =  {type(msg)} \n = {msg}\n")
            global_logger.info(f"新类型消息： {pprint.pformat(msg)}\n")
            global_logger.info("-" * 60)
        
        self.messages.append(msg)
        path = dynamic_path.MsgMemPath(agent_name_id=self.agent_name_id).path()
        with open(path, "w", encoding="utf-8") as fileio:
            json.dump (self, fileio, ensure_ascii=False, indent=4, default=lambda o: o.model_dump())                       

    def need_msg_stop_control(self, config: msg_ctr.MessageControlConfig) -> bool:
        """
        对话控制函数：根据提供的 MessageControlConfig 配置，对当前对话消息列表进行检查，判断是否满足停止条件
        返回值：True 表示满足停止条件，应当结束对话；False 表示继续对话
        """
        if config is None:
            global_logger.info("对话控制：未提供 MessageControlConfig 配置，默认继续对话")
            return False

        # 0. 优先检查模型返回的结束原因，如果模型已经明确返回结束原因，则直接终止对话
        if self.finish_reason:
            if self.finish_reason in ["stop", "length"]:
                global_logger.info(f"对话控制：检测到 finish_reason={self.finish_reason}，根据模型返回的结束原因终止对话")
                return True
            elif self.finish_reason in ["content_filter"]:
                global_logger.info(f"对话控制：检测到 finish_reason={self.finish_reason}，内容因违反规则被过滤，终止对话")
                return True
            else:
                global_logger.info(f"对话控制：检测到 finish_reason={self.finish_reason}，但该结束原因不在预设的停止原因列表中，继续对话")
        
        # 1. 检查强制终止开关
        if config.force_terminate:
            global_logger.info("对话控制：检测到 force_terminate=True，强制终止对话")
            return True
        
        # 2. 检查对话轮数
        if config.max_rounds:
            # 计算当前轮数（每个角色说一次话算一轮）
            rounds = len(self.messages)
            if rounds >= config.max_rounds:
                global_logger.info(f"对话控制：当前轮数 {rounds} 已达到或超过 max_rounds={config.max_rounds}，终止对话")
                return True
        
        # 3. 检查总 Token 长度
        if config.max_tokens_all_turn:
            total_tokens = self.usage.total_tokens if self.usage and self.usage.total_tokens else 0
            if total_tokens >= config.max_tokens_all_turn:
                global_logger.info(f"对话控制：当前总 Token 长度 {total_tokens} 已达到或超过 max_tokens_all_turn={config.max_tokens_all_turn}，终止对话")
                return True
        
        # 4. 检查单轮 Token 长度
        if config.max_tokens_per_turn and len(self.messages) >= 3:
            last_assist_msg_tokens = self.usage.completion_tokens if self.usage and self.usage.completion_tokens else 0
            if last_assist_msg_tokens >= config.max_tokens_per_turn:
                global_logger.info(f"对话控制：当前单轮 Token 长度 {last_assist_msg_tokens} 已达到或超过 max_tokens_per_turn={config.max_tokens_per_turn}，终止对话")
                return True
        
        # 5. 检查停止词触发
        if config.stop_words:
            for msg in self.messages:
                if any(stop_word in (msg.content or "") for stop_word in config.stop_words):
                    global_logger.info(f"对话控制：检测到消息内容包含停止词，触发停止词列表 {config.stop_words} 中的词汇，终止对话")
                    return True
        
        # 如果没有任何停止条件被触发，继续对话
        return False
            
    def _print_assistant_messages(self, assist_msg: ChatCompletionMessage) -> None:
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
def init_messages_with_system_prompt(
    agent_name_id: str, 
    system_prompt: str, 
    user_prompt: str,
    msg_ctr_config: Optional[msg_ctr.MessageControlConfig] = None
    ) -> list[ChatCompletionMessageParam]:
    messages: list[ChatCompletionMessageParam] = [
        ChatCompletionSystemMessageParam(
            content=system_prompt,
            role="system",
            # name="system",
        ),
        ChatCompletionUserMessageParam(
            content=user_prompt,
            role="user",
            # name="user",
        ),
    ]
    return MessageMemory(
        agent_name_id=agent_name_id, 
        messages=messages,  
        msg_ctr_cfg=msg_ctr_config,
    )

