import pprint
from pydantic import BaseModel, Field, ValidationError
from typing import Dict, Type, Any, Optional, Literal, List
import inspect

from src.agent.tool import tool_base
from src.runtime.sub_thread import subthread_python_executor
from src.runtime.status_mgr import var_ws

from src.utils import global_logger
class SearchInDeepwiki(tool_base.ToolBase):
    """
在 Deepwiki 中搜索相关信息的工具。

**功能：**
- 接受一个查询字符串，在 Deepwiki 中执行搜索，并返回相关结果。
- 结果可以包括页面标题、摘要和链接等信息，以帮助用户快速获取所需知识。

**关键规则：**
1. **查询格式**：输入必须是一个清晰的查询字符串，描述需要搜索的信息。
2. **结果格式**：返回的结果应结构化，包含页面标题、摘要和链接等关键信息，以便用户理解和使用。
3. **相关性**：确保返回的结果与查询高度相关，避免提供无关或过时的信息。
    """.strip()
    query: str = Field(
        ..., 
        description=(
        "要在 Deepwiki 中搜索的查询字符串。应清晰描述需要搜索的信息。"
        ),
        examples=["什么是强化学习？"]
    )

    def run(self) -> str:
        # 这里应该实现调用 Deepwiki 搜索 API 的逻辑，并返回结构化的结果。
        # 由于这是一个示例，我们将返回一个模拟的结果。
        global_logger.info(f"在 Deepwiki 中搜索查询：{self.query}")
        simulated_result = {
            "title": "强化学习",
            "summary": "强化学习是一种机器学习方法，通过与环境交互来学习最优策略。",
            "link": "https://deepwiki.com/强化学习"
        }
        return pprint.pformat(simulated_result)