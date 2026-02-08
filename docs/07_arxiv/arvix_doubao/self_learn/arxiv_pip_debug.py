import string

def sanitize_filename(filename: str, replace_char: str = '-') -> str:
    """
    清理文件名中的非法字符，兼容Windows/macOS/Linux
    :param filename: 原始文件名
    :param replace_char: 替换非法字符的目标字符（默认-）
    :return: 安全的文件名
    """
    # 1. 定义所有系统的非法字符集合（核心）
    illegal_chars = {
        # Windows核心非法字符
        '<', '>', ':', '"', '/', '\\', '|', '?', '*',
        # macOS核心非法字符
        ':',
        # Linux核心非法字符
        '/', '\0'  # \0是NULL字符，实际文件名中几乎不会出现，但仍做处理
    }
    # 2. 加入ASCII控制字符（0-31），提升兼容性
    control_chars = set(chr(c) for c in range(32))
    illegal_chars.update(control_chars)
    
    # 3. 创建字符替换映射表（高效批量替换）
    trans_table = str.maketrans({char: replace_char for char in illegal_chars})
    safe_filename = filename.translate(trans_table)
    
    # 4. 处理Windows保留文件名（如CON、PRN等）
    windows_reserved_names = {
        'CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4',
        'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2',
        'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
    }
    # 提取文件名主体（去掉扩展名）判断是否为保留名
    name_part = safe_filename.split('.')[0].upper()
    if name_part in windows_reserved_names:
        safe_filename = f"{safe_filename}{replace_char}"
    
    # 5. 处理末尾的空格/点（Windows禁止）
    safe_filename = safe_filename.rstrip(' .')
    
    # 6. 兜底：如果处理后为空，返回默认名
    if not safe_filename:
        safe_filename = f"unnamed{replace_char}"
    
    return safe_filename
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# 定义嵌套的作者模型（对应 arxiv.Result.Author）
class Author(BaseModel):
    """arxiv 论文的作者信息模型"""
    name: str  # 作者姓名，如 'Tiansheng Hu'

# 定义嵌套的链接模型（对应 arxiv.Result.Link）
class Link(BaseModel):
    """arxiv 论文的链接信息模型"""
    url: str          # 链接地址，如 'https://arxiv.org/abs/2602.05975v1'
    title: Optional[str] = None  # 链接标题（可选，可为 None）
    rel: str          # 链接关系，如 'alternate'/'related'
    content_type: Optional[str] = None  # 内容类型（可选，可为 None）

# 定义核心的 Result 模型（对应 arxiv.Result）
class Result(BaseModel):
    """arxiv 论文查询结果的核心模型"""
    entry_id: str               # 论文唯一标识 URL
    updated: datetime           # 更新时间（带 UTC 时区的 datetime 对象）
    published: datetime         # 发布时间（带 UTC 时区的 datetime 对象）
    title: str                  # 论文标题
    authors: List[Author]       # 作者列表（嵌套 Author 模型）
    summary: str                # 论文摘要
    comment: Optional[str] = None  # 论文备注（可选）
    journal_ref: Optional[str] = None  # 期刊引用（可选，可为 None）
    doi: Optional[str] = None   # DOI 编号（可选，可为 None）
    primary_category: str       # 主要分类，如 'cs.IR'
    categories: List[str]       # 所有分类列表，如 ['cs.IR', 'cs.CL']
    links: List[Link]           # 链接列表（嵌套 Link 模型）

# ------------------- 示例：创建模型实例（匹配你提供的示例数据） -------------------

import arxiv
import requests
search = arxiv.Search(
    query="LLM AND agent AND (RAG OR retrieval)",
    max_results=53,
    sort_by=arxiv.SortCriterion.SubmittedDate,
)

# for result in search.results():
#     print(result.title, result.authors, result.entry_id)
    
# import arxiv

# # 搜索
# search = arxiv.Search(
#     id_list=["2307.12345"],  # 直接用 arXiv ID
#     max_results=2,
# )

for result in search.results():
    print(result.title)
    print(result.entry_id)   # 包含 arXiv ID
    print(result.pdf_url)    # PDF 下载链接
    
    # 获取 BibTeX（拼接链接即可）
    bib_url = f"https://arxiv.org/bibtex/{result.get_short_id()}"
    # 再请求该 URL 就能拿到 BibTeX 字符串
    bib_response = requests.get(bib_url)
    print(bib_response.text)
    result.download_source(
        sanitize_filename(result.title),
        sanitize_filename(result.title),
        )    # 自动下载 PDF
    result.download_pdf(
        sanitize_filename(result.title),
        sanitize_filename(result.title),
        )    # 自动下载 PDF

pass
pass
pass
pass
"""
arxiv.Result(entry_id='http://arxiv.org/abs/2602.05975v1', updated=datetime.datetime(2026, 2, 5, 18, 25, 24, tzinfo=datetime.timezone.utc), published=datetime.datetime(2026, 2, 5, 18, 25, 24, tzinfo=datetime.timezone.utc), title='SAGE: Benchmarking and Improving Retrieval for Deep Research Agents', authors=[arxiv.Result.Author('Tiansheng Hu'), arxiv.Result.Author('Yilun Zhao'), arxiv.Result.Author('Canyu Zhang'), arxiv.Result.Author('Arman Cohan'), arxiv.Result.Author('Chen Zhao')], summary='Deep research agents have emerged as powerful systems for addressing complex queries. Meanwhile, LLM-based retrievers have demonstrated strong capability in following instructions or reasoning. This raises a critical question: can LLM-based retrievers effectively contribute to deep research agent workflows? To investigate this, we introduce SAGE, a benchmark for scientific literature retrieval comprising 1,200 queries across four scientific domains, with a 200,000 paper retrieval corpus.We evaluate six deep research agents and find that all systems struggle with reasoning-intensive retrieval. Using DR Tulu as backbone, we further compare BM25 and LLM-based retrievers (i.e., ReasonIR and gte-Qwen2-7B-instruct) as alternative search tools. Surprisingly, BM25 significantly outperforms LLM-based retrievers by approximately 30%, as existing agents generate keyword-oriented sub-queries. To improve performance, we propose a corpus-level test-time scaling framework that uses LLMs to augment documents with metadata and keywords, making retrieval easier for off-the-shelf retrievers. This yields 8% and 2% gains on short-form and open-ended questions, respectively.', comment='Submission to ACL ARR 2026 January', journal_ref=None, doi=None, primary_category='cs.IR', categories=['cs.IR', 'cs.CL'], links=[arxiv.Result.Link('https://arxiv.org/abs/2602.05975v1', title=None, rel='alternate', content_type=None), arxiv.Result.Link('https://arxiv.org/pdf/2602.05975v1', title='pdf', rel='related', content_type=None)])



arxiv.Result(
	entry_id='http://arxiv.org/abs/2602.05975v1', 
	updated=datetime.datetime(2026, 2, 5, 18, 25, 24, tzinfo=datetime.timezone.utc), 
	published=datetime.datetime(2026, 2, 5, 18, 25, 24, tzinfo=datetime.timezone.utc), 
	title='SAGE: Benchmarking and Improving Retrieval for Deep Research Agents', 
	authors=[arxiv.Result.Author('Tiansheng Hu'), arxiv.Result.Author('Yilun Zhao'), arxiv.Result.Author('Canyu Zhang'), arxiv.Result.Author('Arman Cohan'), arxiv.Result.Author('Chen Zhao')], 
	summary='Deep research agents have emerged as powerful systems for addressing complex queries. Meanwhile, LLM-based retrievers have demonstrated strong capability in following instructions or reasoning. This raises a critical question: can LLM-based retrievers effectively contribute to deep research agent workflows? To investigate this, we introduce SAGE, a benchmark for scientific literature retrieval comprising 1,200 queries across four scientific domains, with a 200,000 paper retrieval corpus.We evaluate six deep research agents and find that all systems struggle with reasoning-intensive retrieval. Using DR Tulu as backbone, we further compare BM25 and LLM-based retrievers (i.e., ReasonIR and gte-Qwen2-7B-instruct) as alternative search tools. Surprisingly, BM25 significantly outperforms LLM-based retrievers by approximately 30%, as existing agents generate keyword-oriented sub-queries. To improve performance, we propose a corpus-level test-time scaling framework that uses LLMs to augment documents with metadata and keywords, making retrieval easier for off-the-shelf retrievers. This yields 8% and 2% gains on short-form and open-ended questions, respectively.', 
	comment='Submission to ACL ARR 2026 January', 
	journal_ref=None, 
	doi=None, 
	primary_category='cs.IR', 
	categories=['cs.IR', 'cs.CL'], 
	links=[
     	arxiv.Result.Link('https://arxiv.org/abs/2602.05975v1', 
			title=None, 
			rel='alternate', 
			content_type=None), 
  		arxiv.Result.Link('https://arxiv.org/pdf/2602.05975v1', 
			title='pdf', 
			rel='related', 
			content_type=None)])


https://arxiv.org/src/2602.05975v1
https://export.arxiv.org/src/2602.05975v1
https://export.arxiv.org/bibtex/2602.05975v1

"""
