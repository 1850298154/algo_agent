from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Set
import json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from collections import defaultdict

# ===================== 复用之前的 Pydantic 模型 =====================
def split_separator(v: str, sep: str = ';') -> List[str]:
    """将分隔符分隔的字符串转为列表"""
    return v.split(sep) if v else []

class LineFragment(BaseModel):
    """地铁线路分段（如上下行分段）"""
    c: List[str] = Field(..., description="分段轨迹像素坐标列表")
    li: str = Field(..., description="分段所属线路ID")

class MetroStation(BaseModel):
    """地铁站点信息"""
    rs: Optional[str] = Field(default="", description="路由段编码（竖线分隔多段）")
    udpx: Optional[str] = Field(default="", description="上下行像素坐标（分号分隔）")
    su: str = Field(..., description="站点状态（1=启用）")
    udsu: Optional[str] = Field(default="", description="上下行状态（分号分隔）")
    en: Optional[str] = Field(default="", description="站点英文名称")
    n: str = Field(..., description="站点中文名称")
    sid: str = Field(..., description="站点唯一ID（高德内部编码）")
    p: Optional[str] = Field(default="", description="站点像素坐标")
    r: Optional[str] = Field(default="", description="路由ID（竖线分隔多ID）")
    udsi: Optional[str] = Field(default="", description="上下行站点ID（分号分隔）")
    t: str = Field(..., description="站点类型（0=普通站/1=换乘站）")
    si: str = Field(..., description="站点ID（与sid一致）")
    sl: str = Field(..., description="站点经纬度（经度,纬度）")
    udli: Optional[str] = Field(default="", description="上下行线路ID（分号分隔）")
    poiid: Optional[str] = Field(default="", description="高德POI唯一ID")
    lg: Optional[str] = Field(default="", description="逻辑分组/层级")
    sp: Optional[str] = Field(default="", description="站点拼音")

    @field_validator('sl')
    def parse_coordinate(cls, v: str) -> str:
        """校验经纬度格式（经度,纬度）"""
        if not v:
            raise ValueError("经纬度不能为空")
        lon, lat = v.split(',')
        try:
            float(lon), float(lat)
        except ValueError:
            raise ValueError(f"无效的经纬度格式：{v}（正确格式：经度,纬度）")
        return v

    def get_lon_lat(self) -> tuple[float, float]:
        """解析经纬度为浮点数元组 (经度, 纬度)"""
        lon, lat = self.sl.split(',')
        return float(lon), float(lat)

    def is_transfer(self) -> bool:
        """判断是否为换乘站"""
        return self.t == '1'

class MetroLine(BaseModel):
    """地铁线路信息"""
    st: List[MetroStation] = Field(..., description="线路下的站点列表")
    ln: str = Field(..., description="线路名称（如S1线）")
    su: str = Field(..., description="线路状态（1=启用）")
    kn: str = Field(..., description="线路常用名称（如地铁1号线(八通线)）")
    c: Optional[List[str]] = Field(default=[], description="线路轨迹像素坐标列表")
    lo: Optional[str] = Field(default="0", description="图层渲染顺序")
    lp: Optional[List[str]] = Field(default=[], description="线路像素范围列表")
    ek: Optional[str] = Field(default="", description="线路英文标识键")
    f: Optional[List[LineFragment]] = Field(default=[], description="线路分段数组")
    ls: str = Field(..., description="线路源ID")
    el: Optional[str] = Field(default="", description="线路英文名称")
    cl: str = Field(..., description="线路颜色（16进制码）")
    la: Optional[str] = Field(default="", description="语言标识")
    x: Optional[int] = Field(default=0, description="线路排序索引")
    ea: Optional[str] = Field(default="", description="线路英文别名")
    li: str = Field(..., description="线路ID（竖线分隔多ID）")

    def get_station_coords(self) -> list[tuple[float, float]]:
        """获取线路所有站点的经纬度列表 [(经度, 纬度), ...]"""
        return [station.get_lon_lat() for station in self.st]

class BeijingMetroDrawData(BaseModel):
    """高德地铁绘制数据（1100_drw_beijing.json）"""
    s: str = Field(..., description="数据主题（如北京市地铁）")
    i: str = Field(..., description="区域编码（1100=北京）")
    l: List[MetroLine] = Field(..., description="地铁线路列表")
    o: Optional[str] = Field(default="", description="可视化画布原点（宽,高）")

    def get_all_lines(self) -> Dict[str, MetroLine]:
        """按线路名称（ln）分组，返回 {线路名: 线路对象}"""
        lines = {}
        for line in self.l:
            lines[line.ln] = line
        return lines

    def get_all_stations(self) -> Dict[str, tuple[MetroStation, Set[str]]]:
        """
        获取所有站点，标注所属线路
        返回：{站点名称: (站点对象, {所属线路名1, 所属线路名2...})}
        """
        station_map: Dict[str, tuple[MetroStation, Set[str]]] = defaultdict(lambda: (None, set()))
        for line in self.l:
            line_name = line.ln
            for station in line.st:
                st_name = station.n
                if station_map[st_name][0] is None:
                    station_map[st_name] = (station, {line_name})
                else:
                    station_map[st_name][1].add(line_name)
        return station_map

def read_metro_drw_json(file_path: str) -> BeijingMetroDrawData:
    """读取高德地铁绘制JSON文件并校验数据"""
    with open(file_path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
    return BeijingMetroDrawData(**raw_data)

# ===================== 绘图核心函数 =====================
def plot_beijing_metro(metro_data: BeijingMetroDrawData, figsize: tuple = (16, 12), dpi: int = 100):
    """
    绘制北京地铁线路与站点图
    :param metro_data: 解析后的地铁数据模型
    :param figsize: 画布大小
    :param dpi: 分辨率
    """
    # 1. 准备数据
    all_lines = metro_data.get_all_lines()  # 所有线路 {线路名: 线路对象}
    all_stations = metro_data.get_all_stations()  # 所有站点 {站名: (站点对象, 所属线路集合)}
    line_names = list(all_lines.keys())  # 线路名称列表

    # 2. 生成彩虹渐变色（确保颜色不重复）
    # 生成N个不同的彩虹色（N为线路数）
    n_lines = len(line_names)
    rainbow_cmap = LinearSegmentedColormap.from_list('custom_rainbow', 
                                                     ['#FF0000', '#FF7F00', '#FFFF00', '#00FF00', '#00FFFF', '#0000FF', '#8B00FF'],
                                                     N=n_lines)
    line_colors = {line_names[i]: rainbow_cmap(i) for i in range(n_lines)}

    # 3. 创建画布
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    ax.set_title("北京地铁线路与站点分布图", fontsize=20, fontweight='bold', pad=20)
    ax.set_xlabel("经度", fontsize=12)
    ax.set_ylabel("纬度", fontsize=12)
    ax.grid(True, alpha=0.3)

    # 4. 绘制地铁线路
    for line_name, line in all_lines.items():
        # 获取线路站点的经纬度
        coords = line.get_station_coords()
        if not coords:
            continue
        lons = [c[0] for c in coords]
        lats = [c[1] for c in coords]
        
        # 绘制线路（加粗，渐变颜色）
        ax.plot(lons, lats, color=line_colors[line_name], linewidth=3, 
                label=line_name, alpha=0.8)

    # 5. 绘制站点（区分换乘站和普通站）
    for st_name, (station, line_set) in all_stations.items():
        lon, lat = station.get_lon_lat()
        is_transfer = station.is_transfer() or len(line_set) > 1

        # 换乘站：红色大圆点，普通站：蓝色小圆点
        if is_transfer:
            ax.scatter(lon, lat, color='red', s=100, alpha=0.9, edgecolors='black', zorder=5)
            # 换乘站标注（所属线路）
            transfer_label = f"{st_name}\n({','.join(line_set)})"
            transfer_label = ""
            ax.annotate(transfer_label, (lon, lat), xytext=(5, 5), textcoords='offset points',
                        fontsize=8, bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
                        zorder=6)
        else:
            ax.scatter(lon, lat, color='blue', s=50, alpha=0.7, edgecolors='gray', zorder=4)
            # 普通站标注（仅站名）
            ax.annotate(st_name, (lon, lat), xytext=(3, 3), textcoords='offset points',
                        fontsize=7, alpha=0.8, zorder=5)

    # 6. 设置图例（颜色对应线路名称）
    legend = ax.legend(title="地铁线路", title_fontsize=12, fontsize=10, 
                       loc='upper right', bbox_to_anchor=(1.2, 1))
    plt.setp(legend.get_texts(), fontsize=9)

    # 7. 调整布局，避免标签重叠
    plt.tight_layout()

    # 8. 显示/保存图片
    plt.show()
    # 可选：保存图片
    # fig.savefig("beijing_metro_map.png", dpi=150, bbox_inches='tight')


import platform
system = platform.system()
if system == "Windows":
    plt.rcParams['font.sans-serif'] = ['SimHei']
elif system == "Darwin":  # Mac
    plt.rcParams['font.sans-serif'] = ['PingFang SC']
else:  # Linux
    plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei']
plt.rcParams['axes.unicode_minus'] = False
# ===================== 主函数：执行绘图 =====================
if __name__ == "__main__":
    # 1. 读取JSON文件（替换为你的文件路径）
    try:
        import pathlib
        dir = pathlib.Path(__file__).parent
        metro_data = read_metro_drw_json(str(dir / "1100_drw_beijing.json"))
        print(f"✅ 成功读取数据：{metro_data.s}，共{len(metro_data.l)}条线路")
    except FileNotFoundError:
        print("❌ 错误：未找到JSON文件，请检查文件路径")
        exit(1)
    except Exception as e:
        print(f"❌ 数据解析错误：{e}")
        exit(1)

    # 2. 绘制地铁图
    plot_beijing_metro(metro_data, figsize=(18, 14), dpi=120)