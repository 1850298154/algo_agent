from pydantic import BaseModel, Field
from typing import Literal, Union, List, Optional


# ===================== 公共基础模型 =====================
class ContentItem(BaseModel):
    """Devin MCP API 响应中核心内容项"""
    type: Literal["text"] = Field(
        ...,
        description="内容类型，Devin MCP API 目前仅支持 'text' 类型"
    )
    text: str = Field(
        ...,
        description="核心文本内容：成功时返回仓库目录/问答结果；失败时返回错误提示（如仓库未找到、格式错误、认证异常等）"
    )


class StructuredContent(BaseModel):
    """Devin MCP API 响应中结构化内容（与 ContentItem.text 内容完全一致）"""
    result: str = Field(
        ...,
        description="结构化的文本结果，值与 content 数组中第一个元素的 text 字段完全相同"
    )


class CommonResult(BaseModel):
    """Devin MCP API 响应中通用的 Result 结构（成功/业务错误场景均适用）"""
    content: List[ContentItem] = Field(
        ...,
        min_length=1,
        max_length=1,
        description="核心内容数组，固定仅包含 1 个 ContentItem 元素"
    )
    structured_content: StructuredContent = Field(
        ...,
        alias="structuredContent",
        description="结构化内容对象，兼容 API 返回的驼峰命名字段"
    )
    is_error: bool = Field(
        ...,
        alias="isError",
        description="是否为错误结果（注意：业务错误时此字段仍为 false，需结合 content[0].text 关键词判断）"
    )


class JsonRpcBaseResponse(BaseModel):
    """JSON-RPC 2.0 基础响应结构（所有 Devin MCP API 有效响应均包含）"""
    jsonrpc: Literal["2.0"] = Field(
        ...,
        description="JSON-RPC 协议版本，固定为 '2.0'"
    )
    id: int = Field(
        ...,
        description="请求时传入的 ID，通常为 1"
    )


class ParseErrorResponse(BaseModel):
    """非标准响应：JSON 解析失败（如接口废弃、网络错误、Method Not Allowed 等场景）"""
    raw_error: Literal["Failed to parse JSON"] = Field(
        ...,
        description="解析错误标识，固定为 'Failed to parse JSON'"
    )
    content: str = Field(
        ...,
        description="原始错误文本（如 'Method Not Allowed'、网络错误信息等）"
    )


# ===================== 具体接口响应模型 =====================
class ReadWikiStructureResponse(JsonRpcBaseResponse):
    """获取仓库 Wiki 目录（read_wiki_structure）接口的响应模型"""
    result: CommonResult = Field(
        ...,
        description="接口返回的核心结果：成功时为仓库目录文本，失败时为错误提示"
    )


class AskQuestionResponse(JsonRpcBaseResponse):
    """仓库 Wiki 问答（ask_question）接口的响应模型"""
    result: CommonResult = Field(
        ...,
        description="接口返回的核心结果：成功时为问答结果文本，失败时为错误提示"
    )


# ===================== 联合类型：覆盖所有场景 =====================
# 获取目录接口的所有可能响应（正常响应 | 解析错误）
DevinTocResponse = Union[ReadWikiStructureResponse, ParseErrorResponse]

# 问答接口的所有可能响应（正常响应 | 解析错误）
DevinQaResponse = Union[AskQuestionResponse, ParseErrorResponse]

# ==========================================
# 测试与验证
# ==========================================
import requests
import json

# 示例：解析 devin_toc 的响应
def parse_toc_response(raw_response: str) -> DevinTocResponse:
    """解析获取仓库目录的 API 响应"""
    try:
        # 先尝试解析为正常响应
        data = json.loads(raw_response)
        return ReadWikiStructureResponse(**data)
    except (json.JSONDecodeError, ValueError):
        # 解析失败时，尝试匹配 ParseErrorResponse
        # （注：实际场景需根据 raw_response 构造 ParseErrorResponse）
        return ParseErrorResponse(
            raw_error="Failed to parse JSON",
            content=raw_response
        )

# 模拟 API 返回的成功响应
success_raw = '''
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [{"type": "text", "text": "Available pages for 1850298154/algo_agent:\\n\\n- 1 Overview"}],
    "structuredContent": {"result": "Available pages for 1850298154/algo_agent:\\n\\n- 1 Overview"},
    "isError": false
  }
}
'''

# 模拟 API 返回的解析错误响应
error_raw = 'Method Not Allowed'

# 解析成功响应
success_response = parse_toc_response(success_raw)
print("成功响应类型:", type(success_response))  # <class '__main__.ReadWikiStructureResponse'>
print("核心内容:", success_response.result.content[0].text)

# 解析错误响应
error_response = parse_toc_response(error_raw)
print("错误响应类型:", type(error_response))  # <class '__main__.ParseErrorResponse'>
print("错误信息:", error_response.content)


# if __name__ == "__main__":
#     # 模拟数据输入
#     toc_data = {'jsonrpc': '2.0', 'id': 1, 'result': {'content': [{'type': 'text', 'text': 'Available pages...\n- 1 Overview'}], 'structuredContent': {'result': 'Available pages...\n- 1 Overview', 'isError': False}}}
#     qa_data = {'jsonrpc': '2.0', 'id': 1, 'result': {'content': [{'type': 'text', 'text': 'The agent coordinates...'}], 'structuredContent': {'result': 'The agent coordinates...', 'isError': False}}}

#     # 验证 TOC 模型 (使用 parse_obj 来接受任意映射并由 pydantic 校验)
#     toc_model = DevinTocResponse.model_validate(toc_data)
#     print(f"TOC 解析成功: ID={toc_model.id}, 文本长度={len(toc_model.result.structured_content.result)}")

#     # 验证 QA 模型 (使用 parse_obj 来接受任意映射并由 pydantic 校验)
#     qa_model = DevinQaResponse.model_validate(qa_data)
#     print(f"QA  解析成功: ID={qa_model.id}, 文本长度={len(qa_model.result.structured_content.result)}")
