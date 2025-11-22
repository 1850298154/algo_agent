import copy
from typing import Any, Dict, Optional, Union
from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator, model_validator, root_validator
from enum import Enum, unique
import sys  # 用于判断模块类型
from src.runtime import source_code
from src.runtime import workspace

# 新增：定义执行状态枚举（仅支持成功、失败、超时三种）
@unique
class ExecutionStatus(str, Enum):
    SUCCESS = "success"  # 执行成功
    FAILURE = "failure"  # 执行失败（代码错误等）
    TIMEOUT = "timeout"  # 执行超时
    
    @classmethod
    def get_display_desc(cls, status) -> str:
        # 统一将 status 转换为字符串（兼容枚举实例和字符串）
        status_key = status.value if isinstance(status, cls) else status
        desc_map = {
            "success": "代码执行成功，输出结果如下：\n",
            "failure": "代码执行失败，代码报错如下：\n",
            "timeout": "代码执行超时，可能未完成的输出：\n",
        }
        # 增加默认值处理，避免 KeyError
        return desc_map.get(status_key, f"未知状态: {status_key}")


# 新增：结构化返回模型（状态使用枚举）
class ExecutionResult(BaseModel):
    command: str = Field(..., description="执行的代码命令")
    timeout: Optional[int] = Field(None, description="设置的超时时间（秒）")
    globals: Dict[str, Any] = Field(..., description="执行后的全局变量（已过滤和深拷贝）（成功状态时）")
    """执行结果结构化模型"""
    status: ExecutionStatus = Field(..., description="执行状态：成功/失败/超时")
    std_output: str = Field(..., description="标准输出或错误信息（任意状态时）")
    """如下自动生成或选填"""
    ret_llm_content: str = Field(None, description="根据状态，自动生成返回作为模型输入")
    exception_type: Optional[str] = Field(None, description="错误类型（失败状态时）")
    exception_value: Optional[str] = Field(None, description="错误值（失败状态时）")
    exception_traceback: Optional[str] = Field(None, description="完整堆栈信息（失败状态时）")

    model_config = ConfigDict(
        # use_enum_values=True,
        arbitrary_types_allowed=True
    )
    
    @field_validator('globals')
    @classmethod        
    def field_validate_globals(cls, value: Dict[str, Any]) -> Dict[str, Any]:
        # 手动判断 value 是否为 None，避免空指针
        if value is None:
            return {}  # 或 return None，根据业务需求调整
        return workspace.filter_and_deepcopy_globals(value)   
    
    @model_validator(mode='before')
    @classmethod
    def model_validate_globals(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        globals = values.get('globals')
        if globals is None:
            return {}  # 或 return None，根据业务需求调整
        values['globals'] = workspace.filter_and_deepcopy_globals(globals) 
        values['ret_llm_content'] = (
            ExecutionStatus.get_display_desc(values['status'])
            + (f"设置的超时时间：{values.get('timeout', '')}秒\n" if values['status'] == ExecutionStatus.TIMEOUT else '')
            + (values.get('std_output', '')
               if values['status'] != ExecutionStatus.FAILURE
                else source_code.get_code_and_traceback(values['command']))
        )
        return values
    

if __name__ == "__main__":
    # 简单测试
    test_globals = {
        'a': 123,
        'b': [1, 2, 3],
        '__builtins__': __builtins__,
        'math': sys,
    }
    filtered_globals = workspace.filter_and_deepcopy_globals(test_globals)
    print("Filtered Globals:", filtered_globals)
    
    test_globals['b'].append(4)
    print("After Modification - Original Globals:", test_globals)
    print("Filtered Globals:", filtered_globals)

    # 测试 ExecutionResult 模型
    result = ExecutionResult(
        status=ExecutionStatus.SUCCESS,
        std_output="Execution completed successfully.",
        globals=test_globals,
        exception_type=None,
        exception_value=None,
        exception_traceback=None
    )
    print("ExecutionResult Model:", result.model_dump())