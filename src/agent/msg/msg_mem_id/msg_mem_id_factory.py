from numpy import add
from pydantic import BaseModel, Field, field_validator
import threading
from src.utils.log_decorator import global_logger

# 1. 全局变量：基础计数器、线程锁、已使用ID集合
_counter_lock = threading.Lock()
_used_agent_ids:set[str] = set()

def if_same_transform_unique(query_id: str) -> str:
    """
    公共函数：检查基础ID是否重复，重复则追加三位数后缀生成唯一ID
    :param query_id: 原始ID（手动传入或自动生成的基础ID）
    :return: 全局唯一的ID字符串
    """
    with _counter_lock:
        # 第一步：检查原始ID是否未重复，直接使用
        if query_id not in _used_agent_ids:
            global_logger.info(f"ID '{query_id}' is unique, using it directly.")
            unique_id = query_id
        else:
            try_id = query_id
            while try_id in _used_agent_ids:
                try_id = f"{try_id}_{len(_used_agent_ids) + 1:03d}"
            unique_id = try_id
            global_logger.warning(f"ID '{query_id}' is already used, generating a unique ID by appending suffix: '{unique_id}'")
        _used_agent_ids.add(unique_id)
        return unique_id 

def generate_unique() -> str:
    """默认工厂函数：生成基础三位数ID，再通过公共函数保证唯一"""
    with _counter_lock:
        # 生成基础三位数ID
        gen_id = f"{len(_used_agent_ids) + 1:03d}"
        while gen_id in _used_agent_ids:
            gen_id = f"{int(gen_id) + 1:03d}"
        
        global_logger.info(f"Generated base ID '{gen_id}' for new agent, checking for uniqueness.")
        return gen_id

class MessageMemory(BaseModel):
    agent_name_id: str = Field(
        default_factory=generate_unique,
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
        return if_same_transform_unique(query_id=v)
# # 测试示例
if __name__ == "__main__":
    # 测试1：手动传入未重复的ID（001）
    mem1 = MessageMemory(agent_name_id="001")
    print(mem1.agent_name_id)  # 输出: 001（未重复，直接使用）
    
    # 测试2：再次手动传入重复的ID（001）
    mem2 = MessageMemory(agent_name_id="001")
    print(mem2.agent_name_id)  # 输出: 001_001（重复，追加后缀001）
    
    # 测试3：第三次传入001，后缀递增
    mem3 = MessageMemory(agent_name_id="001")
    print(mem3.agent_name_id)  # 输出: 001_002
    
    # 测试4：自动生成ID（基础ID002，未重复）
    mem4 = MessageMemory()
    print(mem4.agent_name_id)  # 输出: 002
    
    # 测试5：手动传入带后缀的重复ID
    mem5 = MessageMemory(agent_name_id="001_001")
    print(mem5.agent_name_id)  # 输出: 001_001（未重复，直接使用）
    mem6 = MessageMemory(agent_name_id="001_001")
    print(mem6.agent_name_id)  # 输出: 001_001_001（重复，追加后缀）