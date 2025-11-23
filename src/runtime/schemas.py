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
    CRASHED = "crashed"  # 进程崩溃（如 SegFault）
    
    
    @classmethod
    def get_return_llm(cls, status: "ExecutionStatus", result: "ExecutionResult") -> str:
        """根据执行状态，生成返回给模型的描述信息
            不可以有任何log或print，因为子进程重写了stdout/stderr
        """
        _desc_map = {
            cls.SUCCESS: "## 代码执行成功，输出结果完整，任务完成\n"
                        f"### 终端输出：\n"
                        f"{result.ret_stdout}"
                        ,
            cls.FAILURE: "## 代码执行失败，代码抛出异常，根据报错信息进行调试\n"
                        f"### 终端输出：\n"
                        f"{result.ret_stdout}"
                        f"### 原始代码：\n"
                        f"{source_code.add_line_numbers(result.arg_command)}\n"
                        f"### 报错信息：\n"
                        f"{result.exception_traceback}"
                        ,
            cls.TIMEOUT: "## 代码执行超时，强制退出执行，调整超时时间后重试\n"
                        f"### 终端输出：\n"
                        f"{result.ret_stdout}"
                        f"### 超出限制的时间：{result.arg_timeout} 秒\n"
                        ,
            cls.CRASHED: "## 代码执行崩溃，进程异常退出，根据报错信息进行调试\n"
                        f"### 终端输出：\n"
                        f"{result.ret_stdout}"
                        f"### 退出状态码：{result.exit_code}\n"
                        ,
        }
        return _desc_map.get(status, f"未知状态:  {status}")


"""
exitcode = 0：进程正常退出；
exitcode > 0：进程因错误退出（如代码逻辑错误、命令执行失败）；
exitcode < 0：进程被信号终止（-信号编号，如 -15 对应 SIGTERM，-9 对应 SIGKILL 强制终止， -11=139=128+11 对应 SIGSEGV  segmentation fault）。
"""
# 新增：结构化返回模型（状态使用枚举）
class ExecutionResult(BaseModel):
    """输入参数"""
    arg_command: str = Field(..., description="执行的代码命令")
    arg_timeout: int = Field(..., description="设置的超时时间（秒）")
    arg_globals: Dict[str, Any] = Field(..., description="执行后的全局变量（已过滤和深拷贝）（成功状态时、才能给workspace后续使用）")
    """执行结果结构化模型"""
    exit_status: ExecutionStatus = Field(..., description="执行结果状态")
    exit_code: Optional[int] = Field(None, description="进程退出码（任意状态时，延迟由父进程获取）")
    exception_repr: Optional[str] = Field(None, description="错误的repr（失败状态时）")
    exception_type: Optional[str] = Field(None, description="错误类型（失败状态时）")
    exception_value: Optional[str] = Field(None, description="错误值（失败状态时）")
    exception_traceback: Optional[str] = Field(None, description="完整堆栈信息（失败状态时）")
    """如下延迟父进程获取、自动生成、选填"""
    ret_stdout: str = Field("", description="标准输出或标准错误信息（任意状态时，延迟由父进程获取）")
    ret_tool2llm: Optional[str] = Field(None, description="返回作为模型输入（根据结果状态，延迟由父进程自动生成）")

    model_config = ConfigDict(
        # use_enum_values=True,
        arbitrary_types_allowed=True
    )

    @field_validator('arg_globals')
    @classmethod        
    def field_validate_globals(cls, value: Dict[str, Any]) -> Dict[str, Any]:
        # 手动判断 value 是否为 None，避免空指针
        if value is None:
            return {}  # 或 return None，根据业务需求调整
        return workspace.filter_and_deepcopy_globals(value)   


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
        exit_status=ExecutionStatus.SUCCESS,
        stdout="Execution completed successfully.",
        globals=test_globals,
        exception_type=None,
        exception_value=None,
        exception_traceback=None
    )
    print("ExecutionResult Model:", result.model_dump())
