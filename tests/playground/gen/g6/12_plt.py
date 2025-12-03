import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import warnings
warnings.filterwarnings('ignore')

# -------------------------- 1. 配置路径 & 全局样式 --------------------------
# 过滤后的文件路径（与前序代码输出路径一致）
filtered_address = r"D:\zyt\git_ln\algo_agent\tests\playground\gen\g6\log\filtered_CN-addresses.tsv"
filtered_houses = r"D:\zyt\git_ln\algo_agent\tests\playground\gen\g6\log\filtered_CN-houses.tsv"
filtered_streets = r"D:\zyt\git_ln\algo_agent\tests\playground\gen\g6\log\filtered_CN-streets.tsv"

# 设置中文字体（避免乱码）
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']  # 优先黑体，兼容Linux/Mac
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
plt.rcParams['figure.figsize'] = (12, 8)   # 画布大小
# plt.rcParams['dpi'] = 100                  # 分辨率

# -------------------------- 2. 读取过滤后的数据 --------------------------
# 读取数据并处理空值
df_addr = pd.read_csv(filtered_address, sep="\t", dtype=str).fillna("")
df_house = pd.read_csv(filtered_houses, sep="\t", dtype=str).fillna("")
df_street = pd.read_csv(filtered_streets, sep="\t", dtype=str).fillna("")

# 统一列名 & 提取坐标（处理address的坐标是区间，取均值；house是精确坐标）
# 处理address的坐标（x_min/x_max → 均值，y_min/y_max → 均值）
df_addr['x'] = df_addr.apply(lambda row: (float(row['x_min']) + float(row['x_max']))/2 if row['x_min'] else None, axis=1)
df_addr['y'] = df_addr.apply(lambda row: (float(row['y_min']) + float(row['y_max']))/2 if row['y_min'] else None, axis=1)
df_addr.rename(columns={'street_': 'street', 'city_': 'city'}, inplace=True)

# 处理house的坐标（转为浮点数）
df_house['x'] = pd.to_numeric(df_house['x'], errors='coerce')
df_house['y'] = pd.to_numeric(df_house['y'], errors='coerce')

# 合并所有带坐标的点（address + house）
df_all = pd.concat([
    df_addr[['street', 'city', 'x', 'y']].dropna(subset=['x', 'y']),
    df_house[['street', 'city', 'x', 'y']].dropna(subset=['x', 'y'])
], ignore_index=True)

# 去重（避免重复标记）
df_all = df_all.drop_duplicates(subset=['x', 'y', 'street'])

# -------------------------- 3. 构建街道连通图（复用前序逻辑） --------------------------
G = nx.Graph()
# 添加节点（所有街道）
for street in df_all['street'].unique():
    G.add_node(street)

# 添加边：同城市的街道互相连通（与前序代码逻辑一致）
city_groups = df_all.groupby('city')
for city, group in city_groups:
    city_streets = group['street'].unique()
    for i in range(len(city_streets)):
        for j in range(i + 1, len(city_streets)):
            G.add_edge(city_streets[i], city_streets[j])

# -------------------------- 4. 绘制地图 --------------------------
fig, ax = plt.subplots()

# ========== 步骤1：绘制节点（坐标点） ==========
# 按街道分组着色（不同街道不同颜色）
streets = df_all['street'].unique()
colors = plt.cm.tab10(range(len(streets)))  # 配色方案
street_color_map = dict(zip(streets, colors))

for street in streets:
    df_st = df_all[df_all['street'] == street]
    ax.scatter(
        df_st['x'], df_st['y'],
        label=street,
        color=street_color_map[street],
        s=100,  # 点大小
        alpha=0.7,  # 透明度
        edgecolors='black',  # 点边框
        linewidth=0.5
    )

# ========== 步骤2：绘制边（街道连通关系） ==========
# 遍历所有边，绘制两点之间的连线（取街道的中心点作为连线端点）
for (street1, street2) in G.edges():
    # 取street1的中心坐标
    df_s1 = df_all[df_all['street'] == street1]
    x1, y1 = df_s1['x'].mean(), df_s1['y'].mean()
    # 取street2的中心坐标
    df_s2 = df_all[df_all['street'] == street2]
    x2, y2 = df_s2['x'].mean(), df_s2['y'].mean()
    # 绘制连线
    ax.plot([x1, x2], [y1, y2], color='gray', linewidth=0.8, alpha=0.5, linestyle='--')

# ========== 步骤3：标注节点名称（街道+坐标） ==========
for idx, row in df_all.iterrows():
    ax.annotate(
        text=f"{row['street']}\n({row['x']:.4f}, {row['y']:.4f})",  # 标注内容：街道名+坐标
        xy=(row['x'], row['y']),  # 标注位置
        xytext=(5, 5),  # 文字偏移
        textcoords='offset points',
        fontsize=8,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8),  # 白色背景框
        arrowprops=dict(arrowstyle='->', color='gray', alpha=0.5)  # 箭头指向点
    )

# -------------------------- 5. 美化图表 & 保存 --------------------------
# 设置标题和轴标签
ax.set_title('北京市街道-地址-房屋坐标可视化（最大连通分量）', fontsize=14, fontweight='bold')
ax.set_xlabel('经度（X）', fontsize=12)
ax.set_ylabel('纬度（Y）', fontsize=12)

# 添加图例（街道名称）
ax.legend(
    title='街道名称',
    bbox_to_anchor=(1.05, 1),  # 图例放在画布右侧
    loc='upper left',
    fontsize=10
)

# 网格线
ax.grid(True, alpha=0.3, linestyle='-')

# 调整布局（避免图例/标注被截断）
plt.tight_layout()

# 保存图片（可选）
save_path = r"D:\zyt\git_ln\algo_agent\tests\playground\gen\g6\log\beijing_map.png"
plt.savefig(save_path, bbox_inches='tight', dpi=150)
print(f"地图已保存至：{save_path}")

# 显示图表
plt.show()

# -------------------------- 6. 输出统计信息 --------------------------
print("\n可视化统计信息：")
print(f"- 总标记点数：{len(df_all)}")
print(f"- 涉及街道数：{len(streets)}")
print(f"- 街道连通边数：{len(G.edges())}")
print(f"- 覆盖城市：{df_all['city'].unique()}")
