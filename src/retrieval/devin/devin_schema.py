from typing import List, Literal, Optional, Any
from pydantic import BaseModel, Field

# ==========================================
# 1. 公共组件模型 (Common Component Models)
# ==========================================

class ContentItem(BaseModel):
    """
    内容项模型
    表示 content 列表中的单个片段
    """
    type: str = Field(
        ..., 
        description="内容类型，例如 'text'"
    )
    text: str = Field(
        ..., 
        description="具体的文本内容。对于 TOC 是目录树字符串，对于 QA 是回答内容。"
    )

class StructuredOutput(BaseModel):
    """
    结构化输出模型
    对应 JSON 中的 structuredContent 字段
    """
    result: str = Field(
        ..., 
        description="原始的完整结果字符串，通常与 content 中的 text 内容对应。"
    )
    is_error: bool = Field(
        ..., 
        alias="isError", 
        description="错误标识位。False 表示执行成功，True 表示发生错误。"
    )

# ==========================================
# 2. 结果载体模型 (Result Payload Model)
# ==========================================

class AgentResult(BaseModel):
    """
    Agent 执行结果模型
    对应 JSON-RPC 中的 result 字段
    """
    content: List[ContentItem] = Field(
        ..., 
        description="由多个内容片段组成的列表，通常用于流式传输或分段展示。"
    )
    structured_content: StructuredOutput = Field(
        ..., 
        alias="structuredContent", 
        description="结构化的完整输出对象，包含结果文本和状态码。"
    )

# ==========================================
# 3. 顶层响应模型 (Top-Level Response Models)
# ==========================================

class BaseRpcResponse(BaseModel):
    """
    JSON-RPC 基础响应模型
    抽取了外层的通用协议字段
    """
    jsonrpc: Literal["2.0"] = Field(
        "2.0", 
        description="JSON-RPC 协议版本，固定为 '2.0'"
    )
    id: int = Field(
        ..., 
        description="请求/响应的唯一标识符 ID"
    )

# 虽然两者结构目前相同，但为了业务逻辑区分，
# 定义两个具体的类继承自同一结构。

class DevinTOCResponse(BaseRpcResponse):
    """
    Devin 目录结构(TOC) 响应模型
    """
    result: AgentResult = Field(
        ..., 
        description="包含项目代码和知识库融合后的目录结构(Table of Contents)的解析结果"
    )

class DevinQAResponse(BaseRpcResponse):
    """
    Devin 问答(QA) 响应模型
    """
    result: AgentResult = Field(
        ..., 
        description="包含 Agent 对用户提问的思考、工具调用结果及最终回答"
    )

# ==========================================
# 测试与验证
# ==========================================

if __name__ == "__main__":
    # 模拟数据输入
    toc_data = {'jsonrpc': '2.0', 'id': 1, 'result': {'content': [{'type': 'text', 'text': 'Available pages...\n- 1 Overview'}], 'structuredContent': {'result': 'Available pages...\n- 1 Overview', 'isError': False}}}
    qa_data = {'jsonrpc': '2.0', 'id': 1, 'result': {'content': [{'type': 'text', 'text': 'The agent coordinates...'}], 'structuredContent': {'result': 'The agent coordinates...', 'isError': False}}}

    # 验证 TOC 模型 (使用 parse_obj 来接受任意映射并由 pydantic 校验)
    toc_model = DevinTOCResponse.model_validate(toc_data)
    print(f"TOC 解析成功: ID={toc_model.id}, 文本长度={len(toc_model.result.structured_content.result)}")

    # 验证 QA 模型 (使用 parse_obj 来接受任意映射并由 pydantic 校验)
    qa_model = DevinQAResponse.model_validate(qa_data)
    print(f"QA  解析成功: ID={qa_model.id}, 文本长度={len(qa_model.result.structured_content.result)}")