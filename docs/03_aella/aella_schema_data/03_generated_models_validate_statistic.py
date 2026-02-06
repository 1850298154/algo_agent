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

# --- 时间序列专用组件 ---
class TemporalPoint(BaseModel):
    year: int
    count: int

class TemporalClusterItem(BaseModel):
    """
    用于时间序列分析的聚类对象
    区别：没有顶层的 'count'，但有 'temporal_data' 列表
    """
    cluster_id: int
    cluster_label: str
    color: str
    temporal_data: List[TemporalPoint] = Field(..., description="年份与数量的对应关系列表")

# --- 论文节点模型 ---
class PaperNode(BasePaperMetadata, Coordinate3D):
    """论文节点模型"""
    id: int = Field(..., description="论文的唯一数据库 ID")

class PaperDetail(PaperNode):
    """论文详细信息模型"""
    sample: Optional[str] = Field(None, description="样本内容")
    summarization: Optional[str] = Field(None, description="摘要 (可能缺失)")
    nearest_papers: List['PaperNode'] = Field(default_factory=list)

class SampleDetail(BasePaperMetadata):
    """样本详细信息模型"""
    paper_id: int
    sample: Optional[str] = Field(None)
    summarization: Optional[str] = Field(None)

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

class TemporalDataResponse(BaseModel):
    """URL: /api/temporal-data"""
    # 修复：这里使用 TemporalClusterItem 而不是 ClusterItem
    clusters: List[TemporalClusterItem]

class SampleIdListResponse(BaseModel):
    """URL: /api/samples"""
    paper_ids: List[int]

class SampleDetailResponse(SampleDetail):
    """URL: /api/samples/{id}"""
    pass


# ==========================================
# 4. 统计与验证逻辑
# ==========================================

class SchemaValidator:
    def __init__(self, base_path="."):
        self.base_path = base_path
        # 映射配置
        self.file_mapping = {
            "1_papers.json": PaperListResponse,
            "2_papers,18721.json": PaperDetailResponse,
            "3_clusters.json": ClusterListResponse,
            "4_search.json": SearchResponse,
            "5_temporal-data.json": TemporalDataResponse,
            "6_samples.json": SampleIdListResponse,
            "7_samples,29.json": SampleDetailResponse
        }

    def _analyze_missing_stats(self, data: Any, path: str, stats: Dict):
        """递归统计字段缺失情况"""
        if isinstance(data, dict):
            for key, value in data.items():
                current_path = f"{path}.{key}" if path else key
                stats[current_path]['total'] += 1
                if value is None:
                    stats[current_path]['missing'] += 1
                
                # 递归处理嵌套对象
                if isinstance(value, (dict, list)):
                    self._analyze_missing_stats(value, current_path, stats)
                    
        elif isinstance(data, list):
            # 对于列表，我们只统计列表项的结构，路径加上 []
            list_path = f"{path}[]"
            for item in data:
                self._analyze_missing_stats(item, list_path, stats)

    def print_stats_table(self, filename: str, data: Any):
        """打印缺失率表格"""
        stats = defaultdict(lambda: {'total': 0, 'missing': 0})
        self._analyze_missing_stats(data, "", stats)

        # 过滤掉 total=0 的（空列表情况）以及完全没有缺失的（为了版面整洁，可选）
        relevant_stats = []
        for path, count in stats.items():
            # 只显示 total > 0 的字段
            if count['total'] > 0:
                pct = (count['missing'] / count['total']) * 100
                if pct > 0: # 只显示有缺失的字段
                    relevant_stats.append((path, count['total'], count['missing'], pct))
        
        if not relevant_stats:
            return # 没有缺失数据，不打印表格

        relevant_stats.sort(key=lambda x: x[3], reverse=True) # 按缺失率排序

        print(f"\n   [统计] 字段缺失率分析: {os.path.basename(filename)}")
        print(f"   {'-'*75}")
        print(f"   {'Field Chain':<40} | {'Total':<8} | {'Null':<6} | {'Missing %'}")
        print(f"   {'-'*75}")
        for path, total, missing, pct in relevant_stats:
            # 缩短过长的路径
            display_path = (path[:37] + '..') if len(path) > 37 else path
            print(f"   {display_path:<40} | {total:<8} | {missing:<6} | {pct:>8.1f}%")
        print(f"   {'-'*75}\n")

    def run(self):
        print(f"{'File Name':<45} | {'Status':<10} | {'Message'}")
        print("=" * 100)

        for filename, model_class in self.file_mapping.items():
            # 兼容绝对路径和相对路径
            full_path = filename 
            if not os.path.exists(full_path) and os.path.exists(os.path.join(self.base_path, filename)):
                full_path = os.path.join(self.base_path, filename)

            display_name = os.path.basename(filename)
            
            if not os.path.exists(full_path):
                print(f"{display_name:<45} | MISSING    | 文件未找到")
                continue

            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # 1. 验证 Schema
                model_class.model_validate(data)
                
                print(f"{display_name:<45} | ✅ PASS    | {model_class.__doc__.strip()}")
                
                # 2. 如果验证通过，进行缺失值统计
                self.print_stats_table(full_path, data)

            except ValidationError as e:
                error_count = len(e.errors())
                first = e.errors()[0]
                loc = "->".join(str(x) for x in first['loc'])
                msg = first['msg']
                print(f"{display_name:<45} | ❌ FAIL    | {error_count} errors. First: [{loc}] {msg}")
            except json.JSONDecodeError:
                print(f"{display_name:<45} | ❌ FAIL    | JSON 格式错误")
            except Exception as e:
                print(f"{display_name:<45} | ❌ FAIL    | {str(e)}")

# ==========================================
# 5. 执行入口
# ==========================================
if __name__ == "__main__":
    # 你可以修改这里的路径，指向你存放 json 文件的实际目录
    # 如果文件就在当前目录，可以留空或 "."
    # 假设你的文件在 docs/03_aella/aella_api_req/ 下：
    input_dir = r"docs/03_aella/aella_api_req" 
    
    # 如果你在当前目录运行且文件也在当前目录
    if not os.path.exists(input_dir):
        input_dir = "." 
        
    validator = SchemaValidator(input_dir)
    validator.run()
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

5_temporal-data.json                          | ✅ PASS    | URL: /api/temporal-data
6_samples.json                                | ✅ PASS    | URL: /api/samples
7_samples,29.json                             | ✅ PASS    | URL: /api/samples/{id}

   [统计] 字段缺失率分析: 7_samples,29.json
   ---------------------------------------------------------------------------
   Field Chain                              | Total    | Null   | Missing %
   ---------------------------------------------------------------------------
   publication_year                         | 1        | 1      |    100.0%
   ---------------------------------------------------------------------------

"""