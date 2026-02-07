import abc
from enum import Enum, unique
from token import OP
from typing import Any, Dict, Optional, Literal, Union, Annotated
from pydantic import BaseModel, ConfigDict, Field, field_validator, computed_field
from src.runtime import source_code
from src.runtime import workspace

@unique
class ExecutionStatus(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    TIMEOUT = "timeout"
    CRASHED = "crashed"

# --- 基类：定义所有情况共有的字段 ---
class BaseExecutionResult(BaseModel):
    """执行结果基类"""
    arg_command: str = Field(..., description="执行的代码命令")
    arg_timeout: Optional[float] = Field(None, description="设置的超时时间（秒）")
    exec_timeout: float = Field(..., description="实际执行耗时（秒），可以在超时、等等情况下提供给模型参考")
    
    # stdout 初始为空，由 Executor 执行完后回填
    ret_stdout: str = Field("", description="标准输出或标准错误信息")
    
    # 定义 exit_status 为抽象属性，强制子类实现（通过 Literal）
    exit_status: ExecutionStatus = Field(..., description="执行结果状态")

    # model_config = ConfigDict(arbitrary_types_allowed=True)

    @computed_field
    def ret_tool2llm(self) -> str:
        """
        计算字段：返回作为模型输入的描述信息。
        类似于之前的 get_return_llm，但在访问该属性或序列化时自动计算。
        由子类具体实现。
        """
        return self._generate_llm_response()

    @abc.abstractmethod
    def _generate_llm_response(self) -> str:
        """子类必须实现的具体文案生成逻辑"""
        pass

# --- 1. 成功状态 ---
class ExecutionSuccess(BaseExecutionResult):
    exit_status: Literal[ExecutionStatus.SUCCESS] = ExecutionStatus.SUCCESS
    
    # 只有成功时才需要处理 globals
    arg_chg_globals: Dict[str, Any] = Field(..., description="执行后的全局变量")

    @field_validator('arg_chg_globals', mode='before')
    @classmethod
    def field_validate_globals(cls, value: Any) -> Dict[str, Any]:
        if value is None:
            return {}
        # 这里保留你的深拷贝逻辑
        return workspace.filter_and_deepcopy_globals(value)

    def _generate_llm_response(self) -> str:
        return (
            "## 代码执行成功，输出结果完整，任务完成\n"
            "### 终端输出：\n"
            f"{self.ret_stdout}"
        )

# --- 2. 失败状态（代码报错） ---
class ExecutionFailure(BaseExecutionResult):
    exit_status: Literal[ExecutionStatus.FAILURE] = ExecutionStatus.FAILURE
    
    # 失败特有字段
    exception_repr: str
    exception_type: str
    exception_value: str
    exception_traceback: str

    # 失败时不需要 arg_globals

    def _generate_llm_response(self) -> str:
        return (
            "## 代码执行失败，代码抛出异常，根据报错信息进行调试\n"
            "### 终端输出：\n"
            f"{self.ret_stdout}\n"
            "### 原始代码：\n"
            f"{source_code.add_line_numbers(self.arg_command)}\n"
            "### 报错信息：\n"
            f"{self.exception_traceback}"
        )

# --- 3. 超时状态 ---
class ExecutionTimeout(BaseExecutionResult):
    exit_status: Literal[ExecutionStatus.TIMEOUT] = ExecutionStatus.TIMEOUT
    
    # 可以在这里增加超时特有的元数据，如是否强制 kill 成功等

    def _generate_llm_response(self) -> str:
        return (
            "## 代码执行超时，强制退出执行，调整超时时间后重试\n"
            "### 终端输出：\n"
            f"{self.ret_stdout}\n"
            f"### 超出限制的时间：{self.arg_timeout} 秒\n"
        )

# --- 4. 崩溃状态（SegFault 等） ---
class ExecutionCrashed(BaseExecutionResult):
    exit_status: Literal[ExecutionStatus.CRASHED] = ExecutionStatus.CRASHED
    
    exit_code: Optional[int] = Field(None, description="进程退出码")

    def _generate_llm_response(self) -> str:
        return (
            "## 代码执行崩溃，进程异常退出，根据报错信息进行调试\n"
            "### 终端输出：\n"
            f"{self.ret_stdout}\n"
            f"### 退出状态码：{self.exit_code}\n"
        )

# --- 定义联合类型 ---
# 使用 Annotated 和 Field(discriminator=...) 可以让 Pydantic 在解析 JSON 时自动选择正确的类
# 但在 Python 代码中直接实例化具体类即可
ExecutionResultFromSubThread = Union[ExecutionSuccess, ExecutionFailure]
ExecutionResult = Union[ExecutionResultFromSubThread, ExecutionTimeout, ExecutionCrashed]