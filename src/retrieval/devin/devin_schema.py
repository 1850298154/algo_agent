from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any, Union

# -------------------------- 公共基础模型（抽离复用部分） --------------------------
class FastMcpMeta(BaseModel):
    """FastMCP专属元数据（Tool.meta._fastmcp）"""
    tags: List[str] = Field(
        default_factory=list,
        description="工具标签列表，用于分类/筛选，当前返回数据中均为空数组"
    )

class ToolMeta(BaseModel):
    """工具整体元数据"""
    _fastmcp: FastMcpMeta = Field(
        alias="_fastmcp",  # 适配原数据中的下划线字段
        description="FastMCP框架相关的元数据配置"
    )

class SchemaProperty(BaseModel):
    """Schema中单个参数的属性描述（如repoName/question的类型定义）"""
    type: Optional[str] = Field(
        None,
        description="参数基础类型，如'string'/'array'，部分字段会通过anyOf定义多类型"
    )
    anyOf: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="多类型兼容配置（如repoName支持string或string数组）"
    )
    items: Optional[Dict[str, Any]] = Field(
        None,
        description="当type为array时，定义数组元素的类型（如{'type': 'string'}）"
    )

class BaseSchema(BaseModel):
    """输入/输出Schema的公共基础结构"""
    properties: Dict[str, SchemaProperty] = Field(
        default_factory=dict,
        description="参数字典：key为参数名，value为参数的类型/规则描述"
    )
    required: List[str] = Field(
        default_factory=list,
        description="必填参数列表（如['repoName', 'question']）"
    )
    type: str = Field(
        default="object",
        description="Schema类型，固定为'object'（表示参数是键值对对象）"
    )

# -------------------------- 业务专属模型 --------------------------
class InputSchema(BaseSchema):
    """工具输入参数Schema（无额外字段，继承公共结构）"""
    pass

class OutputSchema(BaseSchema):
    """工具输出结果Schema（扩展FastMCP专属字段）"""
    x_fastmcp_wrap_result: bool = Field(
        alias="x-fastmcp-wrap-result",  # 适配原数据中的短横线字段
        default=True,
        description="FastMCP扩展字段：是否用'result'字段包裹输出结果（当前均为True）"
    )

class Tool(BaseModel):
    """MCP返回的GitHub仓库工具核心模型"""
    name: str = Field(
        description="工具唯一标识名（如'read_wiki_structure'/'ask_question'）"
    )
    title: Optional[str] = Field(
        None,
        description="工具展示标题（当前返回数据中均为None）"
    )
    description: str = Field(
        description="工具功能描述，包含作用和参数说明"
    )
    inputSchema: InputSchema = Field(
        alias="inputSchema",
        description="工具输入参数的Schema规范"
    )
    outputSchema: OutputSchema = Field(
        alias="outputSchema",
        description="工具输出结果的Schema规范"
    )
    icons: Optional[Any] = Field(
        None,
        description="工具图标信息（当前返回数据中均为None）"
    )
    annotations: Optional[Any] = Field(
        None,
        description="工具注解信息（当前返回数据中均为None）"
    )
    meta: ToolMeta = Field(
        description="工具元数据（包含FastMCP标签配置）"
    )
    execution: Optional[Any] = Field(
        None,
        description="工具执行配置（当前返回数据中均为None）"
    )

# -------------------------- 工具列表模型（可选） --------------------------
class ToolList(BaseModel):
    """GitHub仓库工具列表容器"""
    __root__: List[Tool] = Field(
        description="MCP返回的所有工具列表"
    )
