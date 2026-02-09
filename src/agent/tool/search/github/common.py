from pydantic import Field, field_validator
from enum import Enum
from typing import Optional


class OrderEnum(str, Enum):
    """所有搜索功能通用的排序方向枚举"""
    ASC = "asc"
    DESC = "desc"


class SearchCodeSortEnum(str, Enum):
    """search_code 专属排序字段（仅支持 indexed）"""
    INDEXED = "indexed"


class SearchRepositoriesSortEnum(str, Enum):
    """search_repositories 专属排序字段"""
    STARS = "stars"
    FORKS = "forks"
    HELP_WANTED_ISSUES = "help-wanted-issues"
    UPDATED = "updated"


class BaseSearchRequest:
    """所有搜索请求的基础类（封装通用校验逻辑）"""
    @field_validator("query")
    def query_not_empty(cls, v):
        """通用校验：搜索关键词 query 不能为空"""
        if not v.strip():
            raise ValueError("搜索关键词 query 不能为空")
        return v

    # 通用可选参数的默认配置（所有搜索功能共用）
    _DEFAULT_PAGE = 1
    _DEFAULT_PER_PAGE = 30
    _DEFAULT_ORDER = OrderEnum.DESC