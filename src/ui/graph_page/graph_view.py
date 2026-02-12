import streamlit as st


import streamlit as st
import json
from streamlit_agraph import (
    agraph,
    Node,
    Edge,
    Config,
    ConfigBuilder,
    TripleStore,
    data,
)

st.set_page_config(layout="wide")
st.title("🔬 streamlit-agraph 全功能演示")

# 内联示例数据（模拟 marvel.json 结构）
marvel_example = {
    "name": "Marvel Universe",
    "img": "https://example.com/marvel.png",
                    "link": "https://marvel.com/ironman",
    "children": [
        {
            "name": "Avengers",
            "children": [
                {
                    "hero": "Iron Man",
                    "link": "https://marvel.com/ironman",
                    "img": "https://example.com/ironman.png",
                },
                {
                    "hero": "Thor",
                    "link": "https://marvel.com/thor",
                    "img": "https://example.com/thor.png",
                },
            ],
        },
        {
            "name": "Guardians",
            "children": [
                {
                    "hero": "Star-Lord",
                    "link": "https://marvel.com/starlord",
                    "img": "https://example.com/starlord.png",
                }
            ],
        },
    ],
}

def load_from_inline(data_obj):
    nodes, edges = [], []
    root = data_obj
    nodes.append(
        Node(
            id=root["name"],
            # title=root["link"],
            # title='http://localhost:8507/cto',
            title='/cto',
            # title='cto',
        )
    )

    return nodes, edges

nodes_json, edges_json = load_from_inline(marvel_example)
config_json = Config(width=800, height=500, directed=True, physics=True)
return_json = agraph(nodes=nodes_json, edges=edges_json, config=config_json)
st.write("选中节点/边：", return_json)










# 定义CTO页面的核心逻辑
def cto_page():
    st.title("CTO 技术中心 💻")
    st.write("这是 CTO 页面内容")
    
    # 可以扩展更多CTO页面的功能（示例）
    st.divider()
    st.subheader("技术团队信息")
    st.write("- 研发人数：50人")
    st.write("- 核心技术栈：Python、Java、前端框架")
    
    st.subheader("技术规划")
    st.slider("2024年研发投入（万）", 0, 1000, 500)
    st.selectbox("重点研发方向", ["AI应用", "大数据平台", "云原生"])

import streamlit as st

# 配置页面基础信息（可选，但推荐）
st.set_page_config(
    page_title="企业导航系统",  # 浏览器标签标题
    page_icon="🏢",            # 页面图标
    layout="wide"             # 宽屏布局
)

# 主页内容
def home_page():
    st.title("企业主页 🏢")
    st.write("欢迎来到企业导航系统，选择左侧菜单访问不同页面")
    st.divider()
    st.subheader("功能说明")
    st.write("- 点击左侧的CTO选项可进入对应页面")
    st.write("- 支持扩展更多子页面（如CEO、HR等）")

# 导入子页面（从pages文件夹导入）
# from pages.cto import cto_page

# 创建页面对象
home = st.Page(home_page, title="主页", url_path="/", icon="🏠")
cto = st.Page(cto_page, title="CTO", url_path="/cto", icon="💻")

# 配置导航（会自动生成左侧侧边栏）
pg = st.navigation(
    {
        "企业导航": [home, cto]  # 分组名称 + 页面列表
    }

)

# 运行导航
pg.run()