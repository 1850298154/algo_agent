from pydantic import BaseModel, Field
from typing import List, Optional


# ===================== 1100_drw_beijing.json 模型 =====================
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
    r: Optional[str] = Field(None, description="关联路由ID，多值用|分隔")
    udsi: Optional[str] = Field(None, description="上下行站点ID，多值用;分隔")
    t: Optional[str] = Field(None, description="站点类型，1=普通站，2=换乘站等")
    si: str = Field(..., description="站点内部统一ID")
    sl: Optional[str] = Field(None, description="站点经纬度，格式：经度,纬度")
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


# ===================== 1100_info_beijing.json 模型 =====================
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


# ===================== 读取JSON文件的工具函数 =====================
import json
from pathlib import Path


def read_drw_subway_data(file_path: str) -> DrwSubwayData:
    """
    读取1100_drw_beijing.json文件并解析为Pydantic模型
    
    Args:
        file_path: JSON文件路径
    
    Returns:
        解析后的DrwSubwayData模型实例
    """
    file = Path(file_path)
    if not file.exists():
        raise FileNotFoundError(f"文件不存在：{file_path}")
    
    with open(file, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
    
    return DrwSubwayData(**raw_data)


def read_info_subway_data(file_path: str) -> InfoSubwayData:
    """
    读取1100_info_beijing.json文件并解析为Pydantic模型
    
    Args:
        file_path: JSON文件路径
    
    Returns:
        解析后的InfoSubwayData模型实例
    """
    file = Path(file_path)
    if not file.exists():
        raise FileNotFoundError(f"文件不存在：{file_path}")
    
    with open(file, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
    
    return InfoSubwayData(**raw_data)


# ===================== 使用示例 =====================
if __name__ == "__main__":
    # 读取绘制数据
    import os
    dir = os.path.dirname(__file__)
    try:
        # 读取绘制数据
        drw_data = read_drw_subway_data(os.path.join(dir, "1100_drw_beijing.json"))
        print(f"绘制数据 - 主题：{drw_data.s}，区域ID：{drw_data.i}")
        # 打印第一个线路的第一个站点信息
        first_station = drw_data.l[0].st[0]
        print(f"第一个站点名称：{first_station.n}，经纬度：{first_station.sl}")
    except Exception as e:
        print(f"读取绘制数据失败：{e}")

    # 读取信息数据
    try:
        info_data = read_info_subway_data(os.path.join(dir, "1100_info_beijing.json"))
        print(f"\n信息数据 - 区域ID：{info_data.i}")
        # 打印第一个线路的第一个站点的第一个方向信息
        first_direction = info_data.l[0].st[0].d[0]
        print(f"第一个方向 - 线路站点ID：{first_direction.ls}，发车时间：{first_direction.lt}")
    except Exception as e:
        print(f"读取信息数据失败：{e}")