import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from typing import Set

# 设置中文字体（避免中文乱码）
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# -------------------------- 1. 配置文件路径 --------------------------
address_path = r"D:\zyt\git_ln\algo_agent\tests\playground\gen\g6\log\CN-addresses.tsv"
houses_path = r"D:\zyt\git_ln\algo_agent\tests\playground\gen\g6\log\CN-houses.tsv"
streets_path = r"D:\zyt\git_ln\algo_agent\tests\playground\gen\g6\log\CN-streets.tsv"

# 输出路径（过滤后的文件）
output_address = r"D:\zyt\git_ln\algo_agent\tests\playground\gen\g6\log\filtered_CN-addresses.tsv"
output_houses = r"D:\zyt\git_ln\algo_agent\tests\playground\gen\g6\log\filtered_CN-houses.tsv"
output_streets = r"D:\zyt\git_ln\algo_agent\tests\playground\gen\g6\log\filtered_CN-streets.tsv"

# -------------------------- 2. 读取数据 --------------------------
# 读取时指定分隔符为TSV，保留原始列名（处理中英文混合列名）
df_address = pd.read_csv(address_path, sep="\t", dtype=str)
df_houses = pd.read_csv(houses_path, sep="\t", dtype=str)
df_streets = pd.read_csv(streets_path, sep="\t", dtype=str)

# 清理列名空格（避免列名不一致）
df_address.columns = [col.strip() for col in df_address.columns]
df_houses.columns = [col.strip() for col in df_houses.columns]
df_streets.columns = [col.strip() for col in df_streets.columns]

# -------------------------- 3. 第一步过滤：state=北京市 --------------------------
# 筛选streets文件中state为"北京市"的记录
df_streets_beijing = df_streets[df_streets["state"] == "北京市"].copy()

# 获取北京市的街道名称集合（去重）
beijing_streets: Set[str] = set(df_streets_beijing["street_name"].dropna())

# -------------------------- 4. 匹配CN-addresses的street_在其他文件出现 --------------------------
# 提取houses文件中的街道名称集合
houses_streets: Set[str] = set(df_houses["street"].dropna())

# 合并streets和houses的街道名称（其他文件的街道集合）
other_streets = beijing_streets.union(houses_streets)

# 筛选address中street_在其他文件出现且属于北京市的记录
df_address_filtered = df_address[
    df_address["street_"].isin(other_streets)
].copy()

# -------------------------- 5. 构建街道连通图，提取最大连通分量 --------------------------
# 构建街道连通图（假设：同一city下的street_互为连通）
# 可根据实际业务逻辑调整连通规则（如postal_code相同/坐标相邻等）
G = nx.Graph()

# 为过滤后的address中的街道添加节点和边
address_streets = df_address_filtered["street_"].dropna().unique()
for street in address_streets:
    G.add_node(street)

# 添加边（示例：同一city下的街道互相连接）
city_groups = df_address_filtered.groupby("city_")
for city, group in city_groups:
    city_streets = group["street_"].unique()
    # 为同城市的街道构建完全图（互相连通）
    for i in range(len(city_streets)):
        for j in range(i + 1, len(city_streets)):
            G.add_edge(city_streets[i], city_streets[j])

# 提取最大连通分量的街道
if not nx.is_empty(G):
    largest_cc = max(nx.connected_components(G), key=len)
else:
    largest_cc = set()

# -------------------------- 6. 最终过滤三个文件 --------------------------
# 过滤address：仅保留最大连通分量的街道
df_address_final = df_address_filtered[
    df_address_filtered["street_"].isin(largest_cc)
].copy()

# 过滤houses：仅保留最大连通分量的街道 + 北京市
df_houses_final = df_houses[
    (df_houses["street"].isin(largest_cc)) &
    (df_houses["city"].str.contains("北京市", na=False))
].copy()

# 过滤streets：仅保留最大连通分量的街道 + 北京市
df_streets_final = df_streets_beijing[
    df_streets_beijing["street_name"].isin(largest_cc)
].copy()

# -------------------------- 7. 保存过滤后的文件 --------------------------
df_address_final.to_csv(output_address, sep="\t", index=False, na_rep="")
df_houses_final.to_csv(output_houses, sep="\t", index=False, na_rep="")
df_streets_final.to_csv(output_streets, sep="\t", index=False, na_rep="")

# -------------------------- 8. 地图可视化 --------------------------
def prepare_coordinate_data():
    """准备坐标数据，合并address和houses的坐标信息"""
    # 处理address的坐标（取x_min/y_min作为代表坐标）
    df_addr_coords = df_address_final.copy()
    # 转换坐标为数值类型
    for col in ['x_min', 'y_min', 'x_max', 'y_max']:
        df_addr_coords[col] = pd.to_numeric(df_addr_coords[col], errors='coerce')
    
    # 计算中心点坐标
    df_addr_coords['x'] = (df_addr_coords['x_min'] + df_addr_coords['x_max']) / 2
    df_addr_coords['y'] = (df_addr_coords['y_min'] + df_addr_coords['y_max']) / 2
    
    # 处理houses的坐标
    df_house_coords = df_houses_final.copy()
    df_house_coords['x'] = pd.to_numeric(df_house_coords['x'], errors='coerce')
    df_house_coords['y'] = pd.to_numeric(df_house_coords['y'], errors='coerce')
    
    # 合并坐标数据，添加类型标识
    df_addr_coords['type'] = 'address'
    df_house_coords['type'] = 'house'
    
    # 选择需要的列并统一列名
    addr_cols = ['street_', 'x', 'y', 'type', 'city_']
    house_cols = ['street', 'x', 'y', 'type', 'city']
    
    df_addr_sel = df_addr_coords[addr_cols].rename(columns={'street_': 'street', 'city_': 'city'})
    df_house_sel = df_house_coords[house_cols]
    
    # 合并所有坐标数据
    df_all_coords = pd.concat([df_addr_sel, df_house_sel], ignore_index=True)
    # 去除空坐标
    df_all_coords = df_all_coords.dropna(subset=['x', 'y'])
    
    return df_all_coords

# 准备坐标数据
df_coords = prepare_coordinate_data()

# 创建可视化图形
fig, ax = plt.subplots(figsize=(15, 12))

# -------------------------- 8.1 绘制街道连通边 --------------------------
# 构建带坐标的街道图
if len(df_coords) > 0:
    # 按街道分组，计算每个街道的中心坐标
    street_centers = df_coords.groupby('street').agg({
        'x': 'mean',
        'y': 'mean'
    }).reset_index()
    
    # 创建街道坐标映射
    street_to_coords = dict(zip(street_centers['street'], 
                               zip(street_centers['x'], street_centers['y'])))
    
    # 绘制连通边
    for u, v in G.edges():
        if u in street_to_coords and v in street_to_coords:
            x1, y1 = street_to_coords[u]
            x2, y2 = street_to_coords[v]
            # 绘制边，使用浅灰色，透明度0.5
            ax.plot([x1, x2], [y1, y2], 'gray', alpha=0.5, linewidth=1, zorder=1)

# -------------------------- 8.2 绘制坐标点 --------------------------
# 绘制address点（蓝色）
addr_points = df_coords[df_coords['type'] == 'address']
if len(addr_points) > 0:
    ax.scatter(addr_points['x'], addr_points['y'], 
               c='blue', s=100, alpha=0.7, label='Address', zorder=2)

# 绘制house点（红色）
house_points = df_coords[df_coords['type'] == 'house']
if len(house_points) > 0:
    ax.scatter(house_points['x'], house_points['y'], 
               c='red', s=80, alpha=0.7, label='House', zorder=2)

# -------------------------- 8.3 添加名称标注 --------------------------
# 为每个点添加街道名称标注
for idx, row in df_coords.iterrows():
    ax.annotate(
        row['street'],  # 标注文本（街道名称）
        (row['x'], row['y']),  # 标注位置
        xytext=(5, 5),  # 文本偏移
        textcoords='offset points',
        fontsize=8,
        alpha=0.8,
        bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='gray', alpha=0.5),
        zorder=3
    )

# -------------------------- 8.4 图表美化 --------------------------
ax.set_xlabel('经度 (X)', fontsize=12)
ax.set_ylabel('纬度 (Y)', fontsize=12)
ax.set_title('北京市街道连通图与地址分布', fontsize=16, fontweight='bold')
ax.legend(loc='best', fontsize=10)
ax.grid(True, alpha=0.3)

# 设置坐标轴范围（自动适配，留出边距）
if len(df_coords) > 0:
    x_margin = (df_coords['x'].max() - df_coords['x'].min()) * 0.1
    y_margin = (df_coords['y'].max() - df_coords['y'].min()) * 0.1
    ax.set_xlim(df_coords['x'].min() - x_margin, df_coords['x'].max() + x_margin)
    ax.set_ylim(df_coords['y'].min() - y_margin, df_coords['y'].max() + y_margin)

# 调整布局
plt.tight_layout()

# 保存图片（可选）
plt.savefig(r"D:\zyt\git_ln\algo_agent\tests\playground\gen\g6\log\beijing_streets_map.png", 
            dpi=300, bbox_inches='tight')

# 显示图表
plt.show()

# -------------------------- 9. 输出统计信息 --------------------------
print(f"过滤完成！")
print(f"- 原始address记录数：{len(df_address)} → 过滤后：{len(df_address_final)}")
print(f"- 原始houses记录数：{len(df_houses)} → 过滤后：{len(df_houses_final)}")
print(f"- 原始streets记录数：{len(df_streets)} → 过滤后：{len(df_streets_final)}")
print(f"- 最大连通分量街道数：{len(largest_cc)}")
print(f"- 可视化坐标点数：{len(df_coords)}")
print(f"文件保存路径：")
print(f"- {output_address}")
print(f"- {output_houses}")
print(f"- {output_streets}")
print(f"- 可视化图片：D:\\zyt\\git_ln\\algo_agent\\tests\\playground\\gen\\g6\\log\\beijing_streets_map.png")
