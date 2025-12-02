import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")  # 忽略无关警告

# -------------------------- 1. 配置路径 --------------------------
# 过滤后的文件路径（与上一步输出路径一致）
filtered_address = r"D:\zyt\git_ln\algo_agent\tests\playground\gen\g6\log\filtered_CN-addresses.tsv"
filtered_houses = r"D:\zyt\git_ln\algo_agent\tests\playground\gen\g6\log\filtered_CN-houses.tsv"
filtered_streets = r"D:\zyt\git_ln\algo_agent\tests\playground\gen\g6\log\filtered_CN-streets.tsv"

# -------------------------- 2. 读取过滤后的数据 --------------------------
# 读取TSV文件，保留原始格式
df_address = pd.read_csv(filtered_address, sep="\t", dtype=str)
df_houses = pd.read_csv(filtered_houses, sep="\t", dtype=str)
df_streets = pd.read_csv(filtered_streets, sep="\t", dtype=str)

# 清理列名空格
df_address.columns = [col.strip() for col in df_address.columns]
df_houses.columns = [col.strip() for col in df_houses.columns]
df_streets.columns = [col.strip() for col in df_streets.columns]

# 处理空值和坐标类型转换（x/y转为数值型）
df_address["x_min"] = pd.to_numeric(df_address["x_min"], errors="coerce")
df_address["y_min"] = pd.to_numeric(df_address["y_min"], errors="coerce")
df_houses["x"] = pd.to_numeric(df_houses["x"], errors="coerce")
df_houses["y"] = pd.to_numeric(df_houses["y"], errors="coerce")

# -------------------------- 3. 重构最大连通图 --------------------------
# 提取所有有效街道名称
address_streets = df_address["street_"].dropna().unique()
houses_streets = df_houses["street"].dropna().unique()
streets_streets = df_streets["street_name"].dropna().unique()
all_valid_streets = list(set(address_streets) | set(houses_streets) | set(streets_streets))

# 构建连通图（沿用之前的规则：同城市街道互连通）
G = nx.Graph()
G.add_nodes_from(all_valid_streets)

# 添加边：同城市的街道互相连接
city_groups = df_address.groupby("city_")
for city, group in city_groups:
    city_streets = group["street_"].unique()
    for i in range(len(city_streets)):
        for j in range(i + 1, len(city_streets)):
            G.add_edge(city_streets[i], city_streets[j])

# 提取最大连通分量
if not nx.is_empty(G):
    largest_cc = max(nx.connected_components(G), key=len)
    G_largest = G.subgraph(largest_cc).copy()
else:
    print("无有效连通图数据！")
    exit()

# -------------------------- 4. 可视化最大连通图 --------------------------
plt.rcParams["font.sans-serif"] = ["SimHei"]  # 支持中文显示
plt.rcParams["axes.unicode_minus"] = False    # 解决负号显示问题

# 创建画布：分两个子图（拓扑结构 + 地理分布）
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# ===== 子图1：连通图拓扑结构 =====
# 生成布局（spring_layout更美观）
pos = nx.spring_layout(G_largest, seed=42)  # seed固定布局，便于复现

# 绘制节点和边
nx.draw_networkx_edges(G_largest, pos, ax=ax1, edge_color="#6699CC", alpha=0.7, width=1.5)
nx.draw_networkx_nodes(G_largest, pos, ax=ax1, node_color="#FF6B6B", node_size=800, alpha=0.8)

# 绘制节点标签（街道名称）
nx.draw_networkx_labels(G_largest, pos, ax=ax1, font_size=9, font_weight="bold")

ax1.set_title("北京市街道最大连通图（拓扑结构）", fontsize=14, fontweight="bold", pad=20)
ax1.axis("off")  # 隐藏坐标轴

# ===== 子图2：地理坐标分布（基于x/y） =====
# 提取街道对应的坐标（取address的x_min/y_min作为代表）
street_coords = {}
for street in largest_cc:
    street_data = df_address[df_address["street_"] == street]
    if not street_data.empty:
        x = street_data["x_min"].mean()  # 取平均坐标
        y = street_data["y_min"].mean()
        if not pd.isna(x) and not pd.isna(y):
            street_coords[street] = (x, y)

# 若有坐标数据则绘制地理分布
if street_coords:
    # 绘制地理节点
    geo_pos = street_coords
    nx.draw_networkx_edges(G_largest, geo_pos, ax=ax2, edge_color="#6699CC", alpha=0.7, width=1.5)
    nx.draw_networkx_nodes(G_largest, geo_pos, ax=ax2, node_color="#4ECDC4", node_size=800, alpha=0.8)
    nx.draw_networkx_labels(G_largest, geo_pos, ax=ax2, font_size=9, font_weight="bold")
    
    ax2.set_xlabel("经度 (X)", fontsize=12)
    ax2.set_ylabel("纬度 (Y)", fontsize=12)
    ax2.set_title("北京市街道最大连通图（地理分布）", fontsize=14, fontweight="bold", pad=20)
    ax2.grid(True, alpha=0.3)
else:
    ax2.text(0.5, 0.5, "无有效坐标数据", ha="center", va="center", fontsize=16, transform=ax2.transAxes)
    ax2.set_title("北京市街道最大连通图（地理分布）", fontsize=14, fontweight="bold", pad=20)

# 整体标题
fig.suptitle(f"北京市街道最大连通图分析（节点数：{len(G_largest.nodes)} | 边数：{len(G_largest.edges)}）", 
             fontsize=16, fontweight="bold", y=0.98)

# 调整布局，避免标签重叠
plt.tight_layout()

# 保存图片（可选）
plt.savefig(r"D:\zyt\git_ln\algo_agent\tests\playground\gen\g6\log\beijing_streets_connected_graph.png", 
            dpi=300, bbox_inches="tight")

# 显示图形
plt.show()

# -------------------------- 5. 输出连通图统计信息 --------------------------
print("="*50)
print("最大连通图统计信息：")
print(f"- 街道节点数：{len(G_largest.nodes)}")
print(f"- 连通边数：{len(G_largest.edges)}")
print(f"- 街道列表：{list(G_largest.nodes)}")
print("="*50)