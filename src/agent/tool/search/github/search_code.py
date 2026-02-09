from pydantic import BaseModel, Field
from typing import Optional
from src.agent.tool.search.github.common import (
    OrderEnum,
    SearchCodeSortEnum,
    BaseSearchRequest
)


class SearchCodeInput(BaseModel, BaseSearchRequest):
    """search_code 功能专属请求模型（严格校验参数约束）"""
    # 必填参数：GitHub 代码搜索语法
    query: str
    
    # 可选参数：排序方向（默认降序）
    order: Optional[OrderEnum] = Field(
        default=BaseSearchRequest._DEFAULT_ORDER,
        description="排序方向：asc（升序）/desc（降序）"
    )
    
    # 可选参数：页码（最小值 1）
    page: Optional[int] = Field(
        default=BaseSearchRequest._DEFAULT_PAGE,
        ge=1,
        description="页码，最小为 1"
    )
    
    # 可选参数：每页结果数（1-100）
    perPage: Optional[int] = Field(
        default=BaseSearchRequest._DEFAULT_PER_PAGE,
        ge=1,
        le=100,
        description="每页结果数，范围 1-100"
    )
    
    # 可选参数：排序字段（仅支持 indexed）
    sort: Optional[SearchCodeSortEnum] = Field(
        default=SearchCodeSortEnum.INDEXED,
        description="排序字段，仅支持 indexed（按索引时间）"
    )


# 测试示例
if __name__ == "__main__":
    input_data = SearchCodeInput(
        query="content:def calculate_total language:Python repo:python/cpython",
        perPage=50
    )
    print("search_code 请求参数校验通过：", input_data.model_dump())