from pydantic import BaseModel, Field
from typing import List, Optional
import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

# ===================== 1. 原有Pydantic模型（复用） =====================
class DrwStation(BaseModel):
    """地铁绘制数据-站点模型"""
    rs: Optional[str] = Field(None, description="路由段ID，多值用|分隔")
    udpx: Optional[str] = Field(None, description="上下行站点X坐标，多值用;分隔")
    su: Optional[str] = Field(None, description="站点使用状态，1=启用，0=停用")
    udsu: Optional[str] = Field(None, description="上下行站点使用状态，多值用;分隔")
    en: Optional[str] = Field(None, description="站点英文名称")
    n: str = Field(..., description="站点名称")
    sid: str = Field(..., description="站点唯一ID")
    p: Optional[str] = Field(None, description="站点核心坐标（X Y格式）")
    r: Optional[str] = Field(..., description="关联路由ID，多值用|分隔")  # 改为必填（连线依赖）
    udsi: Optional[str] = Field(None, description="上下行站点ID，多值用;分隔")
    t: Optional[str] = Field(None, description="站点类型，1=普通站，2=换乘站等")
    si: str = Field(..., description="站点内部统一ID")
    sl: Optional[str] = Field(..., description="站点经纬度，格式：经度,纬度")
    udli: Optional[str] = Field(None, description="上下行线路ID，多值用;分隔")
    poiid: Optional[str] = Field(None, description="站点关联POI ID")
    lg: Optional[str] = Field(None, description="逻辑标识，0=正常，1=特殊")
    sp: Optional[str] = Field(None, description="站点拼音名称")

class DrwLine(BaseModel):
    """地铁绘制数据-线路模型"""
    st: List[DrwStation] = Field(..., description="线路下的站点列表")

class DrwSubwayData(BaseModel):
    """地铁绘制数据-根模型"""
    s: str = Field(..., description="数据主题名称（如北京市地铁）")
    i: str = Field(..., description="区域ID（北京市行政区划代码1100）")
    l: List[DrwLine] = Field(..., description="地铁线路列表")

class InfoDirection(BaseModel):
    """地铁信息数据-站点方向调度模型"""
    ls: str = Field(..., description="线路-站点关联ID")
    lt: Optional[str] = Field(None, description="站点发车时间，--:--=未配置")
    n: str = Field(..., description="站点唯一标识")
    ft: Optional[str] = Field(None, description="站点到达时间，--:--=未配置")

class InfoStation(BaseModel):
    """地铁信息数据-站点模型"""
    ac: str = Field(..., description="区域编码（如110000=北京市）")
    d: List[InfoDirection] = Field(..., description="站点多方向调度信息列表")
    si: str = Field(..., description="站点内部统一ID")

class InfoLine(BaseModel):
    """地铁信息数据-线路模型"""
    a: str = Field(..., description="区域ID（冗余字段，同根节点i）")
    st: List[InfoStation] = Field(..., description="线路下的站点信息列表")

class InfoSubwayData(BaseModel):
    """地铁信息数据-根模型"""
    i: str = Field(..., description="区域ID（北京市行政区划代码1100）")
    l: List[InfoLine] = Field(..., description="地铁线路信息列表")

# ===================== 2. 原有文件读取函数（复用） =====================
def read_drw_subway_data(file_path: str) -> DrwSubwayData:
    """读取1100_drw_beijing.json文件并解析为Pydantic模型"""
    file = Path(file_path)
    if not file.exists():
        raise FileNotFoundError(f"文件不存在：{file_path}")
    with open(file, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
    return DrwSubwayData(**raw_data)

def read_info_subway_data(file_path: str) -> InfoSubwayData:
    """读取1100_info_beijing.json文件并解析为Pydantic模型"""
    file = Path(file_path)
    if not file.exists():
        raise FileNotFoundError(f"文件不存在：{file_path}")
    with open(file, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
    return InfoSubwayData(**raw_data)

# ===================== 3. 新增可视化工具函数 =====================
def parse_lon_lat(sl_str: Optional[str]) -> tuple[float, float] | None:
    """
    解析站点经纬度字符串（格式：经度,纬度）
    Args:
        sl_str: 经纬度字符串，如"116.178945,39.925686"
    Returns:
        (经度, 纬度) 或 None（解析失败）
    """
    if not sl_str:
        return None
    try:
        lon, lat = sl_str.split(",")
        return float(lon), float(lat)
    except (ValueError, AttributeError):
        return None

def get_route_station_mapping(drw_data: DrwSubwayData) -> dict[str, list[DrwStation]]:
    """
    构建「路由ID -> 站点列表」映射（用于绘制线路连线）
    路由ID是线路分段的核心标识，同一路由下的站点按顺序连线
    """
    route_mapping = defaultdict(list)
    for line in drw_data.l:
        for station in line.st:
            # 拆分多路由ID（如"900000069871|110100023339"）
            route_ids = station.r.split("|")
            for rid in route_ids:
                rid = rid.strip()
                if rid and station.sl:  # 有路由ID且有经纬度才加入
                    route_mapping[rid].append(station)
    return route_mapping

def plot_subway_network(drw_data: DrwSubwayData, figsize: tuple[int, int] = (12, 10)):
    """
    绘制地铁网络：节点（站点）+ 连线（线路）
    Args:
        drw_data: 解析后的地铁绘制数据
        figsize: 画布尺寸
    """
    # 1. 初始化画布
    plt.rcParams["font.sans-serif"] = ["SimHei"]  # 支持中文
    plt.rcParams["axes.unicode_minus"] = False    # 支持负号
    fig, ax = plt.subplots(figsize=figsize)
    
    # 2. 构建路由-站点映射
    route_mapping = get_route_station_mapping(drw_data)
    # 预定义线路配色（可扩展）
    colors = plt.cm.tab10(np.linspace(0, 1, len(route_mapping)))
    
    # 3. 绘制线路连线（先画连线，后画节点，避免节点被遮挡）
    route_color_map = {}  # 路由ID -> 颜色
    for idx, (route_id, stations) in enumerate(route_mapping.items()):
        # 过滤无经纬度的站点
        valid_stations = [s for s in stations if parse_lon_lat(s.sl)]
        if len(valid_stations) < 2:
            continue  # 至少2个站点才连线
        
        # 分配颜色
        route_color_map[route_id] = colors[idx % len(colors)]
        
        # 提取经纬度序列
        lons = [parse_lon_lat(s.sl)[0] for s in valid_stations]
        lats = [parse_lon_lat(s.sl)[1] for s in valid_stations]
        
        # 绘制连线
        ax.plot(
            lons, lats,
            color=route_color_map[route_id],
            linewidth=2,
            alpha=0.7,
            label=f"线路段 {route_id[:8]}..."  # 路由ID过长，截断显示
        )
    
    # 4. 绘制站点节点
    all_stations = []
    for line in drw_data.l:
        all_stations.extend(line.st)
    
    # 区分换乘站（t=2）和普通站（t=1）
    transfer_stations = [s for s in all_stations if s.t == "2" and parse_lon_lat(s.sl)]
    normal_stations = [s for s in all_stations if s.t == "1" and parse_lon_lat(s.sl)]
    
    # 绘制普通站
    if normal_stations:
        lon_norm = [parse_lon_lat(s.sl)[0] for s in normal_stations]
        lat_norm = [parse_lon_lat(s.sl)[1] for s in normal_stations]
        ax.scatter(
            lon_norm, lat_norm,
            s=50,  # 点大小
            c="white",
            edgecolors="gray",
            linewidths=1.5,
            alpha=0.8,
            label="普通站点"
        )
    
    # 绘制换乘站（更大、更醒目）
    if transfer_stations:
        lon_trans = [parse_lon_lat(s.sl)[0] for s in transfer_stations]
        lat_trans = [parse_lon_lat(s.sl)[1] for s in transfer_stations]
        ax.scatter(
            lon_trans, lat_trans,
            s=100,  # 点大小
            c="red",
            edgecolors="darkred",
            linewidths=2,
            alpha=0.9,
            label="换乘站点"
        )
    
    # 5. 标注关键站点（可选：仅标注换乘站，避免文字重叠）
    for station in transfer_stations[:10]:  # 限制标注数量，避免拥挤
        lon, lat = parse_lon_lat(station.sl)
        ax.annotate(
            station.n,
            xy=(lon, lat),
            xytext=(5, 5),  # 文字偏移
            textcoords="offset points",
            fontsize=8,
            bbox=dict(boxstyle="round,pad=0.2", fc="yellow", alpha=0.5)
        )
    
    # 6. 图表美化
    ax.set_title(drw_data.s + " 地铁网络", fontsize=16, fontweight="bold")
    ax.set_xlabel("经度", fontsize=12)
    ax.set_ylabel("纬度", fontsize=12)
    ax.grid(True, alpha=0.3)
    # 图例（仅显示前10个线路段，避免过多）
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[:10] + handles[-2:], labels[:10] + labels[-2:], loc="best", fontsize=8)
    # 调整坐标轴范围（适配数据）
    all_lons = [parse_lon_lat(s.sl)[0] for s in all_stations if parse_lon_lat(s.sl)]
    all_lats = [parse_lon_lat(s.sl)[1] for s in all_stations if parse_lon_lat(s.sl)]
    if all_lons and all_lats:
        ax.set_xlim(min(all_lons) - 0.05, max(all_lons) + 0.05)
        ax.set_ylim(min(all_lats) - 0.05, max(all_lats) + 0.05)
    
    # 7. 显示/保存图片
    plt.tight_layout()
    plt.savefig("subway_network.png", dpi=300, bbox_inches="tight")  # 保存高清图片
    plt.show()

# ===================== 4. 主函数（调用示例） =====================
if __name__ == "__main__":
    path = Path(__file__).parent
    # 1. 读取数据
    try:
        drw_file_path = path / "1100_drw_beijing.json"  # 替换为你的文件路径
        drw_data = read_drw_subway_data(drw_file_path)
        print(f"成功读取数据：{drw_data.s}，共{len(drw_data.l)}条线路")
    except Exception as e:
        print(f"读取数据失败：{e}")
        exit(1)
    
    # 2. 绘制地铁网络
    try:
        plot_subway_network(drw_data)
        print("地铁网络绘制完成，已保存为 subway_network.png")
    except Exception as e:
        print(f"绘制失败：{e}")