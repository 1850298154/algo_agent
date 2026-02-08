import arxiv
import requests
import os
import re
import time

def sanitize_filename(filename):
    """清理文件名中的非法字符"""
    return re.sub(r'[\\/*?:"<>|]', "", filename).strip()

def generate_bibtex(result):
    """根据 arXiv result 对象生成 BibTeX 字符串"""
    short_id = result.get_short_id()
    #以此格式生成引用key: AuthorYearTitleWord
    first_author_lastname = result.authors[0].name.split(' ')[-1].lower()
    year = result.published.year
    first_word_title = result.title.split(' ')[0].lower()
    cite_key = f"{first_author_lastname}{year}{first_word_title}"
    
    authors_str = " and ".join([a.name for a in result.authors])
    
    bibtex = f"""@misc{{{cite_key},
      title={{{result.title}}}, 
      author={{{authors_str}}},
      year={{{result.published.year}}},
      eprint={{{short_id}}},
      archivePrefix={{arXiv}},
      primaryClass={{{result.primary_category}}}
}}"""
    return bibtex

def download_papers(paper_titles, base_dir="Paper_Downloads"):
    """
    批量下载 PDF, LaTeX Source, BibTeX
    """
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
        
    client = arxiv.Client()

    for title in paper_titles:
        print(f"\n🔍 正在搜索: {title} ...")
        
        # 1. 搜索论文
        search = arxiv.Search(
            query=f'ti:"{title}"',
            max_results=1,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        try:
            result = next(client.results(search))
        except StopIteration:
            print(f"❌ 未找到论文: {title}")
            continue
        except Exception as e:
            print(f"❌ 搜索出错: {e}")
            continue

        # 校验：如果搜索结果标题和输入差异太大（比如搜不到匹配了别的），可以加逻辑判断
        # 这里直接信任 arXiv 的相关性排序第一名
        
        # 准备文件路径
        safe_title = sanitize_filename(result.title)
        # 截断过长的文件名防止系统报错
        if len(safe_title) > 150: 
            safe_title = safe_title[:150]
            
        paper_dir = os.path.join(base_dir, safe_title)
        if not os.path.exists(paper_dir):
            os.makedirs(paper_dir)
            
        print(f"   📂 目标文件夹: {paper_dir}")

        # ---------------------------
        # 2. 生成并保存 BibTeX
        # ---------------------------
        bib_path = os.path.join(paper_dir, "citation.bib")
        with open(bib_path, "w", encoding="utf-8") as f:
            f.write(generate_bibtex(result))
        print("   ✅ [1/3] BibTeX 已保存")

        # ---------------------------
        # 3. 下载 PDF
        # ---------------------------
        try:
            # result.download_pdf 会自动处理文件名，但我们想指定路径
            pdf_path = os.path.join(paper_dir, f"{safe_title}.pdf")
            if not os.path.exists(pdf_path):
                result.download_pdf(dirpath=paper_dir, filename=f"{safe_title}.pdf")
                print("   ✅ [2/3] PDF 已下载")
            else:
                print("   ⚠️ [2/3] PDF 已存在，跳过")
        except Exception as e:
            print(f"   ❌ PDF 下载失败: {e}")

        # ---------------------------
        # 4. 下载 LaTeX 源码 (Source)
        # ---------------------------
        # arXiv 的源码下载链接格式通常是 /e-print/{id}
        source_url = f"https://arxiv.org/e-print/{result.get_short_id()}"
        source_path = os.path.join(paper_dir, "source.tar.gz")
        
        if not os.path.exists(source_path):
            try:
                r = requests.get(source_url, stream=True)
                if r.status_code == 200:
                    # 注意：如果这篇论文没有上传 LaTeX 源码（只有PDF），这个链接下载下来的其实是 PDF
                    # 我们可以检查 Content-Type，但通常默认保存为 tar.gz
                    with open(source_path, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=1024):
                            if chunk:
                                f.write(chunk)
                    print("   ✅ [3/3] LaTeX 源码已下载 (source.tar.gz)")
                else:
                    print(f"   ❌ LaTeX 源码下载失败 (Status: {r.status_code})")
            except Exception as e:
                print(f"   ❌ LaTeX 源码请求出错: {e}")
        else:
            print("   ⚠️ [3/3] LaTeX 源码已存在，跳过")
            
        # 礼貌性延时，防止请求过快被封 IP
        time.sleep(1)

# =================使用示例=================
if __name__ == "__main__":
    # 在这里填入你想下载的论文标题列表
    papers_to_download = [
        "Attention Is All You Need",
        "Deep Residual Learning for Image Recognition",
        "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
        # "这里可以放任意不存在的论文测试报错"
    ]

    download_papers(papers_to_download, base_dir="./My_Arxiv_Papers")