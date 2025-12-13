from src.runtime import cwd
import matplotlib.pyplot as plt
cwd.create_cwd('./tests/playground/gen/g9')








import csv
import json
from enum import Enum
from typing import List
from pydantic import BaseModel, field_validator
from pydantic.json_schema import model_json_schema

# 定义星级枚举
class StarRatingEnum(str, Enum):
    """景区星级枚举"""
    THREE_A = "3A"
    FOUR_A = "4A"
    FIVE_A = "5A"

# 定义开放状态枚举
class OpenStatusEnum(str, Enum):
    """景区开放状态枚举"""
    OPEN = "open"
    CLOSE = "close"

# 定义Pydantic数据模型（枚举版+游玩时长）
class ScenicSpot(BaseModel):
    """景区信息数据模型（枚举+经纬度拆分+游玩时长）"""
    name: str                  # 景点名称
    star_rating: StarRatingEnum  # 星级评定（枚举）
    open_status: OpenStatusEnum  # 开放状态（枚举）
    longitude: float           # 经度
    latitude: float            # 纬度
    suggested_play_hours: float  # 建议游玩小时数（新增字段）

    # 自定义枚举验证提示（增强错误信息）
    @field_validator('star_rating', mode='before')
    def validate_star_rating(cls, v):
        try:
            return StarRatingEnum(v.strip())
        except ValueError:
            raise ValueError(
                f"星级必须为{[e.value for e in StarRatingEnum]}中的一个，当前值：{v}"
            )

    @field_validator('open_status', mode='before')
    def validate_open_status(cls, v):
        try:
            return OpenStatusEnum(v.strip())
        except ValueError:
            raise ValueError(
                f"开放状态必须为{[e.value for e in OpenStatusEnum]}中的一个，当前值：{v}"
            )
    
    # 游玩时长合法性验证（新增）
    @field_validator('suggested_play_hours', mode='before')
    def validate_play_hours(cls, v):
        try:
            hours = float(v.strip())
            if hours <= 0:
                raise ValueError("建议游玩时长必须大于0")
            return hours
        except ValueError as e:
            raise ValueError(
                f"建议游玩时长格式错误（需为正数浮点数），当前值：{v}，错误：{str(e)}"
            )

# 读取CSV文件并转换为Pydantic对象列表（适配新增游玩时长列）
def read_csv_to_pydantic(file_path: str) -> List[ScenicSpot]:
    """读取五列格式CSV（含游玩时长），转换为带枚举的ScenicSpot对象列表"""
    spots = []
    with open(file_path, 'r', encoding='utf-8') as f:
        # 适配新增的「建议游玩小时数」列
        fieldnames = ['景点名称', '星级评定', '开放状态', '坐标', '建议游玩小时数']
        reader = csv.DictReader(f, fieldnames=fieldnames)
        next(reader)  # 跳过表头

        for row_num, row in enumerate(reader, start=2):
            try:
                # 提取并清理字段
                name = row['景点名称'].strip()
                star_rating = row['星级评定'].strip()
                open_status = row['开放状态'].strip()
                coord_str = row['坐标'].strip().strip('"')  # 去除坐标引号
                play_hours_str = row['建议游玩小时数'].strip()  # 新增游玩时长字段

                # 拆分经纬度
                lon_str, lat_str = coord_str.split(',')
                longitude = float(lon_str.strip())
                latitude = float(lat_str.strip())

                # 创建枚举版Pydantic对象（新增游玩时长参数）
                spot = ScenicSpot(
                    name=name,
                    star_rating=star_rating,
                    open_status=open_status,
                    longitude=longitude,
                    latitude=latitude,
                    suggested_play_hours=play_hours_str  # 传入游玩时长
                )
                spots.append(spot)

            except Exception as e:
                print(f"⚠️ 第{row_num}行解析失败: {str(e)}")
                continue
    return spots

# 主执行逻辑
if __name__ == '__main__':
    # 1. 读取CSV文件（适配含游玩时长的CSV）
    csv_file = '北京景点等级及建议游玩时长.csv'  # 输入CSV语义化命名
    scenic_spots = read_csv_to_pydantic(csv_file)
    
    if not scenic_spots:
        print("❌ 未解析到有效景区数据")
    else:
        # 2. 生成Schema文件（语义化命名：包含枚举+游玩时长的模型结构）
        schema = model_json_schema(ScenicSpot)
        schema_file = 'beijing_scenic_spot_schema_with_play_hours.json'
        with open(schema_file, 'w', encoding='utf-8') as f:
            json.dump(schema, f, ensure_ascii=False, indent=4)
        
        # 3. 生成数据文件（语义化命名：验证后的景点数据含游玩时长）
        data = [spot.model_dump() for spot in scenic_spots]
        data_file = 'beijing_scenic_spot_validated_data_with_play_hours.json'
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        # 输出统计信息（新增游玩时长相关统计）
        print(f"✅ 成功处理 {len(scenic_spots)} 条景区数据")
        print(f"📊 星级分布:")
        star_counts = {star: 0 for star in StarRatingEnum}
        for spot in scenic_spots:
            star_counts[spot.star_rating] += 1
        for star, count in star_counts.items():
            print(f"   - {star.value}: {count} 条")
        
        # 游玩时长统计（新增）
        total_hours = sum(spot.suggested_play_hours for spot in scenic_spots)
        avg_hours = total_hours / len(scenic_spots)
        print(f"📊 游玩时长统计:")
        print(f"   - 总建议游玩时长: {total_hours:.1f} 小时")
        print(f"   - 平均建议游玩时长: {avg_hours:.1f} 小时")
        
        print(f"📄 已生成文件:")
        print(f"   - Schema文件: {schema_file}（含枚举+游玩时长的模型结构）")
        print(f"   - 数据文件: {data_file}（验证后的景点数据）")