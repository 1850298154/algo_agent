import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.patches import Rectangle
from matplotlib import font_manager

# -------------------------- 配置中文显示 --------------------------
# 解决matplotlib中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']  # 中文支持
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
plt.rcParams['figure.figsize'] = (16, 10)  # 设置默认画布大小

# -------------------------- 读取过滤后的数据 --------------------------
base_dir = r"D:\zyt\git_ln\algo_agent\tests\playground\gen\g6\log\filtered_beijing"

# 读取三个文件
addresses_path = os.path.join(base_dir, "CN-addresses-beijing.tsv")
houses_path = os.path.join(base_dir, "CN-houses-beijing.tsv")
streets_path = os.path.join(base_dir, "CN-streets-beijing.tsv")

# 读取数据
df_addresses = pd.read_csv(addresses_path, sep='\t', encoding='utf-8', on_bad_lines='skip')
df_houses = pd.read_csv(houses_path, sep='\t', encoding='utf-8', on_bad_lines='skip')
df_streets = pd.read_csv(streets_path, sep='\t', encoding='utf-8', on_bad_lines='skip')

# 清理空值
df_addresses = df_addresses.dropna(subset=['street_', 'x_min', 'y_min'])
df_houses = df_houses.dropna(subset=['street', 'x', 'y'])

# -------------------------- 准备可视化数据 --------------------------
# 获取所有唯一的街道名称
unique_streets = df_addresses['street_'].unique()
print(f"待可视化的街道数量：{len(unique_streets)}")
print(f"街道列表：{list(unique_streets)}")

# 为每个街道分配唯一的颜色
# 使用tab10颜色方案，循环使用
colors = plt.cm.tab10(np.linspace(0, 1, len(unique_streets)))
street_color_map = dict(zip(unique_streets, colors))

# -------------------------- 创建可视化图表 --------------------------
fig, ax = plt.subplots(1, 1, figsize=(18, 12))

# 1. 绘制地址范围（矩形）- 代表addresses文件中的地址区间
for idx, row in df_addresses.iterrows():
    street_name = row['street_']
    color = street_color_map[street_name]
    
    # 提取坐标
    x_min, x_max = row['x_min'], row['x_max']
    y_min, y_max = row['y_min'], row['y_max']
    
    # 计算矩形宽度和高度
    width = x_max - x_min if x_max != x_min else 0.0001  # 避免宽度为0
    height = y_max - y_min if y_max != y_min else 0.0001
    
    # 绘制矩形（地址范围）
    rect = Rectangle((x_min, y_min), width, height, 
                     facecolor=color, alpha=0.3,  # 填充色半透明
                     edgecolor=color, linewidth=2,  # 边框色
                     label=f'{street_name} (地址范围)' if idx == 0 else "")
    ax.add_patch(rect)
    
    # 在矩形中心添加街道名称标注
    center_x = (x_min + x_max) / 2
    center_y = (y_min + y_max) / 2
    ax.text(center_x, center_y, street_name, 
            fontsize=8, ha='center', va='center', 
            bbox=dict(boxstyle="round,pad=0.3", facecolor=color, alpha=0.7))

# 2. 绘制具体的房屋位置（散点）- 代表houses文件中的具体房屋
for street_name in unique_streets:
    color = street_color_map[street_name]
    # 筛选该街道的房屋数据
    street_houses = df_houses[df_houses['street'] == street_name]
    
    if not street_houses.empty:
        # 绘制散点
        ax.scatter(street_houses['x'], street_houses['y'], 
                   color=color, s=100, alpha=0.8, 
                   marker='o', edgecolors='black', linewidth=1,
                   label=f'{street_name} (具体房屋)' if street_name == unique_streets[0] else "")

# -------------------------- 设置图表样式和标注 --------------------------
# 设置标题和坐标轴标签
ax.set_title('北京市街道地址分布可视化\n(矩形：地址区间 | 圆点：具体房屋)', 
             fontsize=20, fontweight='bold', pad=20)
ax.set_xlabel('经度 (X坐标)', fontsize=14, fontweight='bold')
ax.set_ylabel('纬度 (Y坐标)', fontsize=14, fontweight='bold')

# 添加网格
ax.grid(True, alpha=0.3, linestyle='--')

# -------------------------- 创建详细的图例 --------------------------
# 创建自定义图例
legend_elements = []

# 为每个街道添加图例项
for street_name in unique_streets:
    color = street_color_map[street_name]
    # 地址范围（矩形）图例
    rect_patch = Rectangle((0, 0), 1, 1, facecolor=color, alpha=0.3, 
                           edgecolor=color, linewidth=2, 
                           label=f'{street_name} - 地址范围')
    # 房屋位置（散点）图例
    scatter_patch = plt.Line2D([0], [0], marker='o', color='w', 
                               markerfacecolor=color, markeredgecolor='black', 
                               markersize=10, label=f'{street_name} - 具体房屋')
    
    legend_elements.extend([rect_patch, scatter_patch])

# 添加图例
ax.legend(handles=legend_elements, 
          loc='upper right', 
          bbox_to_anchor=(1.3, 1.0),
          fontsize=10,
          title='街道颜色说明',
          title_fontsize=12,
          frameon=True,
          shadow=True)

# -------------------------- 添加详细说明文本 --------------------------
info_text = f"""
可视化说明：
1. 颜色编码：每个街道对应唯一颜色（共{len(unique_streets)}个街道）
2. 图形含义：
   • 彩色半透明矩形：CN-addresses.tsv中的地址区间（x_min~x_max, y_min~y_max）
   • 彩色实心圆点：CN-houses.tsv中的具体房屋位置
3. 数据统计：
   • 地址区间数量：{len(df_addresses)}
   • 具体房屋数量：{len(df_houses)}
   • 涉及街道数量：{len(unique_streets)}
4. 坐标说明：X轴为经度，Y轴为纬度
"""

# 在图表左下角添加说明文本
ax.text(0.02, 0.02, info_text, 
        transform=ax.transAxes,
        fontsize=11,
        verticalalignment='bottom',
        bbox=dict(boxstyle="round,pad=0.5", facecolor='lightgray', alpha=0.8))

# -------------------------- 调整布局并保存 --------------------------
plt.tight_layout()

# 保存图片（高分辨率）
output_img_path = os.path.join(base_dir, "beijing_address_visualization.png")
plt.savefig(output_img_path, dpi=300, bbox_inches='tight')
print(f"可视化图片已保存至：{output_img_path}")

# 显示图表
plt.show()

# -------------------------- 输出详细的颜色映射表 --------------------------
print("\n=== 街道-颜色映射表 ===")
for i, (street, color) in enumerate(street_color_map.items()):
    # 将RGB颜色转换为十六进制
    hex_color = '#%02x%02x%02x' % (int(color[0]*255), int(color[1]*255), int(color[2]*255))
    print(f"{i+1}. 街道名称：{street}")
    print(f"   RGB颜色：{color[:3]}")
    print(f"   十六进制：{hex_color}")
    print("   " + "-"*50)