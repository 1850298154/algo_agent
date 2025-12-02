import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from typing import List, Dict
import numpy as np

# ===================== 数据读取与解析 =====================
def load_data(file_path: str = "random_data_1.json") -> Dict:
    """加载随机生成的JSON数据"""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# ===================== 可视化函数 =====================
def visualize_disaster_delivery_data(data: Dict, figsize: tuple = (12, 10)):
    """
    可视化灾害物资配送数据
    颜色定义：
    - 地图基础点：浅灰色
    - 可通行道路：绿色
    - 阻断道路：红色
    - 仓库位置：深蓝色（五角星）
    - 物资目标点：橙色（圆形）
    - 无人车位置：紫色（正方形）
    """
    # ========== 核心修复：解决Matplotlib中文乱码 ==========
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体（Windows：SimHei，Mac：PingFang SC）
    plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题
    # ====================================================
    
    # 创建画布
    plt.figure(figsize=figsize)
    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')
    
    # 1. 提取地图数据
    map_data = data["map_data"]
    points = map_data["points"]
    edges = map_data["edges"]
    
    # 2. 提取其他关键数据
    uvs = data["unmanned_vehicles"]
    materials = data["materials"]
    warehouse_pos = materials[0]["start_position"] if materials else {"x": 500, "y": 500}
    
    # ===================== 绘制道路边 =====================
    # 可通行道路（绿色）
    valid_edges = [e for e in edges if not e["is_blocked"]]
    for edge in valid_edges:
        start = edge["start"]
        end = edge["end"]
        plt.plot(
            [start["x"], end["x"]], 
            [start["y"], end["y"]], 
            'g-', linewidth=1.5, alpha=0.7, label='可通行道路' if valid_edges.index(edge) == 0 else ""
        )
    
    # 阻断道路（红色，带虚线）
    blocked_edges = [e for e in edges if e["is_blocked"]]
    for edge in blocked_edges:
        start = edge["start"]
        end = edge["end"]
        plt.plot(
            [start["x"], end["x"]], 
            [start["y"], end["y"]], 
            'r--', linewidth=2, alpha=0.8, label='阻断道路' if blocked_edges.index(edge) == 0 else ""
        )
    
    # ===================== 绘制地图坐标点 =====================
    point_x = [p["x"] for p in points]
    point_y = [p["y"] for p in points]
    plt.scatter(
        point_x, point_y, 
        c='lightgray', s=30, alpha=0.5, 
        label='地图坐标点', edgecolors='gray', linewidths=0.5
    )
    
    # ===================== 绘制仓库位置 =====================
    plt.scatter(
        warehouse_pos["x"], warehouse_pos["y"],
        c='darkblue', s=200, marker='*', alpha=0.9,
        label='仓库位置', edgecolors='navy', linewidths=2
    )
    
    # ===================== 绘制物资目标点 =====================
    target_x = [m["target_position"]["x"] for m in materials]
    target_y = [m["target_position"]["y"] for m in materials]
    plt.scatter(
        target_x, target_y,
        c='orange', s=80, alpha=0.8,
        label='物资目标点（受灾点）', edgecolors='darkorange', linewidths=1
    )
    
    # ===================== 绘制无人车位置 =====================
    uv_x = [uv["position"]["x"] for uv in uvs]
    uv_y = [uv["position"]["y"] for uv in uvs]
    uv_scatter = plt.scatter(
        uv_x, uv_y,
        c='purple', s=120, marker='s', alpha=0.8,
        label='无人车位置', edgecolors='darkviolet', linewidths=1.5
    )
    
    # 为无人车添加编号标签
    for i, uv in enumerate(uvs):
        plt.annotate(
            uv["uv_id"],
            (uv["position"]["x"], uv["position"]["y"]),
            xytext=(5, 5), textcoords='offset points',
            fontsize=8, color='darkviolet', fontweight='bold'
        )
    
    # ===================== 图表美化与标注 =====================
    # 设置标题和坐标轴
    plt.title('灾害物资配送系统 - 地图数据可视化', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('X 坐标（米）', fontsize=12)
    plt.ylabel('Y 坐标（米）', fontsize=12)
    
    # 设置网格
    plt.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
    
    # 设置图例（避免重复）
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(
        by_label.values(), by_label.keys(),
        loc='upper right', 
        framealpha=0.9,
        shadow=True,
        fontsize=10
    )
    
    # 添加统计信息文本框
    stats_text = f"""
    统计信息：
    • 无人车数量：{len(uvs)}
    • 物资目标点数量：{len(materials)}
    • 可通行道路数：{len(valid_edges)}
    • 阻断道路数：{len(blocked_edges)}
    • 地图坐标点数：{len(points)}
    """
    plt.text(
        0.02, 0.98, stats_text,
        transform=ax.transAxes,
        fontsize=9,
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    )
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图片
    plt.savefig('delivery_data_visualization.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("✅ 可视化完成！图片已保存为：delivery_data_visualization.png")

import platform
system = platform.system()
if system == "Windows":
    plt.rcParams['font.sans-serif'] = ['SimHei']
elif system == "Darwin":  # Mac
    plt.rcParams['font.sans-serif'] = ['PingFang SC']
else:  # Linux
    plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei']
plt.rcParams['axes.unicode_minus'] = False
# ===================== 主执行函数 =====================
if __name__ == "__main__":
    # 加载数据
    data = load_data("random_data_1.json")
    
    # 执行可视化
    visualize_disaster_delivery_data(data)