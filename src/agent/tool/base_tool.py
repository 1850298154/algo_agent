from pydantic import BaseModel, Field, ValidationError
from typing import Dict, Type, Any, Optional, Literal, List
import inspect

# ---------------------- 工具基类（统一接口） ----------------------
class BaseTool(BaseModel):
    """所有工具的基类，定义统一接口"""
    @classmethod
    def tool_name(cls) -> str:
        """工具唯一标识名（用于路由匹配，如 "weatherquery"）"""
        return cls.__name__.lower().replace("tool", "")  # 自动生成工具名

    @classmethod
    def tool_description(cls) -> str:
        """工具描述（供 Agent 理解用途）"""
        return inspect.getdoc(cls) or "无工具描述"

    def run(self) -> str:
        """工具核心执行逻辑（子类必须实现）"""
        raise NotImplementedError("所有工具必须实现 run 方法")

    @classmethod
    def get_parameter_schema(cls) -> dict:
        """获取参数 JSON Schema（供 Agent 构造参数）"""
        return cls.model_json_schema()