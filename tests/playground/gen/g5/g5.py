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
    grid_row: int = Field(..., description="网格行号")
    grid_col: int = Field(..., description="网格列号")
    grid_value: float = Field(..., description="网格随机值（0-1），可代表通行难度/优先级等")

class Edge(BaseModel):
    """地图边（道路）模型"""
    start: Point = Field(..., description="边的起点坐标")
    end: Point = Field(..., description="边的终点坐标")
    is_blocked: bool = Field(default=False, description="道路是否阻断，True=阻断，False=通行")
    edge_type: str = Field(default="grid", description="边类型：grid=网格连通边")

class MapData(BaseModel):
    """车辆可行驶的地图数据模型"""
    points: List[Point] = Field(..., description="地图中所有坐标点列表（网格点）")
    edges: List[Edge] = Field(..., description="地图中所有道路边列表（网格连通边）")
    grid_config: Dict[str, int] = Field(..., description="网格配置：rows=行数, cols=列数, cell_size=单元格大小(米)")

class UAV(BaseModel):
    """无人机数据模型"""
    uav_id: str = Field(..., description="无人机唯一标识，如UAV001")
    load_capacity: int = Field(default=1, description="无人机运载容量，固定为1（单位：箱）")

class UnmannedVehicle(BaseModel):
    """无人车数据模型"""
    uv_id: str = Field(..., description="无人车唯一标识，如UV001")
    position: Point = Field(..., description="无人车当前位置坐标（网格点）")
    uav_capacity: int = Field(..., description="无人车可携带的无人机最大数量")

class Material(BaseModel):
    """物资数据模型"""
    material_id: str = Field(..., description="物资唯一标识，如M001")
    start_position: Point = Field(..., description="物资起点位置（仓库坐标，网格点）")
    target_position: Point = Field(..., description="物资目标位置（受灾点坐标，网格点）")

class AllData(BaseModel):
    """全量数据聚合模型"""
    map_data: MapData = Field(..., description="网格地图数据")
    unmanned_vehicles: List[UnmannedVehicle] = Field(..., description="所有无人车数据")
    uavs: List[UAV] = Field(..., description="所有无人机数据")
    materials: List[Material] = Field(..., description="所有物资数据")

# ===================== 网格地图生成函数 =====================
def generate_grid_point(row: int, col: int, cell_size: float) -> Point:
    """
    生成网格点坐标
    :param row: 网格行号
    :param col: 网格列号
    :param cell_size: 单元格大小（米）
    :return: 带网格属性的坐标点
    """
    # 计算网格中心点坐标
    x = col * cell_size + cell_size / 2
    y = row * cell_size + cell_size / 2
    # 网格随机值（0-1，可代表通行难度、优先级、受灾程度等）
    grid_value = round(random.uniform(0, 1), 3)
    
    return Point(
        x=round(x, 2),
        y=round(y, 2),
        grid_row=row,
        grid_col=col,
        grid_value=grid_value
    )

def generate_grid_map(
    rows: int = 10, 
    cols: int = 10, 
    cell_size: float = 100.0  # 每个单元格100米
) -> MapData:
    """
    生成规则化网格地图（上下左右连通）
    :param rows: 网格行数
    :param cols: 网格列数
    :param cell_size: 单元格大小（米）
    :return: 网格地图数据
    """
    # 1. 生成所有网格点
    grid_points = []
    for row in range(rows):
        for col in range(cols):
            grid_points.append(generate_grid_point(row, col, cell_size))
    
    # 2. 生成网格连通边（仅上下左右相邻）
    grid_edges = []
    point_map = {(p.grid_row, p.grid_col): p for p in grid_points}  # 行数列数映射到点
    
    # 生成水平边（左右相邻）
    for row in range(rows):
        for col in range(cols - 1):
            start = point_map[(row, col)]
            end = point_map[(row, col + 1)]
            # 15%概率道路阻断
            is_blocked = random.choice([True, False]) if random.random() < 0.15 else False
            grid_edges.append(Edge(
                start=start,
                end=end,
                is_blocked=is_blocked,
                edge_type="grid_horizontal"
            ))
    
    # 生成垂直边（上下相邻）
    for col in range(cols):
        for row in range(rows - 1):
            start = point_map[(row, col)]
            end = point_map[(row + 1, col)]
            # 15%概率道路阻断
            is_blocked = random.choice([True, False]) if random.random() < 0.15 else False
            grid_edges.append(Edge(
                start=start,
                end=end,
                is_blocked=is_blocked,
                edge_type="grid_vertical"
            ))
    
    # 3. 构建地图数据
    return MapData(
        points=grid_points,
        edges=grid_edges,
        grid_config={
            "rows": rows,
            "cols": cols,
            "cell_size": int(cell_size)
        }
    )

# ===================== 其他数据生成函数（适配网格） =====================
def generate_unmanned_vehicles(num_uv: int = 3, grid_rows: int = 10, grid_cols: int = 10, cell_size: float = 100.0) -> List[UnmannedVehicle]:
    """生成随机无人车数据（位置在网格点上）"""
    uvs = []
    for i in range(num_uv):
        # 随机选择网格位置
        row = random.randint(0, grid_rows - 1)
        col = random.randint(0, grid_cols - 1)
        position = generate_grid_point(row, col, cell_size)
        
        uvs.append(UnmannedVehicle(
            uv_id=f"UV{i+1:03d}",
            position=position,
            uav_capacity=random.randint(1, 3)  # 每车可带1-3架无人机
        ))
    return uvs

def generate_uavs(num_uav: int = 8) -> List[UAV]:
    """生成随机无人机数据（运载容量固定为1）"""
    return [
        UAV(uav_id=f"UAV{i+1:03d}", load_capacity=1)
        for i in range(num_uav)
    ]

def generate_materials(num_material: int = 10, grid_rows: int = 10, grid_cols: int = 10, cell_size: float = 100.0) -> List[Material]:
    """生成随机物资数据（起点和终点都在网格点上）"""
    materials = []
    # 固定仓库位置（网格中心）
    warehouse_row = grid_rows // 2
    warehouse_col = grid_cols // 2
    warehouse_pos = generate_grid_point(warehouse_row, warehouse_col, cell_size)
    
    for i in range(num_material):
        # 随机受灾点位置
        target_row = random.randint(0, grid_rows - 1)
        target_col = random.randint(0, grid_cols - 1)
        target_pos = generate_grid_point(target_row, target_col, cell_size)
        
        materials.append(Material(
            material_id=f"M{i+1:03d}",
            start_position=warehouse_pos,
            target_position=target_pos
        ))
    return materials

def generate_all_random_data(
    grid_rows: int = 10,
    grid_cols: int = 10,
    cell_size: float = 100.0,
    num_uv: int = 3,
    num_uav: int = 8,
    num_material: int = 10
) -> AllData:
    """生成全量随机数据（网格版）"""
    # 生成网格地图
    map_data = generate_grid_map(rows=grid_rows, cols=grid_cols, cell_size=cell_size)
    
    # 生成其他数据（适配网格）
    unmanned_vehicles = generate_unmanned_vehicles(
        num_uv=num_uv,
        grid_rows=grid_rows,
        grid_cols=grid_cols,
        cell_size=cell_size
    )
    
    uavs = generate_uavs(num_uav=num_uav)
    
    materials = generate_materials(
        num_material=num_material,
        grid_rows=grid_rows,
        grid_cols=grid_cols,
        cell_size=cell_size
    )
    
    return AllData(
        map_data=map_data,
        unmanned_vehicles=unmanned_vehicles,
        uavs=uavs,
        materials=materials
    )

# ===================== 数据导出函数 =====================
def export_schema_and_data():
    """导出Schema JSON和多份随机数据JSON"""
    # 1. 导出数据结构Schema（JSON格式）
    schema = AllData.model_json_schema()
    with open("grid_data_schema.json", "w", encoding="utf-8") as f:
        json.dump(schema, f, ensure_ascii=False, indent=4)
    
    # 2. 生成并导出3份随机网格数据（测试用）
    for i in range(3):
        # 可调整网格大小（示例：10x10网格，每个单元格100米）
        random_data = generate_all_random_data(
            grid_rows=10,
            grid_cols=10,
            cell_size=100.0,
            num_uv=3,
            num_uav=8,
            num_material=10
        )
        data_json = random_data.model_dump_json(indent=4, ensure_ascii=False)
        with open(f"grid_random_data_{i+1}.json", "w", encoding="utf-8") as f:
            f.write(data_json)
    
    print("✅ 网格数据导出完成：")
    print("   - 数据结构Schema：grid_data_schema.json")
    print("   - 随机测试数据：grid_random_data_1.json / grid_random_data_2.json / grid_random_data_3.json")

# ===================== 执行生成与导出 =====================
if __name__ == "__main__":
    export_schema_and_data()