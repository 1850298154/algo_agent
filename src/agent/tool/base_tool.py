from pydantic import BaseModel, Field, ValidationError
from typing import Dict, Type, Any, Optional, Literal, List
import inspect
import inflection

# ---------------------- 工具基类（统一接口） ----------------------
class BaseTool(BaseModel):
    """所有工具的基类，定义统一接口"""
    @classmethod
    def tool_name(cls) -> str:
        """工具唯一标识名（用于路由匹配，如 "weatherquery"）"""
        return inflection.underscore(
            cls.__name__.replace("Tool", "").replace("tool", "")
            )  # 自动生成工具名

    @classmethod
    def tool_description(cls) -> str:
        """工具描述（供 Agent 理解用途）"""
        return inspect.getdoc(cls) or "无工具描述"

    @classmethod
    def get_parameter_schema(cls) -> dict:
        """获取参数 JSON Schema（供 Agent 构造参数）"""
        return cls.model_json_schema()
    
    @classmethod
    def get_tool_schema(cls) -> str:
        """
        获取工具参数描述（供 Agent 理解参数含义）
        例子：
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "当你想查询指定城市的天气时非常有用。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        # 查询天气时需要提供位置，因此参数设置为location
                        "location": {
                            "type": "string",
                            "description": "城市或县区，比如北京市、杭州市、余杭区等。",
                        }
                    },
                    "required": ["location"],
                },
            },
        },   
        """
        tool_schema = {
            "type": "function",
            "function": {
                "name": cls.tool_name(),  # 调用同类的类函数 tool_name
                "description": cls.tool_description(),  # 调用同类的类函数 tool_description
                "parameters": cls.get_parameter_schema()  # 调用同类的类函数 get_parameter_schema
            }
        }
        return tool_schema

    def run(self) -> str:
        """工具核心执行逻辑（子类必须实现）"""
        raise NotImplementedError("所有工具必须实现 run 方法")
