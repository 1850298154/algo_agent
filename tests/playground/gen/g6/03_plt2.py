import os
import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import KDTree  # 用于最近邻连线（可选）
import warnings
warnings.filterwarnings('ignore')

# 基础路径配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILES = {
    "addresses": os.path.join(BASE_DIR, "log", "CN-addresses.tsv"),
    "houses": os.path.join(BASE_DIR, "log", "CN-houses.tsv"),
    "streets": os.path.join(BASE_DIR, "log", "CN-streets.tsv")
}
OUTPUT_FILES = {
    "addresses": os.path.join(BASE_DIR, "log", "CN-beijing-addresses.tsv"),
    "houses": os.path.join(BASE_DIR, "log", "CN-beijing-houses.tsv"),
    "streets": os.path.join(BASE_DIR, "log", "CN-beijing-streets.tsv")
}

# 绘图样式（新增连线颜色/样式）
PLOT_STYLES = {
    "addresses": {
        "scatter": {"color": "#FF6B6B", "marker": "o", "label": "地址数据", "size": 80},
        "line": {"color": "#FF6B6B", "style": "-", "alpha": 0.4, "width": 1}  # 地址连线样式
    },
    "houses": {
        "scatter": {"color": "#4ECDC4", "marker": "^", "label": "房屋数据", "size": 100},
        "line": {"color": "#4ECDC4", "style": "--", "alpha": 0.5, "width": 1}  # 房屋连线样式
    },
    "streets": {
        "scatter": {"color": "#45B7D1", "marker": "s", "label": "街道数据", "size": 60},
        "line": {"color": "#45B7D1", "style": ":", "alpha": 0.6, "width": 1}   # 街道连线样式
    }
}

# 筛选函数（保持不变）
def filter_beijing_addresses():
    try:
        with open(INPUT_FILES["addresses"], "r", encoding="utf-8", newline="") as infile, \
             open(OUTPUT_FILES["addresses"], "w", encoding="utf-8", newline="") as outfile:
            reader = csv.DictReader(infile, delimiter="\t")
            writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames, delimiter="\t")
            writer.writeheader()
            for row in reader:
                city = row.get("city_", "").strip()
                if "北京市" in city or "Beijing" in city:
                    writer.writerow(row)
        print(f"地址文件筛选完成：{OUTPUT_FILES['addresses']}")
    except Exception as e:
        print(f"地址文件处理错误：{str(e)}")

def filter_beijing_houses():
    try:
        with open(INPUT_FILES["houses"], "r", encoding="utf-8", newline="") as infile, \
             open(OUTPUT_FILES["houses"], "w", encoding="utf-8", newline="") as outfile:
            reader = csv.DictReader(infile, delimiter="\t")
            writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames, delimiter="\t")
            writer.writeheader()
            for row in reader:
                city = row.get("city", "").strip()
                if "北京市" in city or "Beijing" in city:
                    writer.writerow(row)
        print(f"房屋文件筛选完成：{OUTPUT_FILES['houses']}")
    except Exception as e:
        print(f"房屋文件处理错误：{str(e)}")

def filter_beijing_streets():
    try:
        with open(INPUT_FILES["streets"], "r", encoding="utf-8", newline="") as infile, \
             open(OUTPUT_FILES["streets"], "w", encoding="utf-8", newline="") as outfile:
            reader = csv.DictReader(infile, delimiter="\t")
            writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames, delimiter="\t")
            writer.writeheader()
            for row in reader:
                state = row.get("state", "").strip()
                if state == "北京市":
                    writer.writerow(row)
        print(f"街道文件筛选完成：{OUTPUT_FILES['streets']}")
    except Exception as e:
        print(f"街道文件处理错误：{str(e)}")

# 读取坐标（优化：返回有序坐标，方便连线）
def read_coordinates(file_type):
    filepath = OUTPUT_FILES[file_type]
    x_coords = []
    y_coords = []
    
    if not os.path.exists(filepath):
        print(f"警告：{filepath} 文件不存在，无{PLOT_STYLES[file_type]['scatter']['label']}可绘制")
        return x_coords, y_coords
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            # 按文件类型匹配XY字段
            if file_type == "addresses":
                x_field, y_field = "x_min", "y_min"
            elif file_type == "houses":
                x_field, y_field = "x", "y"
            elif file_type == "streets":
                print(f"提示：街道文件无XY坐标字段，跳过绘制")
                return x_coords, y_coords
            
            # 读取并校验坐标（保留原始顺序，用于连线）
            for row in reader:
                x_val = row.get(x_field, "").strip()
                y_val = row.get(y_field, "").strip()
                if x_val and y_val and x_val.replace('.','').isdigit() and y_val.replace('.','').isdigit():
                    x_coords.append(float(x_val))
                    y_coords.append(float(y_val))
        
        print(f"读取到{PLOT_STYLES[file_type]['scatter']['label']}坐标数：{len(x_coords)}")
    except Exception as e:
        print(f"读取{PLOT_STYLES[file_type]['scatter']['label']}坐标失败：{str(e)}")
    
    return x_coords, y_coords

# 新增：绘制连线的辅助函数
def plot_connections(ax, x, y, style, connect_type="sequence"):
    """
    绘制数据点连线
    :param ax: 绘图轴对象
    :param x/y: 坐标列表
    :param style: 连线样式字典
    :param connect_type: 连线类型 - sequence（顺序连线）/ nearest（最近邻连线）
    """
    if len(x) < 2:
        return  # 至少2个点才连线
    
    if connect_type == "sequence":
        # 方式1：按数据读取顺序连线（展示原始顺序关联）
        ax.plot(x, y, 
                color=style["color"], 
                linestyle=style["style"], 
                alpha=style["alpha"], 
                linewidth=style["width"])
    
    elif connect_type == "nearest":
        # 方式2：最近邻连线（展示空间相邻关系）
        points = np.column_stack((x, y))
        tree = KDTree(points)
        # 为每个点连接最近的点（排除自身）
        for i in range(len(points)):
            dist, idx = tree.query(points[i], k=2)  # k=2：取最近的2个（第1个是自身）
            nearest_idx = idx[1]
            ax.plot([x[i], x[nearest_idx]], [y[i], y[nearest_idx]],
                    color=style["color"],
                    linestyle=style["style"],
                    alpha=style["alpha"] * 0.7,
                    linewidth=style["width"])

# 优化后的绘图函数（含连线）
def plot_beijing_data():
    # 设置中文字体
    plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
    plt.rcParams["axes.unicode_minus"] = False
    
    # 创建画布（更大尺寸，适配连线）
    fig, ax = plt.subplots(figsize=(14, 9))
    
    # 先绘制连线，再绘制散点（让点覆盖在线上，更清晰）
    for file_type in ["addresses", "houses", "streets"]:
        x, y = read_coordinates(file_type)
        if x and y:
            # 1. 绘制连线（可切换 connect_type="sequence" 或 "nearest"）
            plot_connections(ax, x, y, PLOT_STYLES[file_type]["line"], connect_type="sequence")
            # 2. 绘制散点
            scatter_style = PLOT_STYLES[file_type]["scatter"]
            ax.scatter(x, y, 
                      c=scatter_style["color"], 
                      marker=scatter_style["marker"], 
                      s=scatter_style["size"], 
                      label=scatter_style["label"],
                      alpha=0.8,
                      edgecolors="black", linewidth=0.8,
                      zorder=5)  # zorder让点在最上层
    
    # 图表样式优化
    ax.set_title("北京市地址/房屋/街道数据XY坐标分布图（含连线）", fontsize=18, pad=25, fontweight="bold")
    ax.set_xlabel("X 坐标", fontsize=14, fontweight="medium")
    ax.set_ylabel("Y 坐标", fontsize=14, fontweight="medium")
    ax.grid(True, alpha=0.2, linestyle="-", linewidth=0.8)  # 更细腻的网格
    ax.legend(loc="best", fontsize=12, framealpha=0.9)      # 半透明图例框
    ax.set_axisbelow(True)  # 网格在底层
    
    # 保存高清图片
    save_path = os.path.join(BASE_DIR, "log", "Beijing_XY_Coordinates_With_Lines.png")
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight", facecolor="white")
    print(f"\n带连线的图表已保存至：{save_path}")
    
    # 显示图表
    plt.show()

# 主函数
def main():
    log_dir = os.path.join(BASE_DIR, "log")
    if not os.path.exists(log_dir):
        print(f"错误：log文件夹 {log_dir} 不存在")
        return
    
    # 1. 筛选数据
    filter_beijing_addresses()
    filter_beijing_houses()
    filter_beijing_streets()
    
    # 2. 统计结果
    print("\n=== 筛选结果统计 ===")
    for name, path in OUTPUT_FILES.items():
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                line_count = sum(1 for _ in f) - 1
            print(f"  - {os.path.basename(path)}: {line_count} 条数据")
        else:
            print(f"  - {os.path.basename(path)}: 0 条数据")
    
    # 3. 绘制带连线的图表
    print("\n=== 开始绘制带连线的坐标图 ===")
    plot_beijing_data()

if __name__ == "__main__":
    main()