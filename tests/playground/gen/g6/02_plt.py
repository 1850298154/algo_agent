import os
import csv
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')  # 忽略绘图无关警告

# 定义基础路径（g6文件夹路径）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 定义输入文件路径（读log目录）
INPUT_FILES = {
    "addresses": os.path.join(BASE_DIR, "log", "CN-addresses.tsv"),
    "houses": os.path.join(BASE_DIR, "log", "CN-houses.tsv"),
    "streets": os.path.join(BASE_DIR, "log", "CN-streets.tsv")
}
# 定义输出文件路径（写log目录）
OUTPUT_FILES = {
    "addresses": os.path.join(BASE_DIR, "log", "CN-beijing-addresses.tsv"),
    "houses": os.path.join(BASE_DIR, "log", "CN-beijing-houses.tsv"),
    "streets": os.path.join(BASE_DIR, "log", "CN-beijing-streets.tsv")
}

# 绘图样式配置
PLOT_STYLES = {
    "addresses": {"color": "#FF6B6B", "marker": "o", "label": "地址数据", "size": 80},
    "houses": {"color": "#4ECDC4", "marker": "^", "label": "房屋数据", "size": 100},
    "streets": {"color": "#45B7D1", "marker": "s", "label": "街道数据", "size": 60}
}

def filter_beijing_addresses():
    """筛选地址文件中的北京数据"""
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
    except FileNotFoundError:
        print(f"错误：地址文件 {INPUT_FILES['addresses']} 不存在")
    except Exception as e:
        print(f"地址文件处理错误：{str(e)}")

def filter_beijing_houses():
    """筛选房屋文件中的北京数据"""
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
    except FileNotFoundError:
        print(f"错误：房屋文件 {INPUT_FILES['houses']} 不存在")
    except Exception as e:
        print(f"房屋文件处理错误：{str(e)}")

def filter_beijing_streets():
    """筛选街道文件中的北京数据（state字段为北京市）"""
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
    except FileNotFoundError:
        print(f"错误：街道文件 {INPUT_FILES['streets']} 不存在")
    except Exception as e:
        print(f"街道文件处理错误：{str(e)}")

def read_coordinates(file_type):
    """读取筛选后文件的xy坐标"""
    filepath = OUTPUT_FILES[file_type]
    x_coords = []
    y_coords = []
    
    if not os.path.exists(filepath):
        print(f"警告：{filepath} 文件不存在，无{PLOT_STYLES[file_type]['label']}可绘制")
        return x_coords, y_coords
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            
            # 根据不同文件类型获取对应的xy字段名
            if file_type == "addresses":
                x_field = "x_min"  # 地址文件用x_min/y_min作为坐标（也可改用x_max/y_max）
                y_field = "y_min"
            elif file_type == "houses":
                x_field = "x"      # 房屋文件直接用x/y字段
                y_field = "y"
            elif file_type == "streets":
                # 街道文件原始数据无xy字段，这里做兼容处理
                print(f"提示：街道文件无直接xy坐标字段，跳过绘制")
                return x_coords, y_coords
            
            for row in reader:
                # 过滤空值和非数字的坐标
                x_val = row.get(x_field, "").strip()
                y_val = row.get(y_field, "").strip()
                if x_val and y_val and x_val.replace('.','').isdigit() and y_val.replace('.','').isdigit():
                    x_coords.append(float(x_val))
                    y_coords.append(float(y_val))
        
        print(f"读取到{PLOT_STYLES[file_type]['label']}坐标数：{len(x_coords)}")
    except Exception as e:
        print(f"读取{PLOT_STYLES[file_type]['label']}坐标失败：{str(e)}")
    
    return x_coords, y_coords

def plot_beijing_data():
    """绘制北京数据的xy坐标图"""
    # 设置中文字体（解决中文乱码）
    plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
    plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题
    
    # 创建画布
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # 依次读取并绘制各类数据
    for file_type in ["addresses", "houses", "streets"]:
        x, y = read_coordinates(file_type)
        if x and y:
            style = PLOT_STYLES[file_type]
            ax.scatter(x, y, 
                      c=style["color"], 
                      marker=style["marker"], 
                      s=style["size"], 
                      label=style["label"],
                      alpha=0.7,  # 透明度（避免点重叠）
                      edgecolors="black", linewidth=0.5)  # 加黑色边框更清晰
    
    # 设置图表样式
    ax.set_title("北京市地址/房屋/街道数据XY坐标分布图", fontsize=16, pad=20)
    ax.set_xlabel("X 坐标", fontsize=12)
    ax.set_ylabel("Y 坐标", fontsize=12)
    ax.grid(True, alpha=0.3, linestyle="--")  # 网格线
    ax.legend(loc="best", fontsize=11)        # 图例
    
    # 调整布局并保存图片（保存到log目录）
    plt.tight_layout()
    save_path = os.path.join(BASE_DIR, "log", "Beijing_XY_Coordinates.png")
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    print(f"\n图表已保存至：{save_path}")
    
    # 显示图表
    plt.show()

def main():
    """主函数"""
    # 检查log文件夹是否存在
    log_dir = os.path.join(BASE_DIR, "log")
    if not os.path.exists(log_dir):
        print(f"错误：log文件夹 {log_dir} 不存在")
        return
    
    # 1. 执行数据筛选
    filter_beijing_addresses()
    filter_beijing_houses()
    filter_beijing_streets()
    
    # 2. 统计筛选结果
    print("\n=== 筛选结果统计 ===")
    for name, path in OUTPUT_FILES.items():
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                line_count = sum(1 for _ in f) - 1  # 减表头行
            print(f"  - {path.split('/')[-1].split('\\')[-1]}: {line_count} 条数据")
        else:
            print(f"  - {path.split('/')[-1].split('\\')[-1]}: 0 条数据")
    
    # 3. 绘制XY坐标图
    print("\n=== 开始绘制坐标图 ===")
    plot_beijing_data()

if __name__ == "__main__":
    main()