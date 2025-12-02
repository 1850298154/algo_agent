import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from typing import Set
import warnings
warnings.filterwarnings("ignore")  # 忽略无关警告

# -------------------------- 1. 配置文件路径 --------------------------
address_path = r"D:\zyt\git_ln\algo_agent\tests\playground\gen\g6\log\CN-addresses.tsv"
houses_path = r"D:\zyt\git_ln\algo_agent\tests\playground\gen\g6\log\CN-houses.tsv"
streets_path = r"D:\zyt\git_ln\algo_agent\tests\playground\gen\g6\log\CN-streets.tsv"

# 输出路径（过滤后的文件）
output_address = r"D:\zyt\git_ln\algo_agent\tests\playground\gen\g6\log\filtered_CN-addresses.tsv"
output_houses = r"D:\zyt\git_ln\algo_agent\tests\playground\gen\g6\log\filtered_CN-houses.tsv"
output_streets = r"D:\zyt\git_ln\algo_agent\tests\playground\gen\g6\log\filtered_CN-streets.tsv"

# -------------------------- 2. 读取数据 --------------------------
# 读取时指定分隔符为TSV，保留原始列名
df_address = pd.read_csv(address_path, sep="\t", dtype=str)
df_houses = pd.read_csv(houses_path, sep="\t", dtype=str)
df_streets = pd.read_csv(streets_path, sep="\t", dtype=str)

# 清理列名空格
df_address.columns = [col.strip() for col in df_address.columns]
df_houses.columns = [col.strip() for col in df_houses.columns]
df_streets.columns = [col.strip() for col in df_streets.columns]

# -------------------------- 3. 第一步过滤：state=北京市 --------------------------
df_streets_beijing = df_streets[df_streets["state"] == "北京市"].copy()
beijing_streets: Set[str] = set(df_streets_beijing["street_name"].dropna())

# -------------------------- 4. 匹配CN-addresses的street_在其他文件出现 --------------------------
houses_streets: Set[str] = set(df_houses["street"].dropna())
other_streets = beijing_streets.union(houses_streets)
df_address_filtered = df_address[df_address["street_"].isin(other_streets)].copy()

# -------------------------- 5. 构建街道连通图，提取最大连通分量 --------------------------
G = nx.Graph()
address_streets = df_address_filtered["street_"].dropna().unique()

# 添加节点
for street in address_streets:
    G.add_node(street)

# 添加边（同城市街道互连，可自定义规则）
city_groups = df_address_filtered.groupby("city_")
for city, group in city_groups:
    city_streets = group["street_"].unique()
    for i in range(len(city_streets)):
        for j in range(i + 1, len(city_streets)):
            G.add_edge(city_streets[i], city_streets[j])

# 提取最大连通分量
if not nx.is_empty(G):
    largest_cc = max(nx.connected_components(G), key=len)
    # 构建最大连通子图
    G_largest = G.subgraph(largest_cc).copy()
else:
    largest_cc = set()
    G_largest = nx.Graph()

# -------------------------- 6. 最终过滤三个文件 --------------------------
df_address_final = df_address_filtered[df_address_filtered["street_"].isin(largest_cc)].copy()
df_houses_final = df_houses[
    (df_houses["street"].isin(largest_cc)) &
    (df_houses["city"].str.contains("北京市", na=False))
].copy()
df_streets_final = df_streets_beijing[df_streets_beijing["street_name"].isin(largest_cc)].copy()

# 保存过滤后的文件
df_address_final.to_csv(output_address, sep="\t", index=False, na_rep="")
df_houses_final.to_csv(output_houses, sep="\t", index=False, na_rep="")
df_streets_final.to_csv(output_streets, sep="\t", index=False, na_rep="")

# -------------------------- 7. 可视化最大连通图 --------------------------
plt.rcParams["font.sans-serif"] = ["SimHei"]  # 支持中文显示
plt.rcParams["axes.unicode_minus"] = False    # 解决负号显示问题
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))  # 1行2列子图

# 子图1：连通图拓扑结构
if not nx.is_empty(G_largest):
    # 用spring布局绘制拓扑图
    pos = nx.spring_layout(G_largest, seed=42)  # seed固定布局
    nx.draw(
        G_largest, pos, ax=ax1,
        with_labels=True,  # 显示节点名称（街道名）
        node_color="#4CAF50",  # 节点颜色
        node_size=800,         # 节点大小
        font_size=8,           # 字体大小
        font_weight="bold",    # 字体加粗
        edge_color="#9E9E9E",  # 边颜色
        linewidths=1           # 节点边框宽度
    )
    ax1.set_title("北京市街道最大连通图（拓扑结构）", fontsize=14, fontweight="bold")
else:
    ax1.text(0.5, 0.5, "无连通街道数据", ha="center", va="center", fontsize=12)
    ax1.set_title("北京市街道最大连通图（拓扑结构）", fontsize=14, fontweight="bold")

# 子图2：地理坐标分布（若有坐标数据）
ax2.set_title("北京市街道地理分布", fontsize=14, fontweight="bold")
ax2.set_xlabel("经度", fontsize=12)
ax2.set_ylabel("纬度", fontsize=12)

# 绘制address的坐标（x_min/x_max为经度，y_min/y_max为纬度）
if not df_address_final.empty:
    # 转换坐标为数值类型
    df_address_final["x_min"] = pd.to_numeric(df_address_final["x_min"], errors="coerce")
    df_address_final["y_min"] = pd.to_numeric(df_address_final["y_min"], errors="coerce")
    # 过滤有效坐标
    df_geo = df_address_final.dropna(subset=["x_min", "y_min"])
    
    if not df_geo.empty:
        # 按街道分组绘制散点
        for street in largest_cc:
            df_street = df_geo[df_geo["street_"] == street]
            ax2.scatter(
                df_street["x_min"], df_street["y_min"],
                label=street, s=100, alpha=0.7, edgecolors="black"
            )
        ax2.legend(loc="upper right", fontsize=8)
        ax2.grid(True, alpha=0.3)
else:
    ax2.text(0.5, 0.5, "无有效地理坐标数据", ha="center", va="center", fontsize=12)

# 整体标题
fig.suptitle(f"北京市街道最大连通图分析（节点数：{len(largest_cc)}）", fontsize=16, fontweight="bold")
plt.tight_layout()  # 调整布局避免重叠
plt.savefig(r"D:\zyt\git_ln\algo_agent\tests\playground\gen\g6\log\beijing_streets_graph.png", 
            dpi=300, bbox_inches="tight")  # 保存图片（高清）
plt.show()

# -------------------------- 8. 输出统计信息 --------------------------
print("="*50)
print("数据过滤与可视化完成！")
print("="*50)
print(f"原始数据统计：")
print(f"- CN-addresses.tsv: {len(df_address)} 条")
print(f"- CN-houses.tsv: {len(df_houses)} 条")
print(f"- CN-streets.tsv: {len(df_streets)} 条")
print(f"\n过滤后数据统计：")
print(f"- filtered_CN-addresses.tsv: {len(df_address_final)} 条")
print(f"- filtered_CN-houses.tsv: {len(df_houses_final)} 条")
print(f"- filtered_CN-streets.tsv: {len(df_streets_final)} 条")
print(f"\n最大连通图统计：")
print(f"- 节点数（街道数）：{len(largest_cc)}")
print(f"- 边数：{G_largest.number_of_edges()}")
print(f"\n文件保存路径：")
print(f"- 过滤后文件：{output_address}")
print(f"- 可视化图片：D:\\zyt\\git_ln\\algo_agent\\tests\\playground\\gen\\g6\\log\\beijing_streets_graph.png")
print("="*50)