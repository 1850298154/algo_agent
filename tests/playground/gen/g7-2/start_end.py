import json
import random
from pydantic import BaseModel, Field
from typing import List


# 定义经纬度范围常量
LON_MIN, LON_MAX = 116.269956, 116.511821
LAT_MIN, LAT_MAX = 39.834910, 40.020430


class Point(BaseModel):
    """经纬度点模型"""
    longitude: float = Field(..., description="经度", ge=LON_MIN, le=LON_MAX)
    latitude: float = Field(..., description="纬度", ge=LAT_MIN, le=LAT_MAX)


class Route(BaseModel):
    """路线模型（包含起点和终点）"""
    start_point: Point = Field(..., description="起点经纬度")
    end_point: Point = Field(..., description="终点经纬度")


class RouteData(BaseModel):
    """批量路线数据模型"""
    total: int = Field(..., description="数据总数")
    area_info: dict = Field(..., description="区域信息")
    routes: List[Route] = Field(..., description="路线列表")


def generate_random_point() -> Point:
    """生成指定范围内的随机经纬度点"""
    lon = random.uniform(LON_MIN, LON_MAX)
    lat = random.uniform(LAT_MIN, LAT_MAX)
    # 保留6位小数，符合经纬度精度规范
    return Point(longitude=round(lon, 6), latitude=round(lat, 6))


def generate_route_data(n: int) -> RouteData:
    """生成n组起点终点数据"""
    area_info = {
        "longitude_range": [LON_MIN, LON_MAX],
        "latitude_range": [LAT_MIN, LAT_MAX],
        "area_km2": 423.96
    }
    
    routes = []
    for _ in range(n):
        start = generate_random_point()
        end = generate_random_point()
        routes.append(Route(start_point=start, end_point=end))
    
    return RouteData(
        total=n,
        area_info=area_info,
        routes=routes
    )


def save_json(data: dict, file_path: str):
    """保存数据到JSON文件"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    # 生成10个点（可修改n值）
    n = 10
    
    # 生成数据
    route_data = generate_route_data(n)
    
    # 1. 保存Pydantic Schema（JSON Schema格式）
    schema = RouteData.model_json_schema()
    save_json(schema, "route_schema.json")
    
    # 2. 保存生成的随机数据
    data = route_data.model_dump()
    save_json(data, "route_data.json")
    
    print(f"已生成{n}组起点终点数据")
    print(f"Schema文件: route_schema.json")
    print(f"数据文件: route_data.json")