import pandas as pd
import networkx as nx
import numpy as np
from pathlib import Path

# -------------------------- 1. 配置参数与读取数据 --------------------------
# 定义文件路径
data_dir = Path(r"D:\zyt\git_ln\algo_agent\tests\playground\gen\g6\log\filtered_beijing")
addr_path = data_dir / "CN-addresses-beijing.tsv"
house_path = data_dir / "CN-houses-beijing.tsv"
street_path = data_dir / "CN-streets-beijing.tsv"

# 读取TSV文件（处理可能的编码问题）
df_addr = pd.read_csv(addr_path, sep="\t", encoding="utf-8-sig")
df_house = pd.read_csv(house_path, sep="\t", encoding="utf-8-sig")
df_street = pd.read_csv(street_path, sep="\t", encoding="utf-8-sig")

# 标准化列名（处理可能的空格/下划线差异）
df_addr.columns = df_addr.columns.str.strip().str.replace(" ", "_")
df_house.columns = df_house.columns.str.strip().str.replace(" ", "_")
df_street.columns = df_street.columns.str.strip().str.replace(" ", "_")

# -------------------------- 2. 筛选北京市数据 --------------------------
# 筛选state/省份为"北京市"的数据（兼容不同列名）
df_street_bj = df_street[
    (df_street["state"] == "北京市") | (df_street["province"] == "北京市")
].copy()

# 获取北京市的街道名称列表
bj_street_names = df_street_bj["street_name"].dropna().unique()

# -------------------------- 3. 过滤addresses：关联其他文件的street --------------------------
# 1) 过滤addresses中street_在北京市街道列表/house的street中出现的记录
house_street_names = df_house["street"].dropna().unique()
valid_streets = set(bj_street_names) | set(house_street_names)
df_addr_bj = df_addr[
    df_addr["street_"].dropna().isin(valid_streets)
].copy()

# -------------------------- 4. 构建街道连通图，筛选最大连通分量 --------------------------
def build_street_graph(df_addr, df_house):
    """
    构建街道连通图：
    - 节点：街道名称
    - 边：基于地理坐标相邻（或同一区域）的街道
    """
    G = nx.Graph()
    
    # 提取有坐标的街道数据（addresses）
    addr_coords = df_addr[["street_", "x_min", "y_min"]].dropna()
    # 提取有坐标的街道数据（houses）
    house_coords = df_house[["street", "x", "y"]].dropna()
    
    # 添加节点（所有有效街道）
    all_streets = set(addr_coords["street_"]) | set(house_coords["street"])
    G.add_nodes_from(all_streets)
    
    # 基于坐标距离构建边（简化逻辑：同一城市内坐标相近的街道连通）
    # 实际场景可根据业务调整距离阈值（如0.001经纬度≈100米）
    threshold = 0.001
    
    # 处理addresses中的街道连通
    for idx1, row1 in addr_coords.iterrows():
        for idx2, row2 in addr_coords.iterrows():
            if idx1 >= idx2:
                continue
            # 计算经纬度距离
            dist = np.sqrt(
                (row1["x_min"] - row2["x_min"])**2 + 
                (row1["y_min"] - row2["y_min"])**2
            )
            if dist < threshold:
                G.add_edge(row1["street_"], row2["street_"])
    
    # 处理houses中的街道连通
    for idx1, row1 in house_coords.iterrows():
        for idx2, row2 in house_coords.iterrows():
            if idx1 >= idx2:
                continue
            dist = np.sqrt(
                (row1["x"] - row2["x"])**2 + 
                (row1["y"] - row2["y"])**2
            )
            if dist < threshold:
                G.add_edge(row1["street"], row2["street"])
    
    # 处理addresses和houses之间的街道连通
    for _, addr_row in addr_coords.iterrows():
        for _, house_row in house_coords.iterrows():
            dist = np.sqrt(
                (addr_row["x_min"] - house_row["x"])**2 + 
                (addr_row["y_min"] - house_row["y"])**2
            )
            if dist < threshold:
                G.add_edge(addr_row["street_"], house_row["street"])
    
    return G

# 构建连通图
street_graph = build_street_graph(df_addr_bj, df_house)

# 筛选最大连通分量
if len(street_graph.nodes) > 0:
    largest_cc = max(nx.connected_components(street_graph), key=len)
else:
    largest_cc = set()

# -------------------------- 5. 最终过滤：字段无缺失 + 最大连通分量 --------------------------
# 5.1 过滤CN-addresses.tsv
# 字段完整性校验（所有列无缺失）
addr_required_cols = [
    "postal_code_", "city_", "street_", "x_min", "x_max", 
    "y_min", "y_max", "house_min", "house_max", "house_odd", "house_even"
]
df_addr_final = df_addr_bj[
    df_addr_bj[addr_required_cols].notna().all(axis=1) &  # 无缺失字段
    df_addr_bj["street_"].isin(largest_cc)  # 属于最大连通分量
].copy()

# 5.2 过滤CN-houses.tsv
# 筛选北京市相关 + 字段完整 + 属于最大连通分量
house_required_cols = ["postal_code", "city", "street", "house_number", "x", "y", "country"]
df_house_bj = df_house[
    df_house["street"].isin(valid_streets)  # 关联有效街道
].copy()
df_house_final = df_house_bj[
    df_house_bj[house_required_cols].notna().all(axis=1) &  # 无缺失字段
    df_house_bj["street"].isin(largest_cc)  # 属于最大连通分量
].copy()

# 5.3 过滤CN-streets.tsv
street_required_cols = ["city", "country", "state", "province", "postal_code", "street_name"]
df_street_final = df_street_bj[
    df_street_bj[street_required_cols].notna().all(axis=1) &  # 无缺失字段
    df_street_bj["street_name"].isin(largest_cc)  # 属于最大连通分量
].copy()

# -------------------------- 6. 保存过滤后的数据 --------------------------
output_dir = data_dir / "filtered_bj"
output_dir.mkdir(exist_ok=True)

df_addr_final.to_csv(output_dir / "CN-addresses.tsv", sep="\t", index=False, encoding="utf-8-sig")
df_house_final.to_csv(output_dir / "CN-houses.tsv", sep="\t", index=False, encoding="utf-8-sig")
df_street_final.to_csv(output_dir / "CN-streets.tsv", sep="\t", index=False, encoding="utf-8-sig")

print(f"过滤完成！结果保存至：{output_dir}")
print(f"- 过滤后addresses行数：{len(df_addr_final)}")
print(f"- 过滤后houses行数：{len(df_house_final)}")
print(f"- 过滤后streets行数：{len(df_street_final)}")
print(f"- 最大连通分量街道数：{len(largest_cc)}")