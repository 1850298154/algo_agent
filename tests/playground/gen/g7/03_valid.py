from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Any
import json

# 辅助函数：解析分隔符字符串（分号/竖线）
def split_separator(v: str, sep: str = ';') -> List[str]:
    """将分隔符分隔的字符串转为列表"""
    return v.split(sep) if v else []

# 线路分段模型
class LineFragment(BaseModel):
    """地铁线路分段（如上下行分段）"""
    c: List[str] = Field(..., description="分段轨迹像素坐标列表")
    li: str = Field(..., description="分段所属线路ID")

# 站点模型
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

    # 可选：解析经纬度为浮点数
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

    # 可选：添加解析方法（如将分隔符字段转为列表）
    def get_udpx_list(self) -> List[str]:
        """解析上下行像素坐标为列表"""
        return split_separator(self.udpx, ';')

    def get_rs_list(self) -> List[str]:
        """解析路由段编码为列表"""
        return split_separator(self.rs, '|')

# 线路模型
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

    # 可选：解析线路ID为列表
    def get_line_ids(self) -> List[str]:
        """解析线路ID（竖线分隔）为列表"""
        return split_separator(self.li, '|')

# 根模型（整个地铁数据）
class BeijingMetroDrawData(BaseModel):
    """高德地铁绘制数据（1100_drw_beijing.json）"""
    s: str = Field(..., description="数据主题（如北京市地铁）")
    i: str = Field(..., description="区域编码（1100=北京）")
    l: List[MetroLine] = Field(..., description="地铁线路列表")
    o: Optional[str] = Field(default="", description="可视化画布原点（宽,高）")

    # 可选：解析原点为数字列表
    def get_origin(self) -> List[int]:
        """解析画布原点为[宽, 高]数字列表"""
        return [int(x) for x in self.o.split(',')] if self.o else []

# 读取并校验JSON文件的函数
def read_metro_drw_json(file_path: str) -> BeijingMetroDrawData:
    """
    读取高德地铁绘制JSON文件并校验数据
    
    Args:
        file_path: JSON文件路径
    
    Returns:
        校验后的地铁数据模型
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
    
    # 校验并实例化模型
    metro_data = BeijingMetroDrawData(**raw_data)
    return metro_data

# 示例：使用方法
if __name__ == "__main__":
    # 读取文件（替换为你的文件路径）
    import pathlib
    dir = pathlib.Path(__file__).parent

    metro_data = read_metro_drw_json(str(dir / "1100_drw_beijing.json"))    
    
    # 示例：打印数据信息
    print(f"数据主题：{metro_data.s}")
    print(f"包含线路数：{len(metro_data.l)}")
    
    # 遍历第一条线路的站点
    first_line = metro_data.l[0]
    print(f"\n第一条线路：{first_line.ln}（常用名：{first_line.kn}）")
    print(f"线路颜色：{first_line.cl}")
    print(f"站点数：{len(first_line.st)}")
    
    # 打印第一个站点的经纬度
    first_station = first_line.st[0]
    print(f"\n第一个站点：{first_station.n}")
    print(f"经纬度：{first_station.sl}")
    print(f"站点类型：{'换乘站' if first_station.t == '1' else '普通站'}")
    print(f"上下行线路ID：{first_station.get_udpx_list()}")