import pandas as pd
import networkx as nx
from typing import Set

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

# 输出统计信息
print(f"过滤完成！")
print(f"- 原始address记录数：{len(df_address)} → 过滤后：{len(df_address_final)}")
print(f"- 原始houses记录数：{len(df_houses)} → 过滤后：{len(df_houses_final)}")
print(f"- 原始streets记录数：{len(df_streets)} → 过滤后：{len(df_streets_final)}")
print(f"- 最大连通分量街道数：{len(largest_cc)}")
print(f"文件保存路径：")
print(f"- {output_address}")
print(f"- {output_houses}")
print(f"- {output_streets}")