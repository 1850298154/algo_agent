from pydantic import BaseModel, Field
from typing import List, Dict, Tuple, Optional
import json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
import math

# ===================== 1. 精简模型定义（与Schema一致） =====================
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
    """绘图用地铁数据根模型"""
    lines: List[DrawLine] = Field(..., description="所有地铁线路（含颜色和站点）")
    all_stations: List[DrawStation] = Field(..., description="所有站点（去重，含换乘信息）")

# ===================== 2. 数据读取函数 =====================
def read_json_file(file_path: str) -> dict:
    """读取JSON文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"文件 {file_path} 不存在")
    except json.JSONDecodeError:
        raise ValueError(f"文件 {file_path} 不是有效的JSON格式")

def load_metro_draw_data(schema_path: str, data_path: str) -> MetroDrawSchema:
    """
    加载精简的地铁Schema和Data文件
    :param schema_path: Schema文件路径
    :param data_path: Data文件路径
    :return: 校验后的MetroDrawSchema模型
    """
    # 读取Schema（仅验证结构，实际使用Data）
    read_json_file(schema_path)
    # 读取Data并校验
    data = read_json_file(data_path)
    return MetroDrawSchema(**data)

# ===================== 3. 经纬度分析函数 =====================
class GeoAnalysisResult:
    """经纬度分析结果容器"""
    def __init__(self):
        self.lon_min: float = 0.0
        self.lon_max: float = 0.0
        self.lat_min: float = 0.0
        self.lat_max: float = 0.0
        self.lon_median: float = 0.0
        self.lat_median: float = 0.0
        self.percentile_ranges: Dict[int, Dict[str, float]] = {}  # {百分比: {lon_min, lon_max, lat_min, lat_max, area}}

def calculate_geo_bounds(stations: List[DrawStation], percentiles: List[int] = [100,90,80,70,60,50,40,30]) -> GeoAnalysisResult:
    """
    计算站点经纬度的分布特征和不同百分比的最小包围矩形
    :param stations: 所有站点列表
    :param percentiles: 要计算的百分比列表
    :return: 分析结果
    """
    # 提取经纬度数组
    lons = np.array([station.longitude for station in stations])
    lats = np.array([station.latitude for station in stations])
    
    # 基础统计
    result = GeoAnalysisResult()
    result.lon_min = np.min(lons)
    result.lon_max = np.max(lons)
    result.lat_min = np.min(lats)
    result.lat_max = np.max(lats)
    result.lon_median = np.median(lons)
    result.lat_median = np.median(lats)
    
    # 计算不同百分比的包围矩形
    for p in percentiles:
        if p < 0 or p > 100:
            continue
        
        if p == 100:
            # 100%：全部数据
            lon_p_min = result.lon_min
            lon_p_max = result.lon_max
            lat_p_min = result.lat_min
            lat_p_max = result.lat_max
        else:
            # 计算分位数范围（保留中间p%的数据）
            exclude_p = (100 - p) / 2
            lon_p_min = np.percentile(lons, exclude_p)
            lon_p_max = np.percentile(lons, 100 - exclude_p)
            lat_p_min = np.percentile(lats, exclude_p)
            lat_p_max = np.percentile(lats, 100 - exclude_p)
        
        # 计算包围面积（近似，假设经纬度1度≈111km）
        lon_range = lon_p_max - lon_p_min
        lat_range = lat_p_max - lat_p_min
        # 经纬度面积转换：1度经度 = 111km * cos(纬度)，纬度=111km
        avg_lat = (lat_p_min + lat_p_max) / 2
        area_km2 = (lon_range * 111 * math.cos(math.radians(avg_lat))) * (lat_range * 111)
        
        result.percentile_ranges[p] = {
            "lon_min": lon_p_min,
            "lon_max": lon_p_max,
            "lat_min": lat_p_min,
            "lat_max": lat_p_max,
            "area_km2": area_km2,
            "lon_range": lon_range,
            "lat_range": lat_range
        }
    
    return result

def filter_stations_by_bounds(stations: List[DrawStation], lon_min: float, lon_max: float, lat_min: float, lat_max: float) -> List[DrawStation]:
    """
    过滤出包围矩形内的站点
    :param stations: 原始站点列表
    :param lon_min/lon_max: 经度范围
    :param lat_min/lat_max: 纬度范围
    :return: 过滤后的站点列表
    """
    filtered = []
    for station in stations:
        if (lon_min <= station.longitude <= lon_max) and (lat_min <= station.latitude <= lat_max):
            filtered.append(station)
    return filtered

def filter_lines_by_stations(original_lines: List[DrawLine], filtered_stations: List[DrawStation]) -> List[DrawLine]:
    """
    根据过滤后的站点更新线路数据（仅保留存在的站点）
    :param original_lines: 原始线路列表
    :param filtered_stations: 过滤后的站点列表
    :return: 过滤后的线路列表
    """
    # 构建站点名称映射
    station_names = {s.name for s in filtered_stations}
    station_map = {s.name: s for s in filtered_stations}
    
    filtered_lines = []
    for line in original_lines:
        # 过滤线路内的站点
        line_stations = [station_map[s.name] for s in line.stations if s.name in station_names]
        if line_stations:  # 仅保留有站点的线路
            filtered_line = DrawLine(
                line_name=line.line_name,
                color=line.color,
                stations=line_stations
            )
            filtered_lines.append(filtered_line)
    
    return filtered_lines

def save_filtered_data(filtered_model: MetroDrawSchema, percentile: int, output_dir: str = "./"):
    """保存过滤后的数据文件"""
    output_path = f"{output_dir}/metro-draw-data-{percentile}%.json"
    filtered_data = filtered_model.model_dump(mode="json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, ensure_ascii=False, indent=4)
    print(f"✅ 过滤后的数据（{percentile}%）已保存到：{output_path}")

# ===================== 4. 绘图函数 =====================
def plot_metro_map(metro_data: MetroDrawSchema, geo_result: GeoAnalysisResult, figsize: Tuple[int, int] = (16, 12), dpi: int = 100):
    """
    绘制地铁图（含经纬度包围矩形标注）
    :param metro_data: 地铁数据模型
    :param geo_result: 经纬度分析结果
    :param figsize: 画布大小
    :param dpi: 分辨率
    """
    # 设置中文显示
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 创建画布
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize, dpi=dpi)
    fig.suptitle("北京地铁分析（左：线路图 | 右：经纬度分布）", fontsize=16, fontweight='bold')
    
    # ========== 左图：地铁线路和站点 ==========
    ax1.set_title("地铁线路与站点分布图", fontsize=12)
    ax1.set_xlabel("经度")
    ax1.set_ylabel("纬度")
    ax1.grid(True, alpha=0.3)
    
    # 绘制线路
    for line in metro_data.lines:
        lons = [s.longitude for s in line.stations]
        lats = [s.latitude for s in line.stations]
        ax1.plot(lons, lats, color=line.color, linewidth=3, label=line.line_name, alpha=0.8)
    
    # 绘制站点
    for station in metro_data.all_stations:
        marker = 'o'
        size = 80 if station.is_transfer else 40
        color = 'red' if station.is_transfer else 'blue'
        ax1.scatter(station.longitude, station.latitude, color=color, s=size, 
                    alpha=0.8, edgecolors='black', zorder=5)
        # 标注换乘站名称
        if station.is_transfer:
            ax1.annotate(station.name, (station.longitude, station.latitude), 
                        xytext=(5, 5), textcoords='offset points', fontsize=8,
                        bbox=dict(boxstyle='round,pad=0.2', facecolor='yellow', alpha=0.7))
    
    # 添加图例
    ax1.legend(title="线路", bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    
    # ========== 右图：经纬度分布 + 包围矩形 ==========
    ax2.set_title("经纬度分布与包围矩形", fontsize=12)
    ax2.set_xlabel("经度")
    ax2.set_ylabel("纬度")
    ax2.grid(True, alpha=0.3)
    
    # 绘制所有站点散点
    lons_all = [s.longitude for s in metro_data.all_stations]
    lats_all = [s.latitude for s in metro_data.all_stations]
    ax2.scatter(lons_all, lats_all, color='blue', alpha=0.6, s=20, label='所有站点')
    
    for p in geo_result.percentile_ranges.keys():
        # 绘制p%包围矩形
        rect_p = Rectangle(
            (geo_result.percentile_ranges[p]['lon_min'], geo_result.percentile_ranges[p]['lat_min']),
            geo_result.percentile_ranges[p]['lon_range'],
            geo_result.percentile_ranges[p]['lat_range'],
            linewidth=2, edgecolor='red', facecolor='none', label=f'{p}% 包围矩形'
        )
        ax2.add_patch(rect_p)
    
    ax2.legend(fontsize=10)
    
    # 调整布局
    plt.tight_layout()
    plt.show()

# ===================== 5. 主函数 =====================
def main():
    # 配置文件路径
    import pathlib
    dir = pathlib.Path(__file__).parent
    SCHEMA_PATH = dir / "metro-draw-schema.json"
    DATA_PATH = dir / "100" / "metro-draw-data-90%.json"
    DATA_PATH = dir / "metro-draw-data.json"
    PERCENTILES = [100, 90, 80, 70, 60, 50, 40, 30]
    
    try:
        # 步骤1：加载精简数据
        print("🔍 加载精简地铁数据...")
        metro_data = load_metro_draw_data(SCHEMA_PATH, DATA_PATH)
        print(f"✅ 加载完成：{len(metro_data.lines)} 条线路，{len(metro_data.all_stations)} 个站点")
        
        # 步骤2：经纬度分布分析
        print("\n📊 开始经纬度分布分析...")
        geo_result = calculate_geo_bounds(metro_data.all_stations, PERCENTILES)
        
        # 打印分析结果
        print("\n=== 经纬度基础统计 ===")
        print(f"经度范围：{geo_result.lon_min:.6f} ~ {geo_result.lon_max:.6f}")
        print(f"纬度范围：{geo_result.lat_min:.6f} ~ {geo_result.lat_max:.6f}")
        print(f"经度中位数：{geo_result.lon_median:.6f}")
        print(f"纬度中位数：{geo_result.lat_median:.6f}")
        
        print("\n=== 不同百分比包围矩形分析 ===")
        print(f"{'百分比':<6} {'经度范围':<25} {'纬度范围':<25} {'面积(km²)':<10}")
        print("-" * 80)
        for p in PERCENTILES:
            r = geo_result.percentile_ranges[p]
            lon_range_str = f"{r['lon_min']:.6f} ~ {r['lon_max']:.6f}"
            lat_range_str = f"{r['lat_min']:.6f} ~ {r['lat_max']:.6f}"
            area_str = f"{r['area_km2']:.2f}"
            print(f"{p}%      {lon_range_str:<25} {lat_range_str:<25} {area_str:<10}")
        
        # 步骤3：绘制地铁图
        print("\n🎨 绘制地铁分析图...")
        plot_metro_map(metro_data, geo_result)
        
        # 步骤4：按不同百分比过滤数据并保存
        print("\n🗂️ 过滤并保存不同百分比的数据...")
        for p in PERCENTILES:
            bounds = geo_result.percentile_ranges[p]
            # 过滤站点
            filtered_stations = filter_stations_by_bounds(
                metro_data.all_stations,
                bounds['lon_min'], bounds['lon_max'],
                bounds['lat_min'], bounds['lat_max']
            )
            # 过滤线路
            filtered_lines = filter_lines_by_stations(metro_data.lines, filtered_stations)
            # 构建过滤后的模型
            filtered_model = MetroDrawSchema(
                lines=filtered_lines,
                all_stations=filtered_stations
            )
            # 保存文件
            save_filtered_data(filtered_model, p)
            print(f"   - {p}%：保留 {len(filtered_stations)} 个站点，{len(filtered_lines)} 条线路")
        
        print("\n🎉 所有分析和数据处理完成！")
        
    except Exception as e:
        print(f"❌ 执行出错：{str(e)}")
        raise

if __name__ == "__main__":
    main()