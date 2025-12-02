import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import warnings
warnings.filterwarnings('ignore')

# -------------------------- 1. 配置路径与样式 --------------------------
# 过滤后的数据路径（与上一步输出路径一致）
filtered_address = r"D:\zyt\git_ln\algo_agent\tests\playground\gen\g6\log\filtered_CN-addresses.tsv"
filtered_houses = r"D:\zyt\git_ln\algo_agent\tests\playground\gen\g6\log\filtered_CN-houses.tsv"
filtered_streets = r"D:\zyt\git_ln\algo_agent\tests\playground\gen\g6\log\filtered_CN-streets.tsv"

# 设置中文字体（解决中文乱码）
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.figsize'] = (12, 8)

# -------------------------- 2. 读取过滤后的数据 --------------------------
def read_tsv(path):
    """读取TSV文件，处理空值和数据类型"""
    df = pd.read_csv(path, sep="\t", dtype=str)
    df.columns = [col.strip() for col in df.columns]  # 清理列名空格
    # 经纬度转换为数值类型
    for col in ['x', 'x_min', 'x_max', 'y', 'y_min', 'y_max']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

df_addr = read_tsv(filtered_address)
df_house = read_tsv(filtered_houses)
df_street = read_tsv(filtered_streets)

# 打印数据基本信息
print("=== 过滤后数据概览 ===")
print(f"地址数据：{len(df_addr)} 条")
print(f"房屋数据：{len(df_house)} 条")
print(f"街道数据：{len(df_street)} 条")

# -------------------------- 3. 数据预处理（提取有效坐标） --------------------------
# 地址数据：取x_min/y_min作为坐标（或x_max/y_max，可根据实际调整）
addr_coords = df_addr[['x_min', 'y_min', 'street_']].dropna(subset=['x_min', 'y_min'])
# 房屋数据：直接取x/y坐标
house_coords = df_house[['x', 'y', 'street']].dropna(subset=['x', 'y'])

# 提取最大连通分量的街道（复用上一步逻辑，确保一致性）
G = nx.Graph()
address_streets = df_addr["street_"].dropna().unique()
for street in address_streets:
    G.add_node(street)
# 重建连通图
city_groups = df_addr.groupby("city_")
for city, group in city_groups:
    city_streets = group["street_"].unique()
    for i in range(len(city_streets)):
        for j in range(i + 1, len(city_streets)):
            G.add_edge(city_streets[i], city_streets[j])
largest_cc = max(nx.connected_components(G), key=len) if not nx.is_empty(G) else set()

# -------------------------- 4. 绘制核心可视化图表 --------------------------
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

# --- 子图1：所有有效坐标散点图（地址+房屋） ---
# 地址坐标（蓝色）
ax1.scatter(addr_coords['x_min'], addr_coords['y_min'], 
            c='blue', alpha=0.6, s=50, label='地址坐标', edgecolors='k', linewidth=0.5)
# 房屋坐标（红色）
ax1.scatter(house_coords['x'], house_coords['y'], 
            c='red', alpha=0.6, s=50, label='房屋坐标', edgecolors='k', linewidth=0.5)
ax1.set_title('北京市过滤后坐标分布（地址+房屋）', fontsize=12, fontweight='bold')
ax1.set_xlabel('经度', fontsize=10)
ax1.set_ylabel('纬度', fontsize=10)
ax1.legend(loc='best')
ax1.grid(alpha=0.3)

# --- 子图2：最大连通分量街道的地址分布 ---
addr_largest_cc = addr_coords[addr_coords['street_'].isin(largest_cc)]
ax2.scatter(addr_largest_cc['x_min'], addr_largest_cc['y_min'], 
            c='green', alpha=0.8, s=60, label=f'最大连通分量街道（{len(largest_cc)}条）', 
            edgecolors='k', linewidth=0.5)
ax2.set_title('最大连通分量街道的地址坐标分布', fontsize=12, fontweight='bold')
ax2.set_xlabel('经度', fontsize=10)
ax2.set_ylabel('纬度', fontsize=10)
ax2.legend(loc='best')
ax2.grid(alpha=0.3)

# --- 子图3：街道数量统计（原始vs过滤后） ---
# 统计原始数据（需读取原始文件）
df_street_origin = pd.read_csv(r"D:\zyt\git_ln\algo_agent\tests\playground\gen\g6\log\CN-streets.tsv", sep="\t")
origin_street_count = len(df_street_origin[df_street_origin['state'] == '北京市'])
filtered_street_count = len(df_street)
ax3.bar(['原始北京市街道数', '过滤后街道数'], [origin_street_count, filtered_street_count], 
        color=['orange', 'darkgreen'], alpha=0.7, width=0.6)
ax3.set_title('北京市街道数量对比', fontsize=12, fontweight='bold')
ax3.set_ylabel('数量', fontsize=10)
# 在柱子上标注数值
for i, v in enumerate([origin_street_count, filtered_street_count]):
    ax3.text(i, v + 0.5, str(v), ha='center', va='bottom', fontsize=10, fontweight='bold')
ax3.grid(alpha=0.3, axis='y')

# --- 子图4：连通分量大小分布 ---
if not nx.is_empty(G):
    # 统计所有连通分量的大小
    cc_sizes = [len(cc) for cc in nx.connected_components(G)]
    ax4.bar(range(len(cc_sizes)), sorted(cc_sizes, reverse=True), 
            color='purple', alpha=0.7, width=0.8)
    ax4.set_title('街道连通分量大小分布（降序）', fontsize=12, fontweight='bold')
    ax4.set_xlabel('连通分量序号', fontsize=10)
    ax4.set_ylabel('分量内街道数', fontsize=10)
    ax4.grid(alpha=0.3, axis='y')
else:
    ax4.text(0.5, 0.5, '无有效连通分量', ha='center', va='center', fontsize=12)
    ax4.set_title('街道连通分量大小分布', fontsize=12, fontweight='bold')

# 整体标题
fig.suptitle('北京市街道/地址/房屋数据过滤后可视化分析', fontsize=16, fontweight='bold')
plt.tight_layout()

# -------------------------- 5. 保存与显示图表 --------------------------
# 保存高清图片
plt.savefig(r"D:\zyt\git_ln\algo_agent\tests\playground\gen\g6\log\beijing_data_visualization.png", 
            dpi=300, bbox_inches='tight')
# 显示图表
plt.show()

# -------------------------- 6. 额外：绘制街道连通图（网络结构） --------------------------
if not nx.is_empty(G):
    fig2, ax5 = plt.subplots(1, 1, figsize=(10, 8))
    # 绘制网络结构图（使用spring布局）
    pos = nx.spring_layout(G, seed=42)  # seed保证布局固定
    # 最大连通分量节点标红，其他标灰
    node_colors = ['red' if node in largest_cc else 'gray' for node in G.nodes()]
    nx.draw(G, pos, ax=ax5, node_color=node_colors, node_size=500, 
            with_labels=True, font_size=8, font_weight='bold', 
            edge_color='lightgray', alpha=0.8)
    ax5.set_title('街道连通网络图（红色=最大连通分量）', fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.savefig(r"D:\zyt\git_ln\algo_agent\tests\playground\gen\g6\log\street_network.png", 
                dpi=300, bbox_inches='tight')
    plt.show()

print("\n可视化完成！")
print(f"图表保存路径：")
print(f"- 综合分析图：D:\\zyt\\git_ln\\algo_agent\\tests\\playground\\gen\\g6\\log\\beijing_data_visualization.png")
if not nx.is_empty(G):
    print(f"- 街道连通图：D:\\zyt\\git_ln\\algo_agent\\tests\\playground\\gen\\g6\\log\\street_network.png")