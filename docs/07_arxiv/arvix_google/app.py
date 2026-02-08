import streamlit as st
import arxiv
import pandas as pd
import os
import re
import glob
import plotly.express as px
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# ================= 全局配置 =================
DOWNLOAD_DIR = "Paper_Library"

# 预定义的查询语句列表 (这里只放一部分示例，实际请把所有列表放进来)
PREDEFINED_QUERIES = {
    "核心主题": [
        'ti:"multi-agent path planning" AND ti:"deadlock resolution"',
        'abs:"distributed multi-agent" AND abs:"deadlock breaking"',
    ],
    "LLM与AI Agent": [
        'all:"Large Language Model" AND all:"multi-agent path planning"',
        'ti:"LLM" AND ti:"task allocation" AND ti:"robot"',
    ],
    "运筹优化": [
        'ti:"column generation" AND ti:"vehicle routing" AND ti:"UAV"',
        'all:"mixed integer linear programming" AND all:"heterogeneous UAV"',
    ],
    # ... 你可以在这里添加更多分类
}

# 展平查询用于下拉菜单
FLAT_QUERIES = []
for category, q_list in PREDEFINED_QUERIES.items():
    for q in q_list:
        FLAT_QUERIES.append(f"[{category}] {q}")

# ================= 功能函数 =================

def parse_bib_file(bib_path):
    """简单的 BibTeX 解析器"""
    with open(bib_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    data = {}
    # 提取 title
    title_match = re.search(r'title=\{(.*?)\}', content, re.DOTALL)
    data['title'] = title_match.group(1) if title_match else "Unknown Title"
    
    # 提取 year
    year_match = re.search(r'year=\{(.*?)\}', content)
    data['year'] = int(year_match.group(1)) if year_match else 0
    
    # 提取 authors
    author_match = re.search(r'author=\{(.*?)\}', content)
    if author_match:
        data['authors'] = [a.strip() for a in author_match.group(1).split(' and ')]
        data['primary_author'] = data['authors'][0]
    else:
        data['authors'] = []
        data['primary_author'] = "Unknown"
        
    # 提取 primaryClass
    class_match = re.search(r'primaryClass=\{(.*?)\}', content)
    data['category'] = class_match.group(1) if class_match else "Uncategorized"
    
    return data

def load_local_library():
    """扫描本地下载目录"""
    papers = []
    if not os.path.exists(DOWNLOAD_DIR):
        return pd.DataFrame()
        
    # 遍历所有 citation.bib
    bib_files = glob.glob(os.path.join(DOWNLOAD_DIR, "*", "citation.bib"))
    
    for bib in bib_files:
        try:
            meta = parse_bib_file(bib)
            meta['path'] = os.path.dirname(bib) # 文件夹路径
            papers.append(meta)
        except Exception as e:
            continue
            
    return pd.DataFrame(papers)

# ================= Streamlit UI =================

st.set_page_config(page_title="ArXiv Paper Manager", layout="wide")

st.title("📚 ArXiv Multi-Agent & UAV Research Hub")

tab1, tab2 = st.tabs(["🔍 Search Explorer", "📊 Local Library Analytics"])

# ---------- TAB 1: 实时搜索 ----------
with tab1:
    st.markdown("### 选择查询语句进行实时检索")
    
    # 选择框
    selected_query_raw = st.selectbox("选择预定义查询:", FLAT_QUERIES)
    
    # 提取实际的 query 字符串 (去掉 [Category] 前缀)
    query_str = selected_query_raw.split("] ", 1)[1] if "] " in selected_query_raw else selected_query_raw
    
    # 允许用户修改
    user_query = st.text_input("编辑查询语句 (支持 arXiv 语法):", value=query_str)
    
    max_res = st.slider("最大返回数量", 5, 50, 10)
    
    if st.button("开始搜索 (Search arXiv)", type="primary"):
        st.info(f"正在搜索: `{user_query}` ...")
        
        client = arxiv.Client()
        search = arxiv.Search(
            query=user_query,
            max_results=max_res,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        results = list(client.results(search))
        
        st.success(f"找到 {len(results)} 篇相关论文")
        
        for p in results:
            with st.expander(f"{p.title} ({p.published.year})"):
                st.markdown(f"**Authors:** {', '.join([a.name for a in p.authors])}")
                st.markdown(f"**Category:** `{p.primary_category}` | **Published:** {p.published.date()}")
                st.markdown(f"**Abstract:**")
                st.caption(p.summary)
                st.markdown(f"[PDF Link]({p.pdf_url}) | [ArXiv Page]({p.entry_id})")

# ---------- TAB 2: 本地库分析 ----------
with tab2:
    st.markdown(f"### 本地库分析 (目录: `{DOWNLOAD_DIR}`) mac/linux path")
    
    df = load_local_library()
    
    if df.empty:
        st.warning("⚠️ 本地尚未下载任何论文，或者路径不正确。请先运行下载脚本。")
    else:
        st.markdown(f"**总计下载论文:** `{len(df)}` 篇")
        
        # 1. 侧边栏过滤器
        st.sidebar.header("Filter Options")
        
        # 年份过滤
        min_year, max_year = int(df['year'].min()), int(df['year'].max())
        years = st.sidebar.slider("选择年份范围", min_year, max_year, (min_year, max_year))
        
        # 学科过滤
        all_cats = df['category'].unique()
        selected_cats = st.sidebar.multiselect("选择学科分类", all_cats, default=all_cats)
        
        # 应用过滤
        mask = (df['year'].between(years[0], years[1])) & (df['category'].isin(selected_cats))
        filtered_df = df[mask]
        
        st.divider()
        
        # 2. 图表展示区
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📅 论文年份分布")
            year_counts = filtered_df['year'].value_counts().sort_index()
            fig_year = px.bar(year_counts, x=year_counts.index, y=year_counts.values, labels={'x':'Year', 'y':'Count'})
            st.plotly_chart(fig_year, use_container_width=True)
            
        with col2:
            st.subheader("🏷️ 学科分类分布")
            cat_counts = filtered_df['category'].value_counts()
            fig_cat = px.pie(values=cat_counts.values, names=cat_counts.index, hole=0.4)
            st.plotly_chart(fig_cat, use_container_width=True)
            
        # 3. 作者分析 (Word Cloud)
        st.subheader("☁️ 作者影响力词云")
        all_authors = [author for authors_list in filtered_df['authors'] for author in authors_list]
        if all_authors:
            author_text = " ".join([a.replace(" ", "_") for a in all_authors]) # 将姓名连起来防止被拆分
            wordcloud = WordCloud(width=800, height=300, background_color='white').generate(author_text)
            
            fig, ax = plt.subplots()
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig)
            
        # 4. 论文列表展示
        st.subheader("📄 详细列表")
        st.dataframe(
            filtered_df[['year', 'title', 'primary_author', 'category']],
            use_container_width=True,
            hide_index=True
        )