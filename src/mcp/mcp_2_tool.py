from openai.resources.chat.completions.completions import (
    ChatCompletionToolUnionParam,
)
from openai.types.chat.chat_completion_function_tool_param import (
    ChatCompletionFunctionToolParam,
)
from openai.types.shared_params.function_definition import (
    FunctionDefinition,
    FunctionParameters,
)
from pydantic import BaseModel, Field
from typing import Optional
import json
from pathlib import Path
from typing import Any
from src.mcp import mcp_enum
from src.utils.log_decorator import traceable

class MCPSchema2ToolSchema(BaseModel):
    name: str = Field(..., description="The name of the MCP")
    description: str = Field(..., description="A brief description of the MCP")
    inputSchema: dict = Field(..., description="The input schema for the MCP")
    outputSchema: Optional[dict] = Field(None, description="The output schema for the MCP")
    
    @classmethod
    def list_from_name(cls, name: mcp_enum.MCPEnum) -> list["MCPSchema2ToolSchema"]:
        base_dir = Path(__file__).resolve().parent / mcp_enum.mcp_list_tool_json_dir
        path = base_dir / f"{name.value}.json"
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        def _make(obj: Any) -> "MCPSchema2ToolSchema":
            if hasattr(cls, "model_validate"):
                return cls.model_validate(obj)  # type: ignore
            return cls(**obj)

        if isinstance(data, list):
            return [_make(item) for item in data]
        if isinstance(data, dict):
            return [_make(data)]
        raise ValueError("JSON must be an object or an array of objects")


_enum_2_mcp_tool_schema_collection: dict[mcp_enum.MCPEnum, list[MCPSchema2ToolSchema]] = {
    mcp_enum.MCPEnum.DEVIN: MCPSchema2ToolSchema.list_from_name(mcp_enum.MCPEnum.DEVIN),
    mcp_enum.MCPEnum.GITHUB: MCPSchema2ToolSchema.list_from_name(mcp_enum.MCPEnum.GITHUB),
}


mcp_tool_name_2_enum_dict_for_call_mcp: dict[str, mcp_enum.MCPEnum] = {
    descrip.name: mcp_enum
    for mcp_enum, descrip_list in _enum_2_mcp_tool_schema_collection.items()
    for descrip in descrip_list
}


_all_schema_for_register: list[MCPSchema2ToolSchema] = [
    descrip 
    for descrip_list in _enum_2_mcp_tool_schema_collection.values() 
    for descrip in descrip_list
]

@traceable
def filter_schema_for_register(mcp_tool_name_list: list[str]) -> list[dict]:
    """根据工具名称列表过滤出需要注册的 MCP 工具描述"""
    return [ChatCompletionFunctionToolParam(
        type="function",
        function=FunctionDefinition(
            name=schema.name,
            description=schema.description,
            parameters=schema.inputSchema,  # 直接使用 MCP 的 inputSchema 作为工具的参数定义
        )
        ) 
            for schema in _all_schema_for_register 
            if schema.name in mcp_tool_name_list]

pass
