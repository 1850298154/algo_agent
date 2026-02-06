import json
import os
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError

# ==========================================
# 1. Pydantic Schema 定义 (复用上一段代码)
# ==========================================

class Coordinate3D(BaseModel):
    """3D 空间坐标组件"""
    x: float = Field(..., description="UMAP/t-SNE 降维后的 X 轴坐标")
    y: float = Field(..., description="UMAP/t-SNE 降维后的 Y 轴坐标")
    z: float = Field(..., description="UMAP/t-SNE 降维后的 Z 轴坐标")

class BasePaperMetadata(BaseModel):
    """论文基础元数据"""
    title: str = Field(..., description="论文标题")
    cluster_id: int = Field(..., description="所属聚类的唯一 ID")
    cluster_label: str = Field(..., description="聚类的人类可读标签")
    field_subfield: str = Field(..., description="领域/子领域分类路径")
    publication_year: Optional[int] = Field(None, description="出版年份")
    classification: str = Field(..., description="论文的大类分类")

class ClusterItem(BaseModel):
    cluster_id: int
    cluster_label: str
    count: int
    color: str

class PaperNode(BasePaperMetadata, Coordinate3D):
    """论文节点模型"""
    id: int = Field(..., description="论文的唯一数据库 ID")

class PaperDetail(PaperNode):
    """论文详细信息模型"""
    sample: Optional[str] = Field(None)
    summarization: str
    nearest_papers: List['PaperNode'] = Field(default_factory=list)

class SampleDetail(BasePaperMetadata):
    """样本详细信息模型"""
    paper_id: int
    sample: str
    summarization: str

# --- Response Models ---
# 对应url分别是：
# 1. /api/papers -> PaperListResponse
# 2. /api/papers/{id} -> PaperDetailResponse
# 3. /api/clusters -> ClusterListResponse
# 4. /api/search -> SearchResponse
# 5. /api/temporal-data -> TemporalDataResponse
# 6. /api/samples -> SampleIdListResponse
# 7. /api/samples/{id} -> SampleDetailResponse
class PaperListResponse(BaseModel):
    papers: List[PaperNode]

class PaperDetailResponse(PaperDetail):
    pass

class ClusterListResponse(BaseModel):
    clusters: List[ClusterItem]

class SearchResponse(BaseModel):
    papers: List[PaperNode]

class TemporalDataResponse(BaseModel):
    clusters: List[ClusterItem]

class SampleIdListResponse(BaseModel):
    paper_ids: List[int]

class SampleDetailResponse(SampleDetail):
    pass


# ==========================================
# 2. 验证逻辑 (Verification Logic)
# ==========================================

def verify_files():
    # 定义文件名与对应的 Pydantic 模型映射关系
    # 请确保文件名与你实际生成的一致
    file_mapping: dict[str, type[BaseModel]] = {
        "1_papers.json": PaperListResponse,
        "2_papers,18721.json": PaperDetailResponse,
        "3_clusters.json": ClusterListResponse,
        "4_search.json": SearchResponse,
        "5_temporal-data.json": TemporalDataResponse,
        "6_samples.json": SampleIdListResponse,
        "7_samples,29.json": SampleDetailResponse
    }

    print(f"{'File Name':<30} | {'Status':<10} | {'Message'}")
    print("-" * 80)

    for filename, model_class in file_mapping.items():
        filename = os.path.join("docs/03_aella/aella_api_req", filename)
        status = "UNKNOWN"
        message = ""
        
        if not os.path.exists(filename):
            status = "MISSING"
            message = "文件不存在"
        else:
            try:
                # 1. 读取文件
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 2. 验证数据 (Pydantic V2 使用 model_validate)
                # 如果你使用的是 Pydantic V1，请使用 model_class.parse_obj(data)
                model_class.model_validate(data)
                
                status = "✅ PASS"
                message = f"成功匹配 {model_class.__name__}"
                
            except ValidationError as e:
                status = "❌ FAIL"
                # 提取第一个错误的摘要
                error_count = len(e.errors())
                first_error = e.errors()[0]
                field_path = "->".join([str(x) for x in first_error['loc']])
                message = f"{error_count} errors. First at [{field_path}]: {first_error['msg']}"
            except json.JSONDecodeError:
                status = "❌ FAIL"
                message = "JSON 格式无效"
            except Exception as e:
                status = "❌ FAIL"
                message = f"未知错误: {str(e)}"

        # 打印结果行
        print(f"{filename:<30} | {status:<10} | {message}")

if __name__ == "__main__":
    verify_files()