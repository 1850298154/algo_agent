import os
import csv

# 定义基础路径（g6文件夹路径）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 定义输入文件路径
INPUT_FILES = {
    "addresses": os.path.join(BASE_DIR, "log", "CN-addresses.tsv"),
    "houses": os.path.join(BASE_DIR, "log", "CN-houses.tsv"),
    "streets": os.path.join(BASE_DIR, "log", "CN-streets.tsv")
}
# 定义输出文件路径
OUTPUT_FILES = {
    "addresses": os.path.join(BASE_DIR, "CN-beijing-addresses.tsv"),
    "houses": os.path.join(BASE_DIR, "CN-beijing-houses.tsv"),
    "streets": os.path.join(BASE_DIR, "CN-beijing-streets.tsv")
}

def filter_beijing_addresses():
    """筛选地址文件中的北京数据"""
    try:
        with open(INPUT_FILES["addresses"], "r", encoding="utf-8", newline="") as infile, \
             open(OUTPUT_FILES["addresses"], "w", encoding="utf-8", newline="") as outfile:
            
            # TSV文件使用制表符分隔
            reader = csv.DictReader(infile, delimiter="\t")
            # 保留原表头
            writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames, delimiter="\t")
            writer.writeheader()
            
            # 筛选city_字段包含"北京市"或"Beijing"的行
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
            
            # 筛选city字段包含"北京市"或"Beijing"的行
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
            
            # 筛选state字段为"北京市"的行
            for row in reader:
                state = row.get("state", "").strip()
                if state == "北京市":
                    writer.writerow(row)
                    
        print(f"街道文件筛选完成：{OUTPUT_FILES['streets']}")
    except FileNotFoundError:
        print(f"错误：街道文件 {INPUT_FILES['streets']} 不存在")
    except Exception as e:
        print(f"街道文件处理错误：{str(e)}")

def main():
    """主函数"""
    # 检查log文件夹是否存在
    log_dir = os.path.join(BASE_DIR, "log")
    if not os.path.exists(log_dir):
        print(f"错误：log文件夹 {log_dir} 不存在")
        return
    
    # 执行筛选
    filter_beijing_addresses()
    filter_beijing_houses()
    filter_beijing_streets()
    
    print("\n所有文件筛选完成！")
    print(f"输出文件：")
    for name, path in OUTPUT_FILES.items():
        if os.path.exists(path):
            # 统计输出文件的行数（减去表头）
            with open(path, "r", encoding="utf-8") as f:
                line_count = sum(1 for _ in f) - 1
            print(f"  - {path} (包含 {line_count} 条北京数据)")

if __name__ == "__main__":
    main()