import copy
from typing import Any, Dict, Optional, Union
from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator, model_validator, root_validator
from enum import Enum, unique
import sys  # 用于判断模块类型

# 新增：定义执行状态枚举（仅支持成功、失败、超时三种）
@unique
class ExecutionStatus(str, Enum):
    SUCCESS = "success"  # 执行成功
    FAILURE = "failure"  # 执行失败（代码错误等）
    TIMEOUT = "timeout"  # 执行超时

def filter_and_deepcopy_globals(original_globals: Dict[str, Any]) -> Dict[str, Any]:
    """
    过滤并深拷贝 globals 字典。
    过滤规则：
    1. 排除键为 '__builtins__' 的项。
    2. 排除值为模块类型的项。
    """
    filtered_dict = {}
    for key, value in original_globals.items():
        # 检查键是否为 '__builtins__'
        if key == '__builtins__':
            continue
        # 检查值是否为模块类型
        if isinstance(value, type(sys)):  # 使用 sys 模块的类型来判断其他模块
            continue
        # 对符合条件的值进行深拷贝并添加到新字典
        filtered_dict[key] = copy.deepcopy(value)
    return filtered_dict

# 新增：结构化返回模型（状态使用枚举）
class ExecutionResult(BaseModel):
    """执行结果结构化模型"""
    status: ExecutionStatus = Field(..., description="执行状态：成功/失败/超时")
    output: str = Field(..., description="标准输出或错误信息")
    globals: Dict[str, Any] = Field(..., description="执行后的全局变量（已过滤和深拷贝）")
    exception_type: Optional[str] = Field(None, description="错误类型（失败状态时）")
    exception_value: Optional[str] = Field(None, description="错误值（失败状态时）")
    exception_traceback: Optional[str] = Field(None, description="完整堆栈信息（失败状态时）")

    model_config = ConfigDict(
        use_enum_values=True,
        arbitrary_types_allowed=True
    )
    
    @field_validator('globals')
    @classmethod        
    def field_validate_globals(cls, value: Dict[str, Any]) -> Dict[str, Any]:
        # 手动判断 value 是否为 None，避免空指针
        if value is None:
            return {}  # 或 return None，根据业务需求调整
        return filter_and_deepcopy_globals(value)   
    
    @model_validator(mode='before')
    @classmethod
    def model_validate_globals(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        globals = values.get('globals')
        if globals is None:
            return {}  # 或 return None，根据业务需求调整
        values['globals'] = filter_and_deepcopy_globals(globals)   
        return values
    

if __name__ == "__main__":
    # 简单测试
    test_globals = {
        'a': 123,
        'b': [1, 2, 3],
        '__builtins__': __builtins__,
        'math': sys,
    }
    filtered_globals = filter_and_deepcopy_globals(test_globals)
    print("Filtered Globals:", filtered_globals)
    
    test_globals['b'].append(4)
    print("After Modification - Original Globals:", test_globals)
    print("Filtered Globals:", filtered_globals)

    # 测试 ExecutionResult 模型
    result = ExecutionResult(
        status=ExecutionStatus.SUCCESS,
        output="Execution completed successfully.",
        globals=test_globals,
        exception_type=None,
        exception_value=None,
        exception_traceback=None
    )
    print("ExecutionResult Model:", result.model_dump())