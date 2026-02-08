from pydantic import BaseModel, Field, computed_field, model_validator
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any, Iterable
import re
from urllib.parse import urlparse

# ------------------- 先粘贴我们定义的 Pydantic 模型（完整） -------------------
class Author(BaseModel):
    """
    A light inner class for representing a result's authors.
    """
    name: str = Field(..., description="The author's name.")

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Author):
            return self.name == other.name
        return False


class Link(BaseModel):
    """
    A light inner class for representing a result's links.
    """
    # href: str = Field(..., description="The link's `href` attribute.")
    url: str = Field(..., description="链接地址，例如 'https://arxiv.org/abs/2602.05975v1'")
    title: Optional[str] = Field(None, description="The link's title.")
    rel: str = Field("", description="The link's relationship to the `Result`.")
    content_type: Optional[str] = Field(None, description="The link's HTTP content type.")

    # def __str__(self) -> str:
    #     return self.href

    # def __eq__(self, other: object) -> bool:
    #     if isinstance(other, Link):
    #         return self.href == other.href
    #     return False


class MissingFieldError(Exception):
    """
    An error indicating an entry is unparseable because it lacks required
    fields.
    """
    missing_field: str
    message: str

    def __init__(self, missing_field: str):
        self.missing_field = missing_field
        self.message = "Entry from arXiv missing required info"
        super().__init__(self.message)

    def __repr__(self) -> str:
        return f"MissingFieldError({repr(self.missing_field)})"


class ArxivResult(BaseModel):
    """
    An entry in an arXiv query results feed.
    """
    entry_id: str = Field(..., description="A url of the form `https://arxiv.org/abs/{id}`.")
    updated: datetime = Field(..., description="When the result was last updated.")
    published: datetime = Field(..., description="When the result was originally published.")
    title: str = Field("", description="The title of the result.")
    authors: List[Author] = Field(default_factory=list, description="The result's authors.")
    summary: str = Field("", description="The result abstract.")
    comment: Optional[str] = Field(None, description="The authors' comment if present.")
    journal_ref: Optional[str] = Field(None, description="A journal reference if present.")
    doi: Optional[str] = Field(None, description="A URL for the resolved DOI to an external resource if present.")
    primary_category: str = Field("", description="The result's primary arXiv category.")
    categories: List[str] = Field(default_factory=list, description="All of the result's categories.")
    links: List[Link] = Field(default_factory=list, description="Up to three URLs associated with this result.")
    # pdf_url: Optional[str] = Field(None, description="The URL of a PDF version of this result.")

    # @model_validator(mode='after')
    # def set_pdf_url(self) -> 'ArxivResult':
    #     pdf_urls = [link.href for link in self.links if link.title == "pdf"]
    #     if len(pdf_urls) == 0:
    #         self.pdf_url = None
    #     elif len(pdf_urls) > 1:
    #         print(f"Warning: Result has multiple PDF links; using {pdf_urls[0]}")
    #         self.pdf_url = pdf_urls[0]
    #     else:
    #         self.pdf_url = pdf_urls[0]
    #     return self
    @computed_field(return_type=str)
    def pdf_url(self) -> str:
        pdf_urls = [link.href for link in self.links if link.title == "pdf"]
        return pdf_urls[0]

    def get_short_id(self) -> str:
        return self.entry_id.split("arxiv.org/abs/")[-1]

    def _get_default_filename(self, extension: str = "pdf") -> str:
        nonempty_title = self.title if self.title else "UNTITLED"
        return ".".join(
            [
                self.get_short_id().replace("/", "_"),
                re.sub(r"[^\w]", "_", nonempty_title),
                extension,
            ]
        )

    def source_url(self) -> Optional[str]:
        if self.pdf_url is None:
            return None
        return self.pdf_url.replace("/pdf/", "/src/")

    @staticmethod
    def _substitute_domain(url: str, domain: str) -> str:
        parsed_url = urlparse(url)
        return parsed_url._replace(netloc=domain).geturl()

    class Config:
        eq_mode = "attributes"
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# ------------------- 核心转换函数（重点） -------------------
def convert_arxiv_result_to_pydantic(original_result) -> ArxivResult:
    """
    将 arxiv 库原生的 Result 实例转换为我们定义的 Pydantic Result 模型
    
    Args:
        original_result: arxiv 库返回的原生 Result 实例
    
    Returns:
        转换后的 Pydantic Result 模型实例
    """
    # 1. 转换嵌套的 Author 列表
    pydantic_authors = [
        Author(name=author.name) 
        for author in original_result.authors
    ]
    
    # 2. 转换嵌套的 Link 列表
    pydantic_links = [
        Link(
            url=link.href,
            title=link.title,
            rel=link.rel,
            content_type=link.content_type
        ) 
        for link in original_result.links
    ]
        
    # 4. 构造 Pydantic 模型实例（字段一一映射）
    pydantic_result = ArxivResult(
        entry_id=original_result.entry_id,
        updated=original_result.updated,
        published=original_result.published,
        title=original_result.title,
        authors=pydantic_authors,
        summary=original_result.summary,
        comment=original_result.comment or None,  # 处理空字符串 → None
        journal_ref=original_result.journal_ref or None,
        doi=original_result.doi or None,
        primary_category=original_result.primary_category,
        categories=original_result.categories,
        links=pydantic_links,
        # pdf_url 无需手动传，model_validator 会自动推导
    )
    
    return pydantic_result

def convert_arxiv_results_to_pydantic_list(original_results: Iterable) -> List[ArxivResult]:
    """
    批量转换 arxiv 库返回的 Result 列表为 Pydantic 模型列表
    
    Args:
        original_results: arxiv 库返回的原生 Result 实例列表/可迭代对象
    
    Returns:
        转换后的 Pydantic Result 模型列表
    """
    return [convert_arxiv_result_to_pydantic(res) for res in original_results]

# ------------------- 实际使用示例 -------------------
if __name__ == "__main__":
    # 模拟：你从 arxiv 库获取的原生 Result 列表
    # （实际使用时替换为你真实的 arxiv 查询结果）
    import arxiv

    # 1. 真实场景：调用 arxiv API 获取原生 Result 列表
    search = arxiv.Search(
        query="cs.IR",
        max_results=2,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    client = arxiv.Client(
        page_size=50,
        delay_seconds=0.34,  # 频率控制器已兜底，无需大延迟
        num_retries=2
    
    )
    original_results = list(client.results(search))
    
    # 2. 转换为 Pydantic 列表
    pydantic_results = convert_arxiv_results_to_pydantic_list(original_results)
    
    # 3. 使用 Pydantic 模型的优势：验证、序列化、字段检查
    for res in pydantic_results:
        print("=== 转换后的 Pydantic 模型 ===")
        print(f"标题: {res.title}")
        print(f"PDF 链接: {res.pdf_url}")
        print(f"作者: {[author.name for author in res.authors]}")
        # 序列化为 JSON（Pydantic 原生能力）
        print(f"JSON 序列化:\n{res.model_dump_json(indent=2)}\n")