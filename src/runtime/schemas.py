from typing import Any, Dict, Optional, Union
from pydantic import BaseModel, Field, field_serializer, root_validator  # 新增 Field 用于枚举约束
from enum import Enum, unique  # 新增枚举相关导入

# 新增：定义执行状态枚举（仅支持成功、失败、超时三种）
@unique
class ExecutionStatus(str, Enum):
    SUCCESS = "success"  # 执行成功
    FAILURE = "failure"  # 执行失败（代码错误等）
    TIMEOUT = "timeout"  # 执行超时

# 新增：结构化返回模型（状态使用枚举）
class ExecutionResult(BaseModel):
    """执行结果结构化模型"""
    status: ExecutionStatus = Field(..., description="执行状态：成功/失败/超时")
    output: str = Field(..., description="标准输出或错误信息")
    globals: Dict[str, Any] = Field(..., description="执行后的全局变量")
    locals: Dict[str, Any] = Field({}, description="执行后的局部变量")
    exception_type: Optional[str] = Field(None, description="错误类型（失败状态时）")
    exception_value: Optional[str] = Field(None, description="错误值（失败状态时）")
    exception_traceback: Optional[str] = Field(None, description="完整堆栈信息（失败状态时）")

    class Config:
        use_enum_values = True  # 序列化时使用枚举值（如"pending"）而非枚举对象