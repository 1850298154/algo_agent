from src.agent.tool import base_tool
from src.utils import global_logger, traceable

@traceable
def get_tools_schema(class_names: list[base_tool.BaseTool] = None):
    """获取所有工具的 JSON Schema 列表，供 Agent 构造参数使用"""
    if class_names is None:
        return []
    return [tool.get_tool_schema() for tool in class_names if tool is not None]