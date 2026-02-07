
from mcp.server.fastmcp import FastMCP
import arxiv
import textwrap

# 初始化 MCP 服务
mcp = FastMCP("Paper-Downloader")

@mcp.tool()
def get_paper_resources(title: str) -> str:
    """
    根据论文标题搜索 arXiv，返回 LaTeX 源码下载链接和 BibTeX 引用。
    """
    # 1. 在 arXiv 上搜索
    client = arxiv.Client()
    search = arxiv.Search(
        query=f'ti:"{title}"', # 限制在标题中搜索，提高准确率
        max_results=1,
        sort_by=arxiv.SortCriterion.Relevance
    )

    try:
        result = next(client.results(search))
    except StopIteration:
        return f"未找到名为 '{title}' 的论文，请检查标题拼写或确认该论文是否在 arXiv 上。"

    # 2. 构建 LaTeX 源码下载链接 (arXiv 的 e-print 链接即为源码压缩包)
    # 注意：下载下来的通常是 .tar.gz 文件
    source_url = f"https://arxiv.org/e-print/{result.get_short_id()}"
    pdf_url = result.pdf_url

    # 3. 生成 BibTeX
    # arXiv API 不直接返回 BibTeX，我们需要根据元数据构建
    authors = " and ".join([a.name for a in result.authors])
    year = result.published.year
    # 取 ID 的第一部分作为引用 Key
    cite_key = f"{result.authors[0].name.split(' ')[-1].lower()}{year}{title.split(' ')[0].lower()}"
    
    bibtex = textwrap.dedent(f"""
    @misc{{{cite_key},
      title={{{result.title}}}, 
      author={{{authors}}},
      year={{{year}}},
      eprint={{{result.get_short_id()}}},
      archivePrefix={{arXiv}},
      primaryClass={{{result.primary_category}}}
    }}
    """)

    return f"""
🎉 找到论文: {result.title}

1. **LaTeX 源码下载链接**: 
   {source_url}
   *(注意: 点击链接将下载 .tar.gz 或 .pdf 文件，解压即可获得 .tex 源文件)*

2. **BibTeX**:
```bibtex
{bibtex.strip()}
```

3. **PDF 链接**:
   {pdf_url}
    """
get_paper_resources("Attention Is All You Need")
exit()

##########
import arxiv
import requests
import os

def download_paper_assets(title, output_dir="./downloads"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"🔍 正在搜索: {title}...")
    client = arxiv.Client()
    search = arxiv.Search(query=f'ti:"{title}"', max_results=1)
    
    try:
        paper = next(client.results(search))
    except StopIteration:
        print("❌ 未找到论文")
        return

    paper_id = paper.get_short_id()
    safe_title = "".join([c for c in paper.title if c.isalnum() or c in " ._-"]).strip()
    
    # 1. 生成 BibTeX
    bibtex = f"""@misc{{{paper_id},
      title={{{paper.title}}}, 
      author={{{' and '.join([a.name for a in paper.authors])}}},
      year={{{paper.published.year}}},
      eprint={{{paper_id}}},
      archivePrefix={{arXiv}},
      primaryClass={{{paper.primary_category}}}
    }}"""
    
    with open(f"{output_dir}/{safe_title}.bib", "w", encoding="utf-8") as f:
        f.write(bibtex)
    print(f"✅ BibTeX 已保存: {safe_title}.bib")

    # 2. 下载 LaTeX 源码 (Source)
    # arXiv 的 /e-print/ 接口会自动提供源码包
    download_url = f"https://arxiv.org/e-print/{paper_id}"
    print(f"⬇️ 正在下载源码包 (tar.gz)...")
    
    response = requests.get(download_url, stream=True)
    if response.status_code == 200:
        # arXiv 源码通常是 tar.gz，但也可能是 PDF（如果作者没传 TeX）
        # 我们默认保存为 tar.gz
        file_path = f"{output_dir}/{safe_title}.tar.gz"
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print(f"✅ 源码已下载: {file_path}")
    else:
        print(f"❌ 下载失败，状态码: {response.status_code}")

# 使用示例
download_paper_assets("Attention Is All You Need")