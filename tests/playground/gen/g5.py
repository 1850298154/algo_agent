
import json
import random
from typing import List, Dict, Tuple
from pydantic import BaseModel, Field
from datetime import datetime

# ===================== 数据结构定义（Pydantic BaseModel） =====================
class Point(BaseModel):
    """地图坐标点模型"""
    x: float = Field(..., description="横坐标，单位：米")
    y: float = Field(..., description="纵坐标，单位：米")

class Edge(BaseModel):
    """地图边（道路）模型"""
    start: Point = Field(..., description="边的起点坐标")
    end: Point = Field(..., description="边的终点坐标")
    is_blocked: bool = Field(default=False, description="道路是否阻断，True=阻断，False=通行")

class MapData(BaseModel):
    """车辆可行驶的地图数据模型"""
    points: List[Point] = Field(..., description="地图中所有坐标点列表")
    edges: List[Edge] = Field(..., description="地图中所有道路边列表")

class UAV(BaseModel):
    """无人机数据模型"""
    uav_id: str = Field(..., description="无人机唯一标识，如UAV001")
    load_capacity: int = Field(default=1, description="无人机运载容量，固定为1（单位：箱）")

class UnmannedVehicle(BaseModel):
    """无人车数据模型"""
    uv_id: str = Field(..., description="无人车唯一标识，如UV001")
    position: Point = Field(..., description="无人车当前位置坐标")
    uav_capacity: int = Field(..., description="无人车可携带的无人机最大数量")

class Material(BaseModel):
    """物资数据模型"""
    material_id: str = Field(..., description="物资唯一标识，如M001")
    start_position: Point = Field(..., description="物资起点位置（仓库坐标）")
    target_position: Point = Field(..., description="物资目标位置（受灾点坐标）")

class AllData(BaseModel):
    """全量数据聚合模型"""
    map_data: MapData = Field(..., description="地图数据")
    unmanned_vehicles: List[UnmannedVehicle] = Field(..., description="所有无人车数据")
    uavs: List[UAV] = Field(..., description="所有无人机数据")
    materials: List[Material] = Field(..., description="所有物资数据")

# ===================== 随机数据生成函数 =====================
def generate_random_point(min_val: float = 0, max_val: float = 1000) -> Point:
    """生成随机坐标点（x,y范围：min_val~max_val米）"""
    return Point(
        x=round(random.uniform(min_val, max_val), 2),
        y=round(random.uniform(min_val, max_val), 2)
    )

def generate_random_edge(points: List[Point]) -> Edge:
    """基于地图点生成随机道路边"""
    start = random.choice(points)
    end = random.choice([p for p in points if p != start])
    return Edge(
        start=start,
        end=end,
        is_blocked=random.choice([True, False]) if random.random() < 0.2 else False  # 20%概率阻断
    )

def generate_random_map(num_points: int = 10, num_edges: int = 15) -> MapData:
    """生成随机地图数据"""
    points = [generate_random_point() for _ in range(num_points)]
    edges = [generate_random_edge(points) for _ in range(num_edges)]
    return MapData(points=points, edges=edges)

def generate_unmanned_vehicles(num_uv: int = 3) -> List[UnmannedVehicle]:
    """生成随机无人车数据"""
    uvs = []
    for i in range(num_uv):
        uvs.append(UnmannedVehicle(
            uv_id=f"UV{i+1:03d}",
            position=generate_random_point(),
            uav_capacity=random.randint(1, 3)  # 每车可带1-3架无人机
        ))
    return uvs

def generate_uavs(num_uav: int = 8) -> List[UAV]:
    """生成随机无人机数据（运载容量固定为1）"""
    return [
        UAV(uav_id=f"UAV{i+1:03d}", load_capacity=1)
        for i in range(num_uav)
    ]

def generate_materials(num_material: int = 10) -> List[Material]:
    """生成随机物资数据"""
    materials = []
    # 固定仓库起点（可选，也可随机）
    warehouse_pos = Point(x=500.0, y=500.0)
    for i in range(num_material):
        materials.append(Material(
            material_id=f"M{i+1:03d}",
            start_position=warehouse_pos,
            target_position=generate_random_point()
        ))
    return materials

def generate_all_random_data() -> AllData:
    """生成全量随机数据"""
    return AllData(
        map_data=generate_random_map(),
        unmanned_vehicles=generate_unmanned_vehicles(),
        uavs=generate_uavs(),
        materials=generate_materials()
    )

# ===================== 数据导出函数 =====================
def export_schema_and_data():
    """导出Schema JSON和多份随机数据JSON"""
    # 1. 导出数据结构Schema（JSON格式）
    schema = AllData.model_json_schema()
    with open("data_schema.json", "w", encoding="utf-8") as f:
        json.dump(schema, f, ensure_ascii=False, indent=4)
    
    # 2. 生成并导出3份随机数据（测试用）
    for i in range(3):
        random_data = generate_all_random_data()
        data_json = random_data.model_dump_json(indent=4, ensure_ascii=False)
        with open(f"random_data_{i+1}.json", "w", encoding="utf-8") as f:
            f.write(data_json)
    
    print("✅ 数据导出完成：")
    print("   - 数据结构Schema：data_schema.json")
    print("   - 随机测试数据：random_data_1.json / random_data_2.json / random_data_3.json")

# ===================== 执行生成与导出 =====================
if __name__ == "__main__":
    export_schema_and_data()
exit()
# 读取随机数据
with open("random_data_1.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 提取无人车数据
uvs = data["unmanned_vehicles"]
# 提取物资目标位置
material_targets = [m["target_position"] for m in data["materials"]]
# 提取可通行的道路边
valid_edges = [e for e in data["map_data"]["edges"] if not e["is_blocked"]]