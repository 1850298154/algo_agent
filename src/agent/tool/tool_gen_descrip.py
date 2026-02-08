from src.agent.tool import tool_base
from src.utils import global_logger, traceable

@traceable
def get_tools_schema(class_type_list: list[tool_base.ToolBase]):
    """获取所有工具的 JSON Schema 列表，供 Agent 构造参数使用"""
    return [tool.get_tool_schema() for tool in class_type_list if tool is not None]
