import streamlit as st
import feedparser
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import tarfile
import json
from tqdm import tqdm
import time
from urllib.parse import quote

# --------------------------
# 全局配置与工具函数
# --------------------------
# 创建必要的文件夹
os.makedirs("arxiv_downloads/latex", exist_ok=True)
os.makedirs("arxiv_downloads/bibtex", exist_ok=True)
os.makedirs("arxiv_downloads/summaries", exist_ok=True)

# arXiv API基础配置
ARXIV_API_BASE = "http://export.arxiv.org/api/query"
# 避免API调用频率过高（arXiv建议每秒不超过1次）
API_DELAY = 1.0

def clean_filename(filename):
    """清理文件名中的非法字符"""
    return "".join(c for c in filename if c not in r'<>:"/\|?*').strip()

def parse_arxiv_date(date_str):
    """解析arXiv的日期字符串为datetime对象"""
    try:
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    except:
        return None

def get_arxiv_paper_details(search_query, max_results=10):
    """
    从arXiv API获取批量论文的完整信息（榨干API能力）
    :param search_query: 搜索条件（标题/关键词/分类）
    :param max_results: 返回结果数量
    :return: 包含所有论文详细信息的列表
    """
    # 构造API请求参数（最大化提取字段）
    encoded_query = quote(search_query)
    url = f"{ARXIV_API_BASE}?search_query={encoded_query}&max_results={max_results}&sort=submittedDate&order=desc"
    
    try:
        # 避免高频调用
        time.sleep(API_DELAY)
        feed = feedparser.parse(url)
        
        if feed.bozo != 0:
            st.error(f"API请求错误: {feed.bozo_exception}")
            return []
        
        papers = []
        for entry in tqdm(feed.entries, desc="解析论文信息"):
            # 核心基础信息
            arxiv_id = entry.id.split('/')[-1] if 'id' in entry else ""
            title = entry.title.strip().replace('\n', ' ') if 'title' in entry else ""
            authors = [author.name for author in entry.authors] if 'authors' in entry else []
            abstract = entry.summary.strip() if 'summary' in entry else ""
            
            # 分类信息（arXiv核心分类体系）
            primary_category = entry.arxiv_primary_category['term'] if 'arxiv_primary_category' in entry else ""
            categories = entry.tags[0]['term'].split(',') if 'tags' in entry else []
            # 解析分类对应的学科名称（简化映射）
            category_mapping = {
                'cs': 'Computer Science', 'physics': 'Physics', 'math': 'Mathematics',
                'q-bio': 'Quantitative Biology', 'q-fin': 'Quantitative Finance',
                'stat': 'Statistics', 'econ': 'Economics', 'astro-ph': 'Astrophysics'
            }
            primary_discipline = next((v for k, v in category_mapping.items() if primary_category.startswith(k)), "Other")
            
            # 日期信息（提交/更新）
            submitted_date = parse_arxiv_date(entry.published) if 'published' in entry else None
            updated_date = parse_arxiv_date(entry.updated) if 'updated' in entry else None
            
            # 链接信息（最大化提取）
            pdf_url = next((link.href for link in entry.links if link.rel == 'alternate' and link.type == 'application/pdf'), "")
            latex_url = f"https://arxiv.org/e-print/{arxiv_id}" if arxiv_id else ""
            bibtex_url = f"{ARXIV_API_BASE}?search_query=id:{arxiv_id}&max_results=1&format=bibtex"
            
            # 附加信息
            comment = entry.comment.strip() if 'comment' in entry else ""
            journal_ref = entry.journal_ref.strip() if 'journal_ref' in entry else ""
            doi = entry.doi if 'doi' in entry else ""
            license = entry.rights if 'rights' in entry else ""
            
            # 获取BibTeX内容
            bibtex_content = ""
            if bibtex_url:
                try:
                    time.sleep(API_DELAY)
                    bibtex_resp = requests.get(bibtex_url, timeout=10)
                    if bibtex_resp.status_code == 200:
                        bibtex_content = bibtex_resp.text
                except Exception as e:
                    st.warning(f"获取{arxiv_id}的BibTeX失败: {str(e)}")
            
            # 构建论文信息字典
            paper = {
                'arxiv_id': arxiv_id,
                'title': title,
                'authors': ', '.join(authors),
                'author_count': len(authors),
                'primary_category': primary_category,
                'primary_discipline': primary_discipline,
                'all_categories': ', '.join(categories),
                'submitted_date': submitted_date,
                'updated_date': updated_date,
                'abstract': abstract,
                'pdf_url': pdf_url,
                'latex_url': latex_url,
                'bibtex_content': bibtex_content,
                'comment': comment,
                'journal_ref': journal_ref,
                'doi': doi,
                'license': license,
                'latex_download_status': 'pending',
                'bibtex_save_status': 'pending'
            }
            papers.append(paper)
        
        return papers
    
    except Exception as e:
        st.error(f"获取论文信息失败: {str(e)}")
        return []

def download_latex_batch(papers):
    """批量下载LaTeX源码（tar.gz格式）"""
    for paper in tqdm(papers, desc="下载LaTeX源码"):
        arxiv_id = paper['arxiv_id']
        title = clean_filename(paper['title'][:50])  # 截断长标题
        latex_url = paper['latex_url']
        
        if not latex_url or not arxiv_id:
            paper['latex_download_status'] = 'failed (no URL)'
            continue
        
        try:
            time.sleep(API_DELAY)
            response = requests.get(latex_url, timeout=30, stream=True)
            if response.status_code == 200:
                # 保存tar.gz文件
                file_path = f"arxiv_downloads/latex/{arxiv_id}_{title}.tar.gz"
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                # 可选：解压文件（如需直接获取.tex文件）
                # with tarfile.open(file_path, 'r:gz') as tar:
                #     tar.extractall(f"arxiv_downloads/latex/{arxiv_id}_{title}")
                paper['latex_download_status'] = 'success'
            else:
                paper['latex_download_status'] = f"failed (status: {response.status_code})"
        except Exception as e:
            paper['latex_download_status'] = f"failed: {str(e)[:50]}"
    
    return papers

def save_bibtex_batch(papers):
    """批量保存BibTeX文件"""
    for paper in tqdm(papers, desc="保存BibTeX"):
        arxiv_id = paper['arxiv_id']
        title = clean_filename(paper['title'][:50])
        bibtex_content = paper['bibtex_content']
        
        if not bibtex_content or not arxiv_id:
            paper['bibtex_save_status'] = 'failed (no content)'
            continue
        
        try:
            # 保存单个BibTeX文件
            file_path = f"arxiv_downloads/bibtex/{arxiv_id}_{title}.bib"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(bibtex_content)
            paper['bibtex_save_status'] = 'success'
        except Exception as e:
            paper['bibtex_save_status'] = f"failed: {str(e)[:50]}"
    
    # 生成汇总BibTeX文件
    all_bibtex = "\n\n".join([p['bibtex_content'] for p in papers if p['bibtex_content']])
    summary_bib_path = f"arxiv_downloads/bibtex/all_papers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.bib"
    with open(summary_bib_path, 'w', encoding='utf-8') as f:
        f.write(all_bibtex)
    
    return papers

def generate_summary_stats(papers_df):
    """生成统计分析结果"""
    stats = {}
    
    # 1. 基础统计
    stats['total_papers'] = len(papers_df)
    stats['success_latex'] = len(papers_df[papers_df['latex_download_status'] == 'success'])
    stats['success_bibtex'] = len(papers_df[papers_df['bibtex_save_status'] == 'success'])
    stats['avg_authors'] = papers_df['author_count'].mean()
    
    # 2. 分类分布
    category_counts = papers_df['primary_discipline'].value_counts()
    stats['category_distribution'] = category_counts
    
    # 3. 时间分布（按月）
    papers_df['submitted_month'] = papers_df['submitted_date'].dt.to_period('M')
    monthly_counts = papers_df['submitted_month'].value_counts().sort_index()
    stats['monthly_submissions'] = monthly_counts
    
    return stats

# --------------------------
# Streamlit界面构建
# --------------------------
def main():
    st.set_page_config(
        page_title="arXiv批量下载与分析工具",
        page_icon="📚",
        layout="wide"
    )
    
    st.title("📚 arXiv批量论文处理工具")
    st.subheader("最大化利用arXiv API - 批量下载LaTeX/BibTeX + 全维度信息分析")
    
    # 侧边栏：参数配置
    with st.sidebar:
        st.header("🔧 搜索配置")
        search_type = st.radio("搜索类型", ["按标题批量搜索", "按关键词/分类搜索"])
        
        if search_type == "按标题批量搜索":
            paper_titles = st.text_area(
                "输入论文标题（每行一个）",
                placeholder="Attention Is All You Need\nLanguage Models are Few-Shot Learners"
            )
            search_query = " OR ".join([f"title:{quote(title.strip())}" for title in paper_titles.split('\n') if title.strip()])
        else:
            search_keywords = st.text_input(
                "输入关键词/分类（如cs.AI, transformer）",
                value="cs.AI"
            )
            search_query = search_keywords
        
        max_results = st.slider("最大结果数量", 1, 50, 10)
        
        st.divider()
        st.header("📥 下载配置")
        auto_download_latex = st.checkbox("自动下载LaTeX源码", value=True)
        auto_save_bibtex = st.checkbox("自动保存BibTeX文件", value=True)
        
        st.divider()
        st.info(
            "📝 注意事项：\n"
            "1. arXiv API限制每秒1次调用，请耐心等待\n"
            "2. LaTeX文件保存至arxiv_downloads/latex\n"
            "3. BibTeX文件保存至arxiv_downloads/bibtex\n"
            "4. 仅开源论文提供LaTeX源码"
        )
    
    # 主界面：操作区
    col1, col2, col3 = st.columns(3)
    with col1:
        get_papers_btn = st.button("🚀 获取论文信息", type="primary")
    with col2:
        export_excel_btn = st.button("📤 导出汇总表格")
    with col3:
        export_stats_btn = st.button("📊 导出统计报告")
    
    # 核心逻辑执行
    if get_papers_btn and search_query:
        with st.spinner("正在调用arXiv API获取论文信息..."):
            # 1. 获取论文详细信息
            papers = get_arxiv_paper_details(search_query, max_results)
            
            if not papers:
                st.warning("未找到匹配的论文，请检查搜索条件")
                return
            
            # 2. 批量下载/保存
            if auto_download_latex:
                with st.spinner("批量下载LaTeX源码..."):
                    papers = download_latex_batch(papers)
            
            if auto_save_bibtex:
                with st.spinner("批量保存BibTeX文件..."):
                    papers = save_bibtex_batch(papers)
            
            # 3. 转换为DataFrame便于展示和分析
            papers_df = pd.DataFrame(papers)
            # 处理日期格式（便于展示）
            papers_df['submitted_date'] = papers_df['submitted_date'].dt.strftime('%Y-%m-%d %H:%M')
            papers_df['updated_date'] = papers_df['updated_date'].dt.strftime('%Y-%m-%d %H:%M')
            
            # 4. 缓存数据
            st.session_state['papers_df'] = papers_df
            
            # 5. 生成统计信息
            stats = generate_summary_stats(papers_df)
            st.session_state['stats'] = stats
            
            st.success(f"✅ 成功获取 {len(papers_df)} 篇论文信息！")
    
    # 展示区
    if 'papers_df' in st.session_state:
        papers_df = st.session_state['papers_df']
        stats = st.session_state.get('stats', {})
        
        # 第一部分：核心统计卡片
        st.subheader("📈 核心统计")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("总论文数", stats.get('total_papers', 0))
        with col2:
            st.metric("LaTeX下载成功", stats.get('success_latex', 0))
        with col3:
            st.metric("BibTeX保存成功", stats.get('success_bibtex', 0))
        with col4:
            st.metric("平均作者数", f"{stats.get('avg_authors', 0):.1f}")
        
        # 第二部分：论文信息表格
        st.subheader("📋 论文详细信息")
        # 选择展示的列（避免表格过宽）
        display_columns = [
            'arxiv_id', 'title', 'primary_discipline', 'authors', 
            'submitted_date', 'latex_download_status', 'bibtex_save_status'
        ]
        st.dataframe(
            papers_df[display_columns],
            use_container_width=True,
            hide_index=True,
            column_config={
                "arxiv_id": st.column_config.TextColumn("arXiv ID", width="small"),
                "title": st.column_config.TextColumn("标题", width="large"),
                "primary_discipline": st.column_config.TextColumn("主学科", width="medium"),
                "authors": st.column_config.TextColumn("作者", width="large"),
                "submitted_date": st.column_config.TextColumn("提交日期", width="medium"),
                "latex_download_status": st.column_config.TextColumn("LaTeX状态", width="small"),
                "bibtex_save_status": st.column_config.TextColumn("BibTeX状态", width="small")
            }
        )
        
        # 第三部分：统计可视化
        st.subheader("📊 统计分析")
        tab1, tab2, tab3 = st.tabs(["学科分布", "月度提交", "作者数量分布"])
        
        with tab1:
            if 'category_distribution' in stats:
                fig = px.pie(
                    values=stats['category_distribution'].values,
                    names=stats['category_distribution'].index,
                    title="论文主学科分布",
                    hole=0.3
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            if 'monthly_submissions' in stats:
                fig = px.bar(
                    x=stats['monthly_submissions'].index.astype(str),
                    y=stats['monthly_submissions'].values,
                    title="月度提交数量",
                    labels={"x": "月份", "y": "论文数量"}
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            fig = px.histogram(
                papers_df,
                x="author_count",
                title="作者数量分布",
                labels={"author_count": "作者数量", "count": "论文数"}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # 第四部分：详细信息展开
        st.subheader("🔍 单篇论文详情")
        selected_arxiv_id = st.selectbox(
            "选择论文ID查看详情",
            papers_df['arxiv_id'].tolist()
        )
        selected_paper = papers_df[papers_df['arxiv_id'] == selected_arxiv_id].iloc[0]
        
        with st.expander(f"📄 {selected_paper['title']}", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**arXiv ID**: {selected_paper['arxiv_id']}")
                st.write(f"**主分类**: {selected_paper['primary_category']}")
                st.write(f"**主学科**: {selected_paper['primary_discipline']}")
                st.write(f"**所有分类**: {selected_paper['all_categories']}")
                st.write(f"**提交日期**: {selected_paper['submitted_date']}")
                st.write(f"**更新日期**: {selected_paper['updated_date']}")
                st.write(f"**作者数**: {selected_paper['author_count']}")
                st.write(f"**DOI**: {selected_paper['doi']}")
                st.write(f"**期刊引用**: {selected_paper['journal_ref']}")
                
                # 链接按钮
                st.markdown(f"[📄 PDF链接]({selected_paper['pdf_url']})")
                st.markdown(f"[📥 LaTeX下载]({selected_paper['latex_url']})")
            
            with col2:
                st.write("**摘要**:")
                st.write(selected_paper['abstract'][:500] + "..." if len(selected_paper['abstract']) > 500 else selected_paper['abstract'])
                
                st.write("**BibTeX**:")
                st.code(selected_paper['bibtex_content'], language='bibtex')
        
        # 导出功能
        if export_excel_btn:
            # 导出完整数据到Excel
            excel_path = f"arxiv_downloads/summaries/papers_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            papers_df.to_excel(excel_path, index=False)
            st.success(f"✅ 汇总表格已导出至: {excel_path}")
        
        if export_stats_btn:
            # 导出统计报告
            stats_report = {
                "生成时间": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "搜索条件": search_query,
                "核心统计": stats,
                "下载路径": {
                    "latex": "./arxiv_downloads/latex",
                    "bibtex": "./arxiv_downloads/bibtex"
                }
            }
            stats_path = f"arxiv_downloads/summaries/stats_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(stats_path, 'w', encoding='utf-8') as f:
                json.dump(stats_report, f, ensure_ascii=False, indent=4)
            st.success(f"✅ 统计报告已导出至: {stats_path}")

if __name__ == "__main__":
    main()