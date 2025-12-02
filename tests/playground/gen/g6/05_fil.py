import pandas as pd
import os

# 设置文件路径
base_dir = r"D:\zyt\git_ln\algo_agent\tests\playground\gen\g6\log"
addresses_path = os.path.join(base_dir, "CN-addresses.tsv")
houses_path = os.path.join(base_dir, "CN-houses.tsv")
streets_path = os.path.join(base_dir, "CN-streets.tsv")

# 读取数据（处理TSV格式）
df_addresses = pd.read_csv(addresses_path, sep='\t', encoding='utf-8', on_bad_lines='skip')
df_houses = pd.read_csv(houses_path, sep='\t', encoding='utf-8', on_bad_lines='skip')
df_streets = pd.read_csv(streets_path, sep='\t', encoding='utf-8', on_bad_lines='skip')

# 1. 过滤出state/省份为"北京市"的数据
# 先查看列名，确保正确匹配
print("Streets文件列名：", df_streets.columns.tolist())
print("Addresses文件列名：", df_addresses.columns.tolist())
print("Houses文件列名：", df_houses.columns.tolist())

# 过滤streets中省份为北京市的数据
# 处理不同的列名情况（state/province）
if 'state' in df_streets.columns:
    df_streets_beijing = df_streets[df_streets['state'] == "北京市"].copy()
elif 'province' in df_streets.columns:
    df_streets_beijing = df_streets[df_streets['province'] == "北京市"].copy()
else:
    print("未找到省份相关列")
    df_streets_beijing = pd.DataFrame()

# 获取北京市的街道名称列表
beijing_streets = df_streets_beijing['street_name'].dropna().unique()
print(f"北京市街道数量：{len(beijing_streets)}")

# 2. 过滤addresses文件：只保留北京市街道且street_在其他文件中出现的数据
# 先统一街道列名的匹配
addresses_street_col = 'street_' if 'street_' in df_addresses.columns else 'street'
houses_street_col = 'street' if 'street' in df_houses.columns else 'street_'

# 过滤addresses：只保留街道在北京市街道列表中的数据
df_addresses_beijing = df_addresses[
    df_addresses[addresses_street_col].isin(beijing_streets)
].copy()

# 获取addresses中保留的街道列表
remaining_streets = df_addresses_beijing[addresses_street_col].dropna().unique()

# 3. 过滤houses文件：只保留街道在remaining_streets中的数据
df_houses_beijing = df_houses[
    df_houses[houses_street_col].isin(remaining_streets)
].copy()

# 4. 最终过滤streets文件：只保留在addresses中出现的街道
df_streets_final = df_streets_beijing[
    df_streets_beijing['street_name'].isin(remaining_streets)
].copy()

# 5. 保存过滤后的数据
output_dir = os.path.join(base_dir, "filtered_beijing")
os.makedirs(output_dir, exist_ok=True)

df_addresses_beijing.to_csv(
    os.path.join(output_dir, "CN-addresses-beijing.tsv"),
    sep='\t',
    index=False,
    encoding='utf-8'
)

df_houses_beijing.to_csv(
    os.path.join(output_dir, "CN-houses-beijing.tsv"),
    sep='\t',
    index=False,
    encoding='utf-8'
)

df_streets_final.to_csv(
    os.path.join(output_dir, "CN-streets-beijing.tsv"),
    sep='\t',
    index=False,
    encoding='utf-8'
)

# 打印统计信息
print("\n过滤结果统计：")
print(f"原始Addresses行数：{len(df_addresses)} -> 过滤后：{len(df_addresses_beijing)}")
print(f"原始Houses行数：{len(df_houses)} -> 过滤后：{len(df_houses_beijing)}")
print(f"原始Streets行数：{len(df_streets)} -> 过滤后：{len(df_streets_final)}")
print(f"\n过滤后的数据已保存到：{output_dir}")