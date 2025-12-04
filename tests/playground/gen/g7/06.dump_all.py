from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Set, Tuple
import json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from collections import defaultdict

# ===================== 1. 原始数据 Pydantic 模型（复用） =====================
def split_separator(v: str, sep: str = ';') -> List[str]:
    """将分隔符分隔的字符串转为列表"""
    return v.split(sep) if v else []

class LineFragment(BaseModel):
    c: List[str] = Field(..., description="分段轨迹像素坐标列表")
    li: str = Field(..., description="分段所属线路ID")

class MetroStationRaw(BaseModel):
    """原始站点模型（仅保留绘图必需字段）"""
    n: str = Field(..., description="站点中文名称")
    sl: str = Field(..., description="站点经纬度（经度,纬度）")
    t: str = Field(..., description="站点类型（0=普通站/1=换乘站）")

    @field_validator('sl')
    def parse_coordinate(cls, v: str) -> str:
        if not v:
            raise ValueError("经纬度不能为空")
        lon, lat = v.split(',')
        try:
            float(lon), float(lat)
        except ValueError:
            raise ValueError(f"无效的经纬度格式：{v}（正确格式：经度,纬度）")
        return v

    def get_lon_lat(self) -> Tuple[float, float]:
        """解析经纬度为浮点数元组"""
        lon, lat = self.sl.split(',')
        return float(lon), float(lat)

    def is_transfer(self) -> bool:
        """判断是否为换乘站"""
        return self.t == '1'

class MetroLineRaw(BaseModel):
    """原始线路模型（仅保留绘图必需字段）"""
    st: List[MetroStationRaw] = Field(..., description="线路下的站点列表")
    ln: str = Field(..., description="线路名称（如S1线）")

class BeijingMetroRaw(BaseModel):
    """原始地铁数据根模型"""
    l: List[MetroLineRaw] = Field(..., description="地铁线路列表")

    def get_all_lines(self) -> Dict[str, MetroLineRaw]:
        """按线路名称分组"""
        lines = {}
        for line in self.l:
            lines[line.ln] = line
        return lines

    def get_all_stations(self) -> Dict[str, Tuple[MetroStationRaw, Set[str]]]:
        """获取所有站点及所属线路"""
        station_map: Dict[str, Tuple[MetroStationRaw, Set[str]]] = defaultdict(lambda: (None, set()))
        for line in self.l:
            line_name = line.ln
            for station in line.st:
                st_name = station.n
                if station_map[st_name][0] is None:
                    station_map[st_name] = (station, {line_name})
                else:
                    station_map[st_name][1].add(line_name)
        return station_map

# ===================== 2. 精简绘图模型（仅保留核心字段） =====================
class DrawStation(BaseModel):
    """绘图用站点模型（核心字段）"""
    name: str = Field(..., description="站点名称")
    longitude: float = Field(..., description="站点经度")
    latitude: float = Field(..., description="站点纬度")
    is_transfer: bool = Field(..., description="是否为换乘站")
    belong_lines: List[str] = Field(..., description="所属线路列表")

class DrawLine(BaseModel):
    """绘图用线路模型（核心字段）"""
    line_name: str = Field(..., description="线路名称（如S1线）")
    color: str = Field(..., description="线路分配的16进制颜色码")
    stations: List[DrawStation] = Field(..., description="线路下的站点列表")

class MetroDrawSchema(BaseModel):
    """绘图用地铁数据根模型（最终要导出Schema的模型）"""
    lines: List[DrawLine] = Field(..., description="所有地铁线路（含颜色和站点）")
    all_stations: List[DrawStation] = Field(..., description="所有站点（去重，含换乘信息）")

# ===================== 3. 数据转换与文件保存函数 =====================
def read_raw_metro_json(file_path: str) -> BeijingMetroRaw:
    """读取原始JSON并解析为原始模型"""
    with open(file_path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
    return BeijingMetroRaw(**raw_data)

def generate_rainbow_colors(line_names: List[str]) -> Dict[str, str]:
    """生成彩虹渐变色（返回16进制颜色码）"""
    n_lines = len(line_names)
    # 定义彩虹色阶（可扩展）
    rainbow_colors = [
        "#FF0000", "#FF7F00", "#FFFF00", "#00FF00", 
        "#00FFFF", "#0000FF", "#8B00FF", "#FF00FF",
        "#990000", "#994C00", "#999900", "#009900",
        "#009999", "#000099", "#660099", "#990099"
    ]
    # 确保颜色数量足够
    if n_lines > len(rainbow_colors):
        rainbow_colors *= (n_lines // len(rainbow_colors) + 1)
    return {line_names[i]: rainbow_colors[i] for i in range(n_lines)}

def convert_raw_to_draw_model(raw_data: BeijingMetroRaw) -> MetroDrawSchema:
    """将原始模型转换为绘图精简模型"""
    # 1. 提取原始数据
    all_lines_raw = raw_data.get_all_lines()
    all_stations_raw = raw_data.get_all_stations()
    line_names = list(all_lines_raw.keys())

    # 2. 生成线路颜色
    line_colors = generate_rainbow_colors(line_names)

    # 3. 构建所有站点（去重，含换乘信息）
    all_draw_stations = []
    station_name_set = set()
    for st_name, (station_raw, line_set) in all_stations_raw.items():
        if st_name in station_name_set:
            continue
        station_name_set.add(st_name)
        lon, lat = station_raw.get_lon_lat()
        draw_station = DrawStation(
            name=st_name,
            longitude=lon,
            latitude=lat,
            is_transfer=station_raw.is_transfer() or len(line_set) > 1,
            belong_lines=list(line_set)
        )
        all_draw_stations.append(draw_station)

    # 4. 构建线路（含颜色和站点）
    draw_lines = []
    for line_name, line_raw in all_lines_raw.items():
        # 筛选当前线路的站点
        line_stations = []
        for st_raw in line_raw.st:
            for st_draw in all_draw_stations:
                if st_draw.name == st_raw.n:
                    line_stations.append(st_draw)
                    break
        draw_line = DrawLine(
            line_name=line_name,
            color=line_colors[line_name],
            stations=line_stations
        )
        draw_lines.append(draw_line)

    # 5. 返回精简模型
    return MetroDrawSchema(
        lines=draw_lines,
        all_stations=all_draw_stations
    )

def save_draw_schema(draw_model: MetroDrawSchema, output_path: str = "metro-draw-schema.json"):
    """生成并保存绘图模型的Schema元数据"""
    schema = draw_model.model_json_schema()
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(schema, f, ensure_ascii=False, indent=4)
    print(f"✅ Schema元数据已保存到：{output_path}")

def save_draw_data(draw_model: MetroDrawSchema, output_path: str = "metro-draw-data.json"):
    """保存绘图用的实际数据（与Schema匹配）"""
    # 将模型转换为字典并序列化为JSON
    draw_data = draw_model.model_dump(mode="json")  # mode="json" 确保类型兼容JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(draw_data, f, ensure_ascii=False, indent=4, sort_keys=False)
    print(f"✅ 绘图实际数据已保存到：{output_path}")

# ===================== 4. 主函数：执行转换与保存 =====================
if __name__ == "__main__":
    # 步骤1：读取原始JSON文件（替换为你的文件路径）
    import pathlib
    dir = pathlib.Path(__file__).parent
    raw_file_path = str(dir / "1100_drw_beijing.json")
    try:
        raw_metro_data = read_raw_metro_json(raw_file_path)
        print(f"✅ 成功读取原始数据，共{len(raw_metro_data.l)}条线路")
    except FileNotFoundError:
        print(f"❌ 错误：未找到文件 {raw_file_path}")
        exit(1)
    except Exception as e:
        print(f"❌ 原始数据解析错误：{e}")
        exit(1)

    # 步骤2：转换为绘图精简模型
    draw_model = convert_raw_to_draw_model(raw_metro_data)
    print(f"✅ 数据转换完成，精简模型包含：")
    print(f"   - 线路数：{len(draw_model.lines)}")
    print(f"   - 站点数：{len(draw_model.all_stations)}")

    # 步骤3：保存Schema元数据和实际绘图数据
    save_draw_schema(draw_model, "metro-draw-schema.json")
    save_draw_data(draw_model, "metro-draw-data.json")

    # 可选：验证保存的数据（读取并解析）
    print("\n📌 验证保存的数据：")
    with open("metro-draw-data.json", 'r', encoding='utf-8') as f:
        saved_data = json.load(f)
    # 用精简模型校验保存的数据
    validated_model = MetroDrawSchema(**saved_data)
    print(f"✅ 保存的数据校验通过，包含 {len(validated_model.lines)} 条线路")
    
    # 打印示例数据
    print("\n📌 示例数据（第一条线路）：")
    print(json.dumps(validated_model.lines[0].model_dump(), ensure_ascii=False, indent=2))