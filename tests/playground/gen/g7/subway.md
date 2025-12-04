# [指南获取数据](https://blog.csdn.net/GISShiXiSheng/article/details/107992521)
# [高德地图](https://map.amap.com/subway/index.html?&4401)
## https://map.amap.com/service/subway?_1764748927333&srhdata=1100_drw_beijing.json
## https://map.amap.com/service/subway?_1764748927334&srhdata=1100_info_beijing.json

# [字段解释](https://www.doubao.com/chat/32314146555046658)

### 一、文件命名与字段缩写解析
#### 1. 文件名含义
| 文件名 | 组成部分 | 含义解析 | 命名由来 |
|--------|----------|----------|----------|
| 1100_drw_beijing.json | 1100 | 行政区划代码（北京市的行政区划代码前四位为1100） | 按行政区划+功能类型+城市名命名，drw=draw（绘制），代表地铁地理绘制数据；info代表地铁运营信息数据 |
|        | drw      | Draw（绘制）的缩写，代表地铁线路/站点的地理空间绘制数据 |          |
|        | beijing  | 城市名称（北京） |          |
| 1100_info_beijing.json | 1100 | 同上述，北京市行政区划代码 |          |
|        | info     | Information（信息）的缩写，代表地铁站点运营/调度相关信息 |          |
|        | beijing  | 城市名称（北京） |          |

#### 2. 核心字段缩写与含义
| 字段名 | 缩写全称 | 数据类型 | 含义 | 适用文件 |
|--------|----------|----------|------|----------|
| s | Subject/Name | 字符串 | 数据主题名称（如“北京市地铁”） | 1100_drw_beijing.json |
| i | ID/RegionID | 字符串/数字 | 区域ID（北京市行政区划代码1100） | 两者均适用 |
| l | Lines | 数组（列表） | 地铁线路列表 | 两者均适用 |
| st | Stations | 数组（列表） | 线路下的站点列表 | 两者均适用 |
| rs | RouteSegment | 字符串 | 站点关联的路由段ID（多值用\|/空格分隔） | 1100_drw_beijing.json |
| udpx | UpDownPointX | 字符串 | 上下行站点X坐标（多值用;分隔） | 1100_drw_beijing.json |
| su | StationUse | 字符串/数字 | 站点使用状态（1=启用，0=停用） | 1100_drw_beijing.json |
| udsu | UpDownStationUse | 字符串 | 上下行站点使用状态（多值用;分隔） | 1100_drw_beijing.json |
| en | EnglishName | 字符串 | 站点英文名称（空代表未配置） | 1100_drw_beijing.json |
| n | Name/StationID | 字符串 | 站点名称（drw）/站点唯一标识（info） | 两者均适用（含义略有差异） |
| sid | StationID | 字符串 | 站点唯一ID | 1100_drw_beijing.json |
| p | Position | 字符串 | 站点核心坐标（格式：X Y） | 1100_drw_beijing.json |
| r | RouteID | 字符串 | 关联路由ID（多值用\|分隔） | 1100_drw_beijing.json |
| udsi | UpDownStationID | 字符串 | 上下行站点ID（多值用;分隔） | 1100_drw_beijing.json |
| t | Type | 字符串/数字 | 站点类型（1=普通站，2=换乘站等） | 1100_drw_beijing.json |
| si | StationInnerID | 字符串 | 站点内部统一ID | 两者均适用 |
| sl | StationLocation | 字符串 | 站点经纬度（格式：经度,纬度） | 1100_drw_beijing.json |
| udli | UpDownLineID | 字符串 | 上下行线路ID（多值用;分隔） | 1100_drw_beijing.json |
| poiid | POIID | 字符串 | 站点关联的POI（兴趣点）ID | 1100_drw_beijing.json |
| lg | LogicFlag | 字符串/数字 | 逻辑标识（0=正常，1=特殊） | 1100_drw_beijing.json |
| sp | SpellName | 字符串 | 站点拼音名称 | 1100_drw_beijing.json |
| a | AreaID | 字符串/数字 | 区域ID（同i字段，冗余设计） | 1100_info_beijing.json |
| ac | AreaCode | 字符串 | 区域编码（110000=北京市） | 1100_info_beijing.json |
| d | Directions | 数组（列表） | 站点上下行/多方向调度信息 | 1100_info_beijing.json |
| ls | LineStationID | 字符串 | 线路-站点关联ID | 1100_info_beijing.json |
| lt | LeaveTime | 字符串 | 站点发车时间（--:--=未配置） | 1100_info_beijing.json |
| ft | ArriveTime | 字符串 | 站点到达时间（--:--=未配置） | 1100_info_beijing.json |

### 二、数据Schema表格（结构化定义）
#### 1. 1100_drw_beijing.json Schema
| 层级 | 字段 | 数据类型 | 可为空 | 描述 | 示例值 |
|------|------|----------|--------|------|--------|
| 根节点 | s | string | N | 数据主题名称 | "北京市地铁" |
| 根节点 | i | string | N | 区域ID（行政区划代码） | "1100" |
| 根节点 | l | array[Line] | N | 地铁线路数组 | - |
| Line | st | array[Station] | N | 线路下的站点数组 | - |
| Station | rs | string | Y | 路由段ID（多值\|分隔） | "871 862\|871 848" |
| Station | udpx | string | Y | 上下行X坐标（多值;分隔） | "871 866;871 859" |
| Station | su | string | Y | 站点使用状态 | "1" |
| Station | udsu | string | Y | 上下行使用状态（多值;分隔） | "1;1" |
| Station | en | string | Y | 英文名称 | "" |
| Station | n | string | N | 站点名称 | "苹果园" |
| Station | sid | string | N | 站点唯一ID | "110100023339034" |
| Station | p | string | Y | 核心坐标（X Y） | "871 855" |
| Station | r | string | Y | 路由ID（多值\|分隔） | "900000069871\|110100023339" |
| Station | udsi | string | Y | 上下行站点ID（多值;分隔） | "900000069872017;900000069871009" |
| Station | t | string | Y | 站点类型 | "1" |
| Station | si | string | N | 站点内部ID | "110100023339034" |
| Station | sl | string | Y | 经纬度（经度,纬度） | "116.178945,39.925686" |
| Station | udli | string | Y | 上下行线路ID（多值;分隔） | "900000069872;900000069871" |
| Station | poiid | string | Y | POI ID | "BV10013454" |
| Station | lg | string | Y | 逻辑标识 | "0" |
| Station | sp | string | Y | 拼音名称 | "PingGuoYuan" |

#### 2. 1100_info_beijing.json Schema
| 层级 | 字段 | 数据类型 | 可为空 | 描述 | 示例值 |
|------|------|----------|--------|------|--------|
| 根节点 | i | string | N | 区域ID（行政区划代码） | "1100" |
| 根节点 | l | array[LineInfo] | N | 地铁线路信息数组 | - |
| LineInfo | a | string | N | 区域ID（冗余） | "1100" |
| LineInfo | st | array[StationInfo] | N | 线路下的站点信息数组 | - |
| StationInfo | ac | string | N | 区域编码 | "110000" |
| StationInfo | d | array[Direction] | N | 站点方向调度信息数组 | - |
| StationInfo | si | string | N | 站点内部ID | "110100023339034" |
| Direction | ls | string | N | 线路-站点关联ID | "900000069871" |
| Direction | lt | string | Y | 发车时间 | "--:--" |
| Direction | n | string | N | 站点标识 | "110100023339034" |
| Direction | ft | string | Y | 到达时间 | "--:--" |

### 三、Python Pydantic 实现（含类型注解+描述）
#### 1. 安装依赖
```bash
pip install pydantic python-dotenv
```

#### 2. 代码实现
```python
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
    try:
        drw_data = read_drw_subway_data("1100_drw_beijing.json")
        print(f"绘制数据 - 主题：{drw_data.s}，区域ID：{drw_data.i}")
        # 打印第一个线路的第一个站点信息
        first_station = drw_data.l[0].st[0]
        print(f"第一个站点名称：{first_station.n}，经纬度：{first_station.sl}")
    except Exception as e:
        print(f"读取绘制数据失败：{e}")

    # 读取信息数据
    try:
        info_data = read_info_subway_data("1100_info_beijing.json")
        print(f"\n信息数据 - 区域ID：{info_data.i}")
        # 打印第一个线路的第一个站点的第一个方向信息
        first_direction = info_data.l[0].st[0].d[0]
        print(f"第一个方向 - 线路站点ID：{first_direction.ls}，发车时间：{first_direction.lt}")
    except Exception as e:
        print(f"读取信息数据失败：{e}")
```

### 四、代码说明
1. **模型设计**：严格按照JSON结构分层定义Pydantic模型，每个字段均添加`Field`描述，明确含义和可为空性；
2. **类型注解**：使用`typing`模块的`List`/`Optional`标注复杂类型，符合Python类型规范；
3. **工具函数**：封装文件读取逻辑，包含文件存在性校验，确保鲁棒性；
4. **使用示例**：提供了完整的调用示例，可直接运行测试。

### 五、扩展说明
- 若JSON中存在更多嵌套层级或字段，可在对应模型中新增字段（保持`Optional`或必填）；
- Pydantic会自动校验数据类型，若JSON字段类型与模型定义不符，会抛出`ValidationError`，便于数据校验；
- 可基于模型扩展数据处理逻辑（如解析经纬度、拆分多值字段、数据清洗等）。

