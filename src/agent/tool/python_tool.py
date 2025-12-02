import pprint
from pydantic import BaseModel, Field, ValidationError
from typing import Dict, Type, Any, Optional, Literal, List
import inspect

from src.agent.tool import base_tool
from src.runtime import subprocess_python_executor
from src.runtime import workspace

from src.utils import global_logger

class ExecutePythonCodeTool(base_tool.BaseTool):
    """
必须调用在每一轮推理中，作为计算工具。
在有状态的环境中执行Python代码片段，类似于在Jupyter Notebook中运行单元格。

**功能：**
- 使用 Python 3.12 执行计算、数据处理和逻辑执行。
- **状态持久化**：在一次调用中定义的变量和函数会为后续调用保留（例如，在第一次调用中定义 `x=1` 后，第二次调用就可以使用 `x`）。
- **错误反馈**：如果代码运行失败，将返回详细的回溯信息，以便进行自我修正。

**关键规则：**
1. **输出可见性**：该工具捕获 `stdout`。你**必须使用 `print(...)`** 才能查看任何结果或变量值。仅计算值而不打印将导致输出为空。并且在print变量前print一下这个变量的含义，例如print("x=",x)。
2. **导入模块**：虽然变量会持续存在，但由于序列化限制，导入的模块（如 `math`、`json`）可能不会在每次调用中持续存在。**在每个代码片段中始终重新导入必要的模块**。
3. **安全性**：无限循环或运行时间极长的代码将被超时机制终止。
4. **依赖管理**：如果代码缺失了依赖于特定的外部库，可以代码片段 `subprocess.check_call(["uv", "add", package_name])` 代码安装。
    """.strip()
    python_code_snippet: str = Field(
        ..., 
        description=(
        "要执行的有效 Python 代码片段。不得包含恶意代码（例如，修改系统文件、访问敏感数据或执行无限循环的代码）。"
        ),
        examples=["print('Hello, World!')"]
    )
    timeout: int = Field(
        30, 
        description="执行代码的最大时间（秒）。如果代码运行时间超过此值，将被终止并返回错误消息。"
    )

    def run(self) -> str:
        execution_context: Optional[Dict[str, Any]] = workspace.get_arg_globals()
        global_logger.info(f"执行Python代码片段：{pprint.pformat(self.python_code_snippet)}")
        exec_result: subprocess_python_executor.ExecutionResult =  subprocess_python_executor.run_structured_in_subprocess(
            command=self.python_code_snippet, 
            _globals=execution_context,
            timeout=self.timeout
        )
        workspace.append_out_globals(exec_result.arg_globals)
        return exec_result.ret_tool2llm
