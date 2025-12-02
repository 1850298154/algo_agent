import os
import csv
import matplotlib.pyplot as plt
import numpy as np
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

# 绘图样式配置（保留原区分规则）
PLOT_STYLES = {
    "addresses": {
        "scatter": {"color": "#FF6B6B", "marker": "o", "label": "地址数据", "size": 80},
        "line": {"color": "#FF6B6B", "style": "-", "alpha": 0.4, "width": 1}
    },
    "houses": {
        "scatter": {"color": "#4ECDC4", "marker": "^", "label": "房屋数据", "size": 100},
        "line": {"color": "#4ECDC4", "style": "--", "alpha": 0.5, "width": 1}
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

# 新增：按街道名称读取数据（返回 {街道名: [(x1,y1), (x2,y2)...]} 格式）
def read_data_by_street(file_type):
    """按街道名称分组读取坐标数据"""
    filepath = OUTPUT_FILES[file_type]
    street_data = {}  # key: 街道名, value: 坐标列表
    
    if not os.path.exists(filepath):
        print(f"警告：{filepath} 文件不存在，无{PLOT_STYLES[file_type]['scatter']['label']}可绘制")
        return street_data
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            
            # 适配不同文件的字段名
            if file_type == "addresses":
                street_field = "street_"
                x_field, y_field = "x_min", "y_min"
            elif file_type == "houses":
                street_field = "street"
                x_field, y_field = "x", "y"
            else:
                return street_data
            
            for row in reader:
                # 提取街道名（去重空格）
                street_name = row.get(street_field, "").strip()
                if not street_name:
                    continue  # 跳过无街道名的记录
                
                # 提取并校验坐标
                x_val = row.get(x_field, "").strip()
                y_val = row.get(y_field, "").strip()
                if x_val and y_val and x_val.replace('.','').isdigit() and y_val.replace('.','').isdigit():
                    x = float(x_val)
                    y = float(y_val)
                    
                    # 按街道名分组
                    if street_name not in street_data:
                        street_data[street_name] = []
                    street_data[street_name].append((x, y))
        
        # 统计各街道的点数
        valid_streets = {k: v for k, v in street_data.items() if len(v) >= 2}
        print(f"读取到{PLOT_STYLES[file_type]['scatter']['label']}：")
        print(f"  - 有效街道数（≥2个点）：{len(valid_streets)}")
        print(f"  - 总坐标点数：{sum(len(v) for v in street_data.values())}")
    except Exception as e:
        print(f"读取{PLOT_STYLES[file_type]['scatter']['label']}失败：{str(e)}")
    
    return street_data

# 核心：按街道名称绘制连线
def plot_by_street_connection():
    """按街道名称连接同街道的坐标点"""
    # 设置中文字体
    plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
    plt.rcParams["axes.unicode_minus"] = False
    
    # 创建画布
    fig, ax = plt.subplots(figsize=(14, 9))
    
    # 1. 处理地址数据（按街道连线）
    addr_street_data = read_data_by_street("addresses")
    for street_name, coords in addr_street_data.items():
        if len(coords) >= 2:  # 至少2个点才连线
            x = [p[0] for p in coords]
            y = [p[1] for p in coords]
            # 绘制同街道的连线
            ax.plot(x, y, 
                    color=PLOT_STYLES["addresses"]["line"]["color"],
                    linestyle=PLOT_STYLES["addresses"]["line"]["style"],
                    alpha=PLOT_STYLES["addresses"]["line"]["alpha"],
                    linewidth=PLOT_STYLES["addresses"]["line"]["width"])
            # 绘制地址散点
            ax.scatter(x, y,
                      c=PLOT_STYLES["addresses"]["scatter"]["color"],
                      marker=PLOT_STYLES["addresses"]["scatter"]["marker"],
                      s=PLOT_STYLES["addresses"]["scatter"]["size"],
                      label=PLOT_STYLES["addresses"]["scatter"]["label"] if street_name == list(addr_street_data.keys())[0] else "",
                      alpha=0.8, edgecolors="black", linewidth=0.8, zorder=5)
    
    # 2. 处理房屋数据（按街道连线）
    house_street_data = read_data_by_street("houses")
    for street_name, coords in house_street_data.items():
        if len(coords) >= 2:
            x = [p[0] for p in coords]
            y = [p[1] for p in coords]
            # 绘制同街道的连线
            ax.plot(x, y,
                    color=PLOT_STYLES["houses"]["line"]["color"],
                    linestyle=PLOT_STYLES["houses"]["line"]["style"],
                    alpha=PLOT_STYLES["houses"]["line"]["alpha"],
                    linewidth=PLOT_STYLES["houses"]["line"]["width"])
            # 绘制房屋散点
            ax.scatter(x, y,
                      c=PLOT_STYLES["houses"]["scatter"]["color"],
                      marker=PLOT_STYLES["houses"]["scatter"]["marker"],
                      s=PLOT_STYLES["houses"]["scatter"]["size"],
                      label=PLOT_STYLES["houses"]["scatter"]["label"] if street_name == list(house_street_data.keys())[0] else "",
                      alpha=0.8, edgecolors="black", linewidth=0.8, zorder=5)
    
    # 图表样式优化
    ax.set_title("北京市数据XY坐标分布图（按街道名称连线）", fontsize=18, pad=25, fontweight="bold")
    ax.set_xlabel("X 坐标", fontsize=14, fontweight="medium")
    ax.set_ylabel("Y 坐标", fontsize=14, fontweight="medium")
    ax.grid(True, alpha=0.2, linestyle="-", linewidth=0.8)
    ax.legend(loc="best", fontsize=12, framealpha=0.9)
    ax.set_axisbelow(True)
    
    # 保存图片
    save_path = os.path.join(BASE_DIR, "log", "Beijing_XY_By_Street_Connection.png")
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight", facecolor="white")
    print(f"\n按街道连线的图表已保存至：{save_path}")
    
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
    for name in ["addresses", "houses", "streets"]:
        path = OUTPUT_FILES[name]
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                line_count = sum(1 for _ in f) - 1
            print(f"  - {os.path.basename(path)}: {line_count} 条数据")
        else:
            print(f"  - {os.path.basename(path)}: 0 条数据")
    
    # 3. 按街道连线绘图
    print("\n=== 开始绘制按街道连线的坐标图 ===")
    plot_by_street_connection()

if __name__ == "__main__":
    main()