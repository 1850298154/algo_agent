"""
.. include:: ../README.md

https://info.arxiv.org/help/api/user-manual.html#query_details
"""

from __future__ import annotations

import logging
import time
import itertools
import feedparser
import os
import math
import re
import requests
import warnings
from urllib.parse import urlencode, urlparse
from urllib.request import urlretrieve
from datetime import datetime, timedelta, timezone
from calendar import timegm
from enum import Enum
from typing import TYPE_CHECKING, Generator, Iterator, Optional, List, Any

# 新增Pydantic导入
from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

if TYPE_CHECKING:
    from typing_extensions import TypedDict
    import feedparser

    class FeedParserDict(TypedDict, total=False):
        id: str
        title: str
        summary: str
        authors: list[dict[str, str]]
        links: list[dict[str, str]]
        tags: list[dict[str, str]]
        updated_parsed: time.struct_time
        published_parsed: time.struct_time
        arxiv_comment: str
        arxiv_journal_ref: str
        arxiv_doi: str
        arxiv_primary_category: dict[str, str]


logger = logging.getLogger(__name__)

_DEFAULT_TIME = datetime.min


# -------------------------- 改造核心：Pydantic模型 --------------------------
class ResultAuthor(BaseModel):
    """
    用于表示搜索结果作者的轻量级模型
    """
    name: str = Field(..., description="作者的姓名")

    model_config = ConfigDict(
        arbitrary_types_allowed=True,  # 允许非标准类型（兼容原有逻辑）
        json_encoders={
            datetime: lambda v: v.isoformat()  # datetime序列化为ISO格式字符串
        }
    )

    @classmethod
    def _from_feed_author(cls, feed_author: feedparser.FeedParserDict) -> "ResultAuthor":
        """
        从feed条目里的作者对象构造Author模型
        """
        return cls(name=feed_author.name)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"{_classname(self)}({repr(self.name)})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ResultAuthor):
            return self.name == other.name
        return False


class ResultLink(BaseModel):
    """
    用于表示搜索结果链接的轻量级模型
    """
    href: str = Field(..., description="链接的href属性（URL地址）")
    title: Optional[str] = Field(None, description="链接的标题")
    rel: str = Field("", description="链接与Result的关联关系")
    content_type: Optional[str] = Field(None, description="链接的HTTP内容类型")

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )

    @classmethod
    def _from_feed_link(cls, feed_link: feedparser.FeedParserDict) -> "ResultLink":
        """
        从feed条目里的链接对象构造Link模型
        """
        return cls(
            href=feed_link.href,
            title=feed_link.get("title"),
            rel=feed_link.get("rel") or "",
            content_type=feed_link.get("content_type"),
        )

    def __str__(self) -> str:
        return self.href

    def __repr__(self) -> str:
        return (
            f"{_classname(self)}({repr(self.href)}, title={repr(self.title)}, "
            f"rel={repr(self.rel)}, content_type={repr(self.content_type)})"
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ResultLink):
            return self.href == other.href
        return False


class Result(BaseModel):
    """
    arXiv查询结果feed中的一个条目

    参考：[arXiv API用户手册：返回的Atom结果详情](https://arxiv.org/help/api/user-manual#_details_of_atom_results_returned)
    """
    # 核心字段（全部带Field和中文注释）
    entry_id: str = Field(..., description="格式为`https://arxiv.org/abs/{id}`的URL")
    updated: datetime = Field(_DEFAULT_TIME, description="结果最后更新的时间（带UTC时区）")
    published: datetime = Field(_DEFAULT_TIME, description="结果最初发布的时间（带UTC时区）")
    title: str = Field("", description="结果的标题（自动去除多余空格）")
    authors: List[ResultAuthor] = Field([], description="结果的作者列表")
    summary: str = Field("", description="结果的摘要（abstract）")
    comment: Optional[str] = Field(None, description="作者的补充评论（如果有）")
    journal_ref: Optional[str] = Field(None, description="期刊引用信息（如果有）")
    doi: Optional[str] = Field(None, description="指向外部资源的DOI链接（如果有）")
    primary_category: str = Field("", description="结果的主要arXiv分类，参考：https://arxiv.org/category_taxonomy")
    categories: List[str] = Field([], description="结果的所有arXiv分类列表")
    links: List[ResultLink] = Field([], description="与该结果关联的URL列表（最多3个）")
    raw: Optional[feedparser.FeedParserDict] = Field(None, description="原始feedparser解析结果（仅调试用）")

    # 计算字段（序列化时自动包含）
    pdf_url: Optional[str] = Field(None, description="结果的PDF版本URL（从links中提取）")

    # Pydantic配置（关键：支持JSON序列化、兼容非标准类型）
    model_config = ConfigDict(
        arbitrary_types_allowed=True,  # 允许feedparser.FeedParserDict等非标准类型
        populate_by_name=True,  # 支持按字段名赋值
        json_encoders={
            # datetime序列化为ISO格式字符串（空值返回None）
            datetime: lambda v: v.isoformat() if v != _DEFAULT_TIME else None,
            # feedparser字典序列化为普通字典（方便JSON输出）
            feedparser.FeedParserDict: lambda v: dict(v) if v else None
        }
    )

    def __init__(self, **data):
        """
        重写初始化方法：自动计算pdf_url字段
        """
        # 从links中提取PDF URL（保持原有逻辑）
        links = data.get("links", [])
        data["pdf_url"] = self._get_pdf_url(links)
        super().__init__(**data)

    @classmethod
    def _from_feed_entry(cls, entry: feedparser.FeedParserDict) -> "Result":
        """
        将feedparser解析的arXiv条目转换为Result模型
        """
        if not hasattr(entry, "id"):
            raise cls.MissingFieldError("id")
        
        # 兼容标题缺失的bug（参考：https://github.com/lukasschwab/arxiv.py/issues/71）
        title = "0"
        if hasattr(entry, "title"):
            title = entry.title
        else:
            logger.warning("结果 %s 缺失标题属性；默认设为'0'", entry.id)

        # 构造模型入参
        return cls(
            entry_id=entry.id,
            updated=cls._to_datetime(entry.updated_parsed),
            published=cls._to_datetime(entry.published_parsed),
            title=re.sub(r"\s+", " ", title),
            authors=[ResultAuthor._from_feed_author(a) for a in entry.authors],
            summary=entry.summary,
            comment=entry.get("arxiv_comment"),
            journal_ref=entry.get("arxiv_journal_ref"),
            doi=entry.get("arxiv_doi"),
            primary_category=entry.arxiv_primary_category.get("term"),
            categories=[tag.get("term") for tag in entry.tags],
            links=[ResultLink._from_feed_link(link) for link in entry.links],
            _raw=entry,
        )

    def __str__(self) -> str:
        return self.entry_id

    def __repr__(self) -> str:
        return (
            f"{_classname(self)}(entry_id={repr(self.entry_id)}, updated={repr(self.updated)}, "
            f"published={repr(self.published)}, title={repr(self.title)}, authors={repr(self.authors)}, "
            f"summary={repr(self.summary)}, comment={repr(self.comment)}, journal_ref={repr(self.journal_ref)}, "
            f"doi={repr(self.doi)}, primary_category={repr(self.primary_category)}, "
            f"categories={repr(self.categories)}, links={repr(self.links)})"
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Result):
            return self.entry_id == other.entry_id
        return False

    def get_short_id(self) -> str:
        """
        返回结果的短ID（去除URL前缀）
        
        示例：
        - 完整URL: https://arxiv.org/abs/2107.05580v1 → 短ID: 2107.05580v1
        - 旧格式URL: https://arxiv.org/abs/quant-ph/0201082v1 → 短ID: quant-ph/0201082v1
        """
        return self.entry_id.split("arxiv.org/abs/")[-1]

    def _get_default_filename(self, extension: str = "pdf") -> str:
        """
        生成默认文件名（短ID + 标题 + 扩展名）
        """
        nonempty_title = self.title if self.title else "UNTITLED"
        return ".".join([
            self.get_short_id().replace("/", "_"),
            re.sub(r"[^\w]", "_", nonempty_title),
            extension,
        ])

    def download_pdf(
        self,
        dirpath: str = "./",
        filename: str = "",
        download_domain: str = "export.arxiv.org",
    ) -> str:
        """
        下载结果的PDF文件（已废弃：建议直接使用pdf_url）
        """
        if not filename:
            filename = self._get_default_filename()
        path = os.path.join(dirpath, filename)
        if self.pdf_url is None:
            raise ValueError("该结果没有可用的PDF URL")
        pdf_url = self._substitute_domain(self.pdf_url, download_domain)
        written_path, _ = urlretrieve(pdf_url, path)
        return written_path

    def download_source(
        self,
        dirpath: str = "./",
        filename: str = "",
        download_domain: str = "export.arxiv.org",
    ) -> str:
        """
        下载结果的源文件压缩包（已废弃：建议直接使用source_url）
        """
        if not filename:
            filename = self._get_default_filename("tar.gz")
        path = os.path.join(dirpath, filename)
        source_url_str = self.source_url()
        if source_url_str is None:
            raise ValueError("该结果没有可用的源文件URL")
        source_url = self._substitute_domain(source_url_str, download_domain)
        written_path, _ = urlretrieve(source_url, path)
        return written_path

    def source_url(self) -> Optional[str]:
        """
        推导结果的源文件压缩包URL（从PDF URL替换路径）
        """
        if self.pdf_url is None:
            return None
        return self.pdf_url.replace("/pdf/", "/src/")

    @staticmethod
    def _get_pdf_url(links: List[ResultLink]) -> Optional[str]:
        """
        从链接列表中提取PDF URL（优先取第一个）
        """
        pdf_urls = [link.href for link in links if link.title == "pdf"]
        if len(pdf_urls) == 0:
            return None
        elif len(pdf_urls) > 1:
            logger.warning("结果有多个PDF链接；使用第一个：%s", pdf_urls[0])
        return pdf_urls[0]

    @staticmethod
    def _to_datetime(ts: time.struct_time) -> datetime:
        """
        将UTC时间的struct_time转换为带时区的datetime对象
        """
        return datetime.fromtimestamp(timegm(ts), tz=timezone.utc)

    @staticmethod
    def _substitute_domain(url: str, domain: str) -> str:
        """
        替换URL的域名（用于测试）
        """
        parsed_url = urlparse(url)
        return parsed_url._replace(netloc=domain).geturl()

    class MissingFieldError(Exception):
        """
        条目缺失必填字段导致无法解析的异常
        """
        missing_field: str = Field("", description="缺失的必填字段名")
        message: str = Field("", description="异常描述信息")

        def __init__(self, missing_field: str):
            self.missing_field = missing_field
            self.message = f"来自arXiv的条目缺失必填字段：{missing_field}"
            super().__init__(self.message)

        def __repr__(self) -> str:
            return f"{_classname(self)}({repr(self.missing_field)})"


# -------------------------- 原有逻辑（无改动） --------------------------
class SortCriterion(Enum):
    """
    搜索结果的排序依据

    参考：[arXiv API用户手册：结果排序](https://arxiv.org/help/api/user-manual#sort)
    """
    Relevance = "relevance"
    LastUpdatedDate = "lastUpdatedDate"
    SubmittedDate = "submittedDate"


class SortOrder(Enum):
    """
    搜索结果的排序方向

    参考：[arXiv API用户手册：结果排序](https://arxiv.org/help/api/user-manual#sort)
    """
    Ascending = "ascending"
    Descending = "descending"


class Search:
    """
    arXiv数据库搜索的规格定义

    执行搜索：使用`Search.run`（默认客户端）或`Client.run`（自定义客户端）
    """
    query: str
    """
    搜索查询字符串（未编码）
    
    示例：au:del_maestro AND ti:checkerboard（而非au:del_maestro+AND+ti:checkerboard）
    参考：[arXiv API用户手册：查询构造](https://arxiv.org/help/api/user-manual#query_details)
    """
    id_list: list[str]
    """
    限制搜索范围的arXiv文章ID列表
    
    参考：[arXiv API用户手册：query与id_list的交互](https://arxiv.org/help/api/user-manual#search_query_and_id_list)
    """
    max_results: int | None
    """
    搜索返回的最大结果数（设为None则返回所有结果）
    
    API限制：单次查询最多返回300,000条结果
    """
    sort_by: SortCriterion
    """结果排序依据"""
    sort_order: SortOrder
    """结果排序方向"""

    def __init__(
        self,
        query: str = "",
        id_list: list[str] | None = None,
        max_results: int | None = None,
        sort_by: SortCriterion = SortCriterion.Relevance,
        sort_order: SortOrder = SortOrder.Descending,
    ):
        """构造arXiv API搜索条件"""
        self.query = query
        self.id_list = id_list or []
        self.max_results = None if max_results == math.inf else max_results
        self.sort_by = sort_by
        self.sort_order = sort_order

    def __str__(self) -> str:
        if self.query and self.id_list:
            return f"Search(query='{self.query}', id_list={len(self.id_list)} items)"
        elif self.query:
            return f"Search(query='{self.query}')"
        elif self.id_list:
            return f"Search(id_list={len(self.id_list)} items)"
        else:
            return "Search(empty)"

    def __repr__(self) -> str:
        return (
            "{}(query={}, id_list={}, max_results={}, sort_by={}, sort_order={})"
        ).format(
            _classname(self),
            repr(self.query),
            repr(self.id_list),
            repr(self.max_results),
            repr(self.sort_by),
            repr(self.sort_order),
        )

    def _url_args(self) -> dict[str, str]:
        """返回API请求的参数字典"""
        return {
            "search_query": self.query,
            "id_list": ",".join(self.id_list),
            "sortBy": self.sort_by.value,
            "sortOrder": self.sort_order.value,
        }

    def results(self, offset: int = 0) -> Iterator[Result]:
        """
        执行搜索（已废弃：建议使用Client.results）
        """
        warnings.warn(
            "The 'Search.results' method is deprecated, use 'Client.results' instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return Client().results(self, offset=offset)


class Client:
    """
    arXiv API结果获取策略定义（封装分页、重试逻辑）
    """
    query_url_format = "https://export.arxiv.org/api/query?{}"
    """arXiv查询API端点格式"""
    page_size: int
    """单次API请求获取的最大结果数（API限制：2000条/页）"""
    delay_seconds: float
    """API请求间隔（遵循arXiv要求：至少3秒）"""
    num_retries: int
    """失败请求的重试次数"""

    _last_request_dt: datetime | None
    _session: requests.Session

    def __init__(self, page_size: int = 100, delay_seconds: float = 3.0, num_retries: int = 3):
        """构造arXiv API客户端"""
        self.page_size = page_size
        self.delay_seconds = delay_seconds
        self.num_retries = num_retries
        self._last_request_dt = None
        self._session = requests.Session()

    def __str__(self) -> str:
        return f"Client(page_size={self.page_size}, delay={self.delay_seconds}s, retries={self.num_retries})"

    def __repr__(self) -> str:
        return "{}(page_size={}, delay_seconds={}, num_retries={})".format(
            _classname(self),
            repr(self.page_size),
            repr(self.delay_seconds),
            repr(self.num_retries),
        )

    def results(self, search: Search, offset: int = 0) -> Iterator[Result]:
        """
        按客户端配置获取搜索结果（生成器）
        """
        limit = search.max_results - offset if search.max_results else None
        if limit and limit < 0:
            return iter(())
        return itertools.islice(self._results(search, offset), limit)

    def _results(self, search: Search, offset: int = 0) -> Generator[Result, None, None]:
        """分页获取结果的内部生成器"""
        page_url = self._format_url(search, offset, self.page_size)
        feed = self._parse_feed(page_url, first_page=True)
        if not feed.entries:
            logger.info("首页无结果；停止生成")
            return
        total_results = int(feed.feed.opensearch_totalresults)
        logger.info("获取首页：%d / %d 条结果", len(feed.entries), total_results)

        while feed.entries:
            for entry in feed.entries:
                try:
                    yield Result._from_feed_entry(entry)
                except Result.MissingFieldError as e:
                    logger.warning("跳过不完整结果：%s", e)
            offset += len(feed.entries)
            if offset >= total_results:
                break
            page_url = self._format_url(search, offset, self.page_size)
            feed = self._parse_feed(page_url, first_page=False)

    def _format_url(self, search: Search, start: int, page_size: int) -> str:
        """构造分页请求的URL"""
        url_args = search._url_args()
        url_args.update({
            "start": str(start),
            "max_results": str(page_size),
        })
        return self.query_url_format.format(urlencode(url_args))

    def _parse_feed(
        self, url: str, first_page: bool = True, _try_index: int = 0
    ) -> feedparser.FeedParserDict:
        """获取并解析feed（带重试逻辑）"""
        try:
            return self.__try_parse_feed(url, first_page=first_page, try_index=_try_index)
        except (
            HTTPError,
            UnexpectedEmptyPageError,
            requests.exceptions.ConnectionError,
        ) as err:
            if _try_index < self.num_retries:
                logger.debug("请求失败（第%d次重试）：%s", _try_index, err)
                return self._parse_feed(url, first_page=first_page, _try_index=_try_index + 1)
            logger.debug("重试次数耗尽：%s", err)
            raise err

    def __try_parse_feed(
        self,
        url: str,
        first_page: bool,
        try_index: int,
    ) -> feedparser.FeedParserDict:
        """执行单次feed解析（含速率限制）"""
        # 速率限制：确保请求间隔≥delay_seconds
        if self._last_request_dt is not None:
            required = timedelta(seconds=self.delay_seconds)
            since_last = datetime.now() - self._last_request_dt
            if since_last < required:
                sleep_sec = (required - since_last).total_seconds()
                logger.info("速率限制：休眠%.2f秒", sleep_sec)
                time.sleep(sleep_sec)

        logger.info("请求页面（首页：%r，重试：%d）：%s", first_page, try_index, url)
        resp = self._session.get(url, headers={"user-agent": "arxiv.py/2.3.2"})
        self._last_request_dt = datetime.now()
        
        if resp.status_code != requests.codes.OK:
            raise HTTPError(url, try_index, resp.status_code)

        feed = feedparser.parse(resp.content)
        if len(feed.entries) == 0 and not first_page:
            raise UnexpectedEmptyPageError(url, try_index, feed)

        if feed.bozo:
            logger.warning("Feed解析异常：%s", feed.get("bozo_exception"))

        return feed


class ArxivError(Exception):
    """该包的基础异常类"""
    url: str
    """出错的feed URL"""
    retry: int
    """重试次数（0为首次请求）"""
    message: str
    """异常描述"""

    def __init__(self, url: str, retry: int, message: str):
        self.url = url
        self.retry = retry
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"{self.message}（URL：{self.url}）"


class UnexpectedEmptyPageError(ArxivError):
    """非首页返回空结果的异常（arXiv API偶发问题）"""
    raw_feed: feedparser.FeedParserDict
    """原始feedparser解析结果"""

    def __init__(self, url: str, retry: int, raw_feed: feedparser.FeedParserDict):
        self.raw_feed = raw_feed
        super().__init__(url, retry, "非首页结果为空")

    def __repr__(self) -> str:
        return f"{_classname(self)}({repr(self.url)}, {repr(self.retry)}, {repr(self.raw_feed)})"


class HTTPError(ArxivError):
    """请求返回非200状态码的异常"""
    status: int
    """HTTP状态码"""

    def __init__(self, url: str, retry: int, status: int):
        self.status = status
        super().__init__(url, retry, f"HTTP请求失败：状态码{status}")

    def __repr__(self) -> str:
        return f"{_classname(self)}({repr(self.url)}, {repr(self.retry)}, {repr(self.status)})"


def _classname(o: object) -> str:
    """辅助函数：生成类的完整名称（如arxiv.Result.Author）"""
    return f"arxiv.{o.__class__.__qualname__}"


# -------------------------- 测试示例（可删除） --------------------------
if __name__ == "__main__":
    # 测试：创建Result对象并序列化为JSON
    test_author = ResultAuthor(name="张三")
    test_link = ResultLink(
        href="https://arxiv.org/pdf/2107.05580v1.pdf",
        title="pdf",
        rel="alternate",
        content_type="application/pdf"
    )
    test_result = Result(
        entry_id="https://arxiv.org/abs/2107.05580v1",
        updated=datetime.now(timezone.utc),
        published=datetime.now(timezone.utc) - timedelta(days=1),
        title="测试标题",
        authors=[test_author],
        summary="测试摘要",
        comment="测试评论",
        journal_ref="测试期刊引用",
        doi="10.1234/test.2024",
        primary_category="cs.AI",
        categories=["cs.AI", "cs.LG"],
        links=[test_link]
    )
    
    # 序列化为JSON（缩进4格，忽略None值）
    json_str = test_result.model_dump_json(indent=4, exclude_none=True)
    print("Result JSON序列化结果：")
    print(json_str)
    
    # 1. 真实场景：调用 arxiv API 获取原生 Result 列表
    search = Search(
        query="cs.IR",
        max_results=1,
        sort_by=SortCriterion.SubmittedDate
    )
    client = Client(
        page_size=1,
        delay_seconds=0.34,  # 频率控制器已兜底，无需大延迟
        num_retries=2
    
    )
    original_results = list(client.results(search))
    print("原生 Result 列表：")
    for result in original_results:
        print(result.model_dump_json(indent=4, exclude_none=True))
    