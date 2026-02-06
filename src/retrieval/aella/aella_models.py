import json
import os
from collections import defaultdict
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, ValidationError

# ==========================================
# 1. 基础组件 (Base Components)
# ==========================================

class Coordinate3D(BaseModel):
    """3D 空间坐标组件"""
    x: float = Field(..., description="UMAP/t-SNE 降维后的 X 轴坐标")
    y: float = Field(..., description="UMAP/t-SNE 降维后的 Y 轴坐标")
    z: float = Field(..., description="UMAP/t-SNE 降维后的 Z 轴坐标")

class BasePaperMetadata(BaseModel):
    """
    论文基础元数据
    修复：大量字段改为 Optional，因为存在 id=895 这种 title 为 null 的情况
    """
    title: Optional[str] = Field(None, description="论文标题 (可能为 null，如果是 PARTIAL_TEXT)")
    cluster_id: int = Field(..., description="所属聚类的唯一 ID")
    cluster_label: str = Field(..., description="聚类的人类可读标签")
    field_subfield: Optional[str] = Field(None, description="领域/子领域分类路径 (可能缺失)")
    publication_year: Optional[int] = Field(None, description="出版年份 (可能缺失)")
    classification: Optional[str] = Field(None, description="论文的大类分类")

# ==========================================
# 2. 核心数据模型
# ==========================================

# --- 标准聚类模型 ---
class ClusterItem(BaseModel):
    """用于列表展示的标准聚类对象"""
    cluster_id: int
    cluster_label: str
    count: int = Field(..., description="该聚类下的论文总数")
    color: str

# --- 论文节点模型 ---
class PaperNode(BasePaperMetadata, Coordinate3D):
    """论文节点模型"""
    id: int = Field(..., description="论文的唯一数据库 ID")

class PaperDetail(PaperNode):
    """论文详细信息模型"""
    sample: Optional[str] = Field(None, description="样本内容")
    summarization: Optional[str] = Field(None, description="摘要 (可能缺失)")
    nearest_papers: List['PaperNode'] = Field(default_factory=list)

# ==========================================
# 3. 响应模型 (API Response Models)
# ==========================================

class PaperListResponse(BaseModel):
    """URL: /api/papers"""
    papers: List[PaperNode]

class PaperDetailResponse(PaperDetail):
    """URL: /api/papers/{id}"""
    pass

class ClusterListResponse(BaseModel):
    """URL: /api/clusters"""
    clusters: List[ClusterItem]

class SearchResponse(BaseModel):
    """URL: /api/search"""
    papers: List[PaperNode]



"""
File Name                                     | Status     | Message
====================================================================================================
1_papers.json                                 | ✅ PASS    | URL: /api/papers

   [统计] 字段缺失率分析: 1_papers.json
   ---------------------------------------------------------------------------
   Field Chain                              | Total    | Null   | Missing %
   ---------------------------------------------------------------------------
   papers[].publication_year                | 89008    | 41365  |     46.5%
   papers[].title                           | 89008    | 8      |      0.0%
   papers[].field_subfield                  | 89008    | 8      |      0.0%
   ---------------------------------------------------------------------------

2_papers,18721.json                           | ✅ PASS    | URL: /api/papers/{id}

   [统计] 字段缺失率分析: 2_papers,18721.json
   ---------------------------------------------------------------------------
   Field Chain                              | Total    | Null   | Missing %
   ---------------------------------------------------------------------------
   sample                                   | 1        | 1      |    100.0%
   nearest_papers[].publication_year        | 15       | 2      |     13.3%
   ---------------------------------------------------------------------------

3_clusters.json                               | ✅ PASS    | URL: /api/clusters
4_search.json                                 | ✅ PASS    | URL: /api/search

   [统计] 字段缺失率分析: 4_search.json
   ---------------------------------------------------------------------------
   Field Chain                              | Total    | Null   | Missing %
   ---------------------------------------------------------------------------
   papers[].publication_year                | 70       | 28     |     40.0%
   ---------------------------------------------------------------------------

"""