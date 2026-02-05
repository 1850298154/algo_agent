# https://www.doubao.com/chat/30875400448002306

你想基于这些应急物资运输调度场景，生成对应的随机测试数据，包含 Pydantic BaseModel 定义的数据结构，并导出 schema.json 和多个随机 data.json。我可以为你提供一个完整的实现方案，涵盖所有核心实体和关系。

### 实现思路

1. **分析核心实体**：
   - 任务（Task）：救援需求
   - 物资（Material）：运输的物品
   - 载体（Carrier）：无人机、无人车等
   - 位置（Location）：坐标信息
   - 路径（Path）：运输路线
   - 风险（Risk）：潜在危险点

2. **设计数据关系**：
   - 一个任务包含多种物资
   - 一个任务由多个载体协同完成
   - 每个载体有预设路径
   - 路径上可能存在风险点

3. **随机数据生成策略**：
   - 基于真实地理范围生成坐标
   - 模拟不同优先级和时效性要求
   - 随机生成路径点和风险点
   - 确保数据的多样性和覆盖性

### 完整代码实现

```python
import json
import random
import uuid
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator


class Location(BaseModel):
    """位置信息"""
    id: str = Field(default_factory=lambda: f"loc_{uuid.uuid4().hex[:8]}")
    name: str
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    altitude: Optional[float] = Field(default=None, description="海拔高度（米）")
    type: str = Field(default="unknown", description="位置类型：受灾点/物资点/起降点等")

    @validator('latitude', 'longitude')
    def round_coordinates(cls, v):
        """坐标保留6位小数"""
        return round(v, 6)


class Material(BaseModel):
    """物资信息"""
    id: str = Field(default_factory=lambda: f"mat_{uuid.uuid4().hex[:8]}")
    name: str
    type: str
    quantity: int = Field(gt=0)
    unit: str
    weight_kg: float = Field(gt=0)
    volume_m3: float = Field(gt=0)
    urgency_level: str = Field(default="normal", description="紧急程度：critical/urgent/normal/low")
    expiration_time: Optional[datetime] = Field(default=None, description="保质期")
    temperature_control: bool = Field(default=False, description="是否需要温控")
    special_handling: bool = Field(default=False, description="是否需要特殊处理")

    @validator('urgency_level')
    def validate_urgency(cls, v):
        if v not in ["critical", "urgent", "normal", "low"]:
            raise ValueError("紧急程度必须是 critical/urgent/normal/low 中的一个")
        return v


class RiskPoint(BaseModel):
    """风险点信息"""
    id: str = Field(default_factory=lambda: f"risk_{uuid.uuid4().hex[:8]}")
    location: Location
    type: str = Field(description="风险类型：自然灾害/道路损坏/信号干扰等")
    level: int = Field(ge=1, le=5, description="风险等级1-5")
    description: str
    timestamp: datetime = Field(default_factory=datetime.now)
    is_active: bool = Field(default=True)


class PathSegment(BaseModel):
    """路径段信息"""
    id: str = Field(default_factory=lambda: f"seg_{uuid.uuid4().hex[:8]}")
    start_location: Location
    end_location: Location
    distance_km: float = Field(gt=0)
    estimated_time_min: float = Field(gt=0)
    risk_points: List[RiskPoint] = Field(default_factory=list)
    restrictions: List[str] = Field(default_factory=list, description="通行限制")


class Carrier(BaseModel):
    """运输载体信息"""
    id: str = Field(default_factory=lambda: f"car_{uuid.uuid4().hex[:8]}")
    name: str
    type: str = Field(description="载体类型：drone/vehicle/robot")
    model: str
    max_weight_kg: float = Field(gt=0)
    max_volume_m3: float = Field(gt=0)
    current_weight_kg: float = Field(default=0)
    current_volume_m3: float = Field(default=0)
    speed_kmh: float = Field(gt=0)
    battery_level: int = Field(ge=0, le=100, description="电量百分比")
    status: str = Field(default="available", description="状态：available/busy/maintenance")
    location: Location
    assigned_path: List[PathSegment] = Field(default_factory=list)
    communication_range_km: float = Field(default=5.0)
    last_communication: datetime = Field(default_factory=datetime.now)

    @validator('type')
    def validate_type(cls, v):
        if v not in ["drone", "vehicle", "robot"]:
            raise ValueError("载体类型必须是 drone/vehicle/robot 中的一个")
        return v

    @validator('status')
    def validate_status(cls, v):
        if v not in ["available", "busy", "maintenance"]:
            raise ValueError("状态必须是 available/busy/maintenance 中的一个")
        return v


class Task(BaseModel):
    """救援任务信息"""
    id: str = Field(default_factory=lambda: f"task_{uuid.uuid4().hex[:8]}")
    name: str
    description: str
    priority: int = Field(ge=1, le=5, description="优先级1-5")
    status: str = Field(default="pending", description="状态：pending/in_progress/completed/failed")
    created_time: datetime = Field(default_factory=datetime.now)
    required_completion_time: datetime
    location: Location
    materials: List[Material] = Field(default_factory=list)
    assigned_carriers: List[Carrier] = Field(default_factory=list)
    estimated_time_arrival: Optional[datetime] = Field(default=None)
    actual_time_arrival: Optional[datetime] = Field(default=None)
    feedback: Dict[str, Any] = Field(default_factory=dict, description="任务反馈信息")

    @validator('priority')
    def validate_priority(cls, v):
        if not (1 <= v <= 5):
            raise ValueError("优先级必须在1-5之间")
        return v

    @validator('status')
    def validate_status(cls, v):
        if v not in ["pending", "in_progress", "completed", "failed"]:
            raise ValueError("状态必须是 pending/in_progress/completed/failed 中的一个")
        return v


class EmergencyResponse(BaseModel):
    """应急响应整体数据"""
    id: str = Field(default_factory=lambda: f"resp_{uuid.uuid4().hex[:8]}")
    name: str
    description: str
    start_time: datetime = Field(default_factory=datetime.now)
    end_time: Optional[datetime] = Field(default=None)
    status: str = Field(default="active", description="状态：active/completed/canceled")
    tasks: List[Task] = Field(default_factory=list)
    carriers: List[Carrier] = Field(default_factory=list)
    locations: List[Location] = Field(default_factory=list)
    risks: List[RiskPoint] = Field(default_factory=list)
    metrics: Dict[str, Any] = Field(default_factory=dict, description="救援指标")

    @validator('status')
    def validate_status(cls, v):
        if v not in ["active", "completed", "canceled"]:
            raise ValueError("状态必须是 active/completed/canceled 中的一个")
        return v


class DataGenerator:
    """随机数据生成器"""
    
    def __init__(self):
        self.locations = []
        self.materials = []
        self.carriers = []
        self.risk_points = []
        
    def generate_location(self, location_type: str = "unknown") -> Location:
        """生成随机位置信息（基于中国范围）"""
        # 中国地理范围：纬度3.86-53.55，经度73.66-135.05
        latitude = round(random.uniform(3.86, 53.55), 6)
        longitude = round(random.uniform(73.66, 135.05), 6)
        altitude = round(random.uniform(0, 5000), 2) if random.random() > 0.3 else None
        
        location_names = {
            "disaster": ["地震灾区A", "洪水淹没区B", "泥石流现场C", "滑坡区域D", "台风受灾点E"],
            "material": ["物资仓库1", "临时补给站2", "医疗物资点3", "食品储备库4", "救援设备站5"],
            "takeoff": ["无人机起降场A", "车辆集结点B", "机器人部署点C", "应急机场D", "临时停机坪E"],
            "unknown": ["未知地点X", "待探索区域Y", "坐标点Z"]
        }
        
        name = random.choice(location_names.get(location_type, location_names["unknown"]))
        return Location(
            name=name,
            latitude=latitude,
            longitude=longitude,
            altitude=altitude,
            type=location_type
        )
    
    def generate_material(self) -> Material:
        """生成随机物资信息"""
        material_types = {
            "medical": ["急救包", "氧气瓶", "心电图机", "血压计", "手术器械", "抗生素", "血浆", "疫苗"],
            "food": ["方便面", "矿泉水", "压缩饼干", "能量棒", "罐头食品", "饮用水", "即食米饭"],
            "equipment": ["对讲机", "手电筒", "发电机", "切割机", "绳索", "安全帽", "防护服", "生命探测仪"],
            "supplies": ["帐篷", "睡袋", "毛毯", "毛巾", "卫生纸", "电池", "充电器", "蜡烛"]
        }
        
        mat_type = random.choice(list(material_types.keys()))
        name = random.choice(material_types[mat_type])
        
        urgency_levels = ["critical", "urgent", "normal", "low"]
        weights = {
            "medical": random.uniform(0.1, 20),
            "food": random.uniform(0.5, 50),
            "equipment": random.uniform(1, 100),
            "supplies": random.uniform(0.3, 30)
        }
        
        volumes = {
            "medical": random.uniform(0.001, 0.1),
            "food": random.uniform(0.005, 0.5),
            "equipment": random.uniform(0.01, 2),
            "supplies": random.uniform(0.003, 1)
        }
        
        # 血液等需要温控的特殊物资
        temperature_control = (name in ["血浆", "疫苗"] or random.random() < 0.1)
        special_handling = (name in ["手术器械", "生命探测仪"] or random.random() < 0.05)
        
        # 保质期（仅对食品和药品）
        expiration_time = None
        if mat_type in ["medical", "food"] and random.random() > 0.2:
            expiration_days = random.randint(1, 180)
            expiration_time = datetime.now() + timedelta(days=expiration_days)
        
        return Material(
            name=name,
            type=mat_type,
            quantity=random.randint(1, 100),
            unit="箱" if random.random() > 0.5 else "件",
            weight_kg=round(weights[mat_type], 2),
            volume_m3=round(volumes[mat_type], 3),
            urgency_level=random.choice(urgency_levels),
            expiration_time=expiration_time,
            temperature_control=temperature_control,
            special_handling=special_handling
        )
    
    def generate_risk_point(self, location: Optional[Location] = None) -> RiskPoint:
        """生成随机风险点"""
        risk_types = [
            "地震余波", "洪水上涨", "泥石流", "滑坡", "道路塌陷", 
            "桥梁断裂", "信号干扰", "恶劣天气", "雷暴", "强风"
        ]
        
        location = location or self.generate_location()
        return RiskPoint(
            location=location,
            type=random.choice(risk_types),
            level=random.randint(1, 5),
            description=f"{random.choice(risk_types)}导致通行困难",
            timestamp=datetime.now() - timedelta(hours=random.randint(0, 24)),
            is_active=random.random() > 0.2
        )
    
    def generate_path_segment(self) -> PathSegment:
        """生成随机路径段"""
        start_loc = self.generate_location()
        end_loc = self.generate_location()
        
        # 计算距离（简化计算）
        lat_diff = abs(start_loc.latitude - end_loc.latitude)
        lon_diff = abs(start_loc.longitude - end_loc.longitude)
        distance_km = round((lat_diff + lon_diff) * 111, 2)  # 近似值
        
        # 估计时间
        speed = random.uniform(20, 80)  # km/h
        estimated_time_min = round((distance_km / speed) * 60, 2)
        
        # 随机风险点
        risk_points = []
        if random.random() > 0.3:
            num_risks = random.randint(1, 3)
            for _ in range(num_risks):
                risk_points.append(self.generate_risk_point())
        
        restrictions = []
        if random.random() > 0.5:
            restriction_types = ["限高", "限重", "单向通行", "临时封闭", "人员限行"]
            restrictions = random.sample(restriction_types, random.randint(1, 2))
        
        return PathSegment(
            start_location=start_loc,
            end_location=end_loc,
            distance_km=distance_km,
            estimated_time_min=estimated_time_min,
            risk_points=risk_points,
            restrictions=restrictions
        )
    
    def generate_carrier(self) -> Carrier:
        """生成随机运输载体"""
        carrier_types = {
            "drone": [
                {"model": "DJI Matrice 300", "max_weight": 9, "max_volume": 0.1, "speed": 72},
                {"model": "Autel EVO II", "max_weight": 3, "max_volume": 0.05, "speed": 70},
                {"model": "Skydio X2", "max_weight": 2.5, "max_volume": 0.03, "speed": 65}
            ],
            "vehicle": [
                {"model": "越野救援车", "max_weight": 5000, "max_volume": 20, "speed": 80},
                {"model": "物资运输车", "max_weight": 10000, "max_volume": 50, "speed": 60},
                {"model": "医疗救护车", "max_weight": 3000, "max_volume": 10, "speed": 90}
            ],
            "robot": [
                {"model": "地面救援机器人", "max_weight": 500, "max_volume": 5, "speed": 15},
                {"model": "履带式机器人", "max_weight": 800, "max_volume": 8, "speed": 10},
                {"model": "多足机器人", "max_weight": 200, "max_volume": 3, "speed": 8}
            ]
        }
        
        carrier_type = random.choice(list(carrier_types.keys()))
        specs = random.choice(carrier_types[carrier_type])
        
        # 随机状态
        status_weights = {"available": 0.4, "busy": 0.5, "maintenance": 0.1}
        status = random.choices(list(status_weights.keys()), list(status_weights.values()))[0]
        
        # 电量（无人机和机器人需要）
        battery_level = random.randint(20, 100) if carrier_type in ["drone", "robot"] else 100
        
        # 生成路径
        assigned_path = []
        if status == "busy" and random.random() > 0.3:
            num_segments = random.randint(2, 5)
            for _ in range(num_segments):
                assigned_path.append(self.generate_path_segment())
        
        return Carrier(
            name=f"{carrier_type.capitalize()} {random.randint(100, 999)}",
            type=carrier_type,
            model=specs["model"],
            max_weight_kg=specs["max_weight"],
            max_volume_m3=specs["max_volume"],
            current_weight_kg=round(random.uniform(0, specs["max_weight"] * 0.8), 2),
            current_volume_m3=round(random.uniform(0, specs["max_volume"] * 0.8), 3),
            speed_kmh=specs["speed"],
            battery_level=battery_level,
            status=status,
            location=self.generate_location(location_type="takeoff"),
            assigned_path=assigned_path,
            communication_range_km=random.uniform(3, 20),
            last_communication=datetime.now() - timedelta(minutes=random.randint(0, 30))
        )
    
    def generate_task(self) -> Task:
        """生成随机救援任务"""
        task_names = [
            "紧急医疗物资运输", "食品补给配送", "救援设备转运", 
            "伤员转移", "临时避难所搭建物资", "通讯设备运输"
        ]
        
        # 优先级权重（高优先级概率更高）
        priority_weights = {1: 0.1, 2: 0.2, 3: 0.4, 4: 0.2, 5: 0.1}
        priority = random.choices(list(priority_weights.keys()), list(priority_weights.values()))[0]
        
        # 状态权重
        status_weights = {"pending": 0.3, "in_progress": 0.5, "completed": 0.15, "failed": 0.05}
        status = random.choices(list(status_weights.keys()), list(status_weights.values()))[0]
        
        # 完成时间要求（紧急任务时间更短）
        completion_hours = {
            1: random.randint(1, 3),    # 最高优先级：1-3小时
            2: random.randint(3, 6),    # 高优先级：3-6小时
            3: random.randint(6, 12),   # 中优先级：6-12小时
            4: random.randint(12, 24),  # 低优先级：12-24小时
            5: random.randint(24, 48)   # 最低优先级：24-48小时
        }
        required_completion_time = datetime.now() + timedelta(hours=completion_hours[priority])
        
        # 物资
        num_materials = random.randint(1, 5)
        materials = [self.generate_material() for _ in range(num_materials)]
        
        # 分配载体
        num_carriers = random.randint(1, 3)
        carriers = [self.generate_carrier() for _ in range(num_carriers)]
        
        # ETA和实际到达时间
        estimated_time_arrival = None
        actual_time_arrival = None
        
        if status in ["in_progress", "completed", "failed"]:
            # 已开始的任务有ETA
            eta_hours = random.uniform(0.5, completion_hours[priority] * 0.8)
            estimated_time_arrival = datetime.now() + timedelta(hours=eta_hours)
            
            if status == "completed":
                # 已完成的任务有实际到达时间
                actual_delay = random.uniform(-0.2, 0.5)  # 可能提前或延迟
                actual_time_arrival = estimated_time_arrival + timedelta(
                    hours=eta_hours * actual_delay
                )
        
        # 任务反馈
        feedback = {}
        if status == "completed":
            feedback = {
                "success_rate": round(random.uniform(85, 100), 1),
                "damage": random.choice(["无损坏", "轻微损坏", "部分损坏"]) if random.random() > 0.7 else "无损坏",
                "delay_minutes": round(random.uniform(0, 60), 1) if random.random() > 0.5 else 0,
                "carrier_performance": {car.id: random.randint(80, 100) for car in carriers}
            }
        elif status == "failed":
            failure_reasons = ["路径阻断", "载体故障", "天气恶劣", "信号丢失", "任务取消"]
            feedback = {
                "failure_reason": random.choice(failure_reasons),
                "failure_time": datetime.now() - timedelta(hours=random.randint(1, 12)),
                "affected_materials": [mat.id for mat in materials[:random.randint(1, len(materials))]]
            }
        
        return Task(
            name=random.choice(task_names),
            description=f"{random.choice(task_names)}任务，优先级：{priority}级",
            priority=priority,
            status=status,
            created_time=datetime.now() - timedelta(hours=random.randint(0, 12)),
            required_completion_time=required_completion_time,
            location=self.generate_location(location_type="disaster"),
            materials=materials,
            assigned_carriers=carriers,
            estimated_time_arrival=estimated_time_arrival,
            actual_time_arrival=actual_time_arrival,
            feedback=feedback
        )
    
    def generate_emergency_response(self, num_tasks: int = 5, num_carriers: int = 10) -> EmergencyResponse:
        """生成完整的应急响应数据"""
        disaster_types = ["地震", "洪水", "泥石流", "台风", "滑坡", "海啸"]
        disaster_name = random.choice(disaster_types)
        
        # 收集所有位置
        all_locations = []
        for _ in range(num_tasks + num_carriers // 2):
            all_locations.append(self.generate_location(location_type="disaster"))
            all_locations.append(self.generate_location(location_type="material"))
            all_locations.append(self.generate_location(location_type="takeoff"))
        
        # 收集所有风险点
        all_risks = []
        for _ in range(num_tasks * 2):
            all_risks.append(self.generate_risk_point())
        
        # 生成任务和载体
        tasks = [self.generate_task() for _ in range(num_tasks)]
        carriers = [self.generate_carrier() for _ in range(num_carriers)]
        
        # 救援指标
        metrics = {
            "total_tasks": num_tasks,
            "completed_tasks": sum(1 for task in tasks if task.status == "completed"),
            "in_progress_tasks": sum(1 for task in tasks if task.status == "in_progress"),
            "failed_tasks": sum(1 for task in tasks if task.status == "failed"),
            "total_carriers": num_carriers,
            "available_carriers": sum(1 for car in carriers if car.status == "available"),
            "busy_carriers": sum(1 for car in carriers if car.status == "busy"),
            "maintenance_carriers": sum(1 for car in carriers if car.status == "maintenance"),
            "total_materials": sum(len(task.materials) for task in tasks),
            "critical_materials": sum(1 for task in tasks for mat in task.materials 
                                    if mat.urgency_level == "critical"),
            "total_distance_km": round(sum(seg.distance_km for car in carriers 
                                         for seg in car.assigned_path), 2),
            "active_risk_points": sum(1 for risk in all_risks if risk.is_active)
        }
        
        return EmergencyResponse(
            name=f"{disaster_name}应急救援响应",
            description=f"{disaster_name}发生后，针对受灾区域的综合应急救援行动",
            start_time=datetime.now() - timedelta(hours=random.randint(1, 24)),
            end_time=datetime.now() + timedelta(hours=random.randint(24, 72)) if random.random() > 0.5 else None,
            status="active" if random.random() > 0.3 else random.choice(["completed", "canceled"]),
            tasks=tasks,
            carriers=carriers,
            locations=all_locations,
            risks=all_risks,
            metrics=metrics
        )
    
    def export_schema(self, output_file: str = "schema.json"):
        """导出JSON Schema"""
        schema = EmergencyResponse.model_json_schema()
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(schema, f, ensure_ascii=False, indent=2)
        print(f"Schema导出到：{output_file}")
    
    def generate_and_export_data(self, num_samples: int = 5, base_filename: str = "data"):
        """生成并导出多个随机数据样本"""
        for i in range(num_samples):
            response_data = self.generate_emergency_response(
                num_tasks=random.randint(3, 8),
                num_carriers=random.randint(5, 15)
            )
            
            # 转换为字典并处理datetime
            data_dict = response_data.model_dump()
            
            # 保存为JSON
            filename = f"{base_filename}_{i+1:02d}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data_dict, f, ensure_ascii=False, indent=2, default=str)
            print(f"数据样本导出到：{filename}")


def main():
    """主函数"""
    generator = DataGenerator()
    
    # 导出Schema
    generator.export_schema("schema.json")
    
    # 生成5个随机数据样本
    generator.generate_and_export_data(num_samples=5, base_filename="emergency_response_data")
    
    print("\n生成完成！")
    print("文件清单：")
    print("1. schema.json - 数据结构Schema定义")
    print("2. emergency_response_data_01.json 至 emergency_response_data_05.json - 随机测试数据")


if __name__ == "__main__":
    main()
```

### 运行结果

运行上述代码后，会生成以下文件：

1. **schema.json** - 完整的数据结构Schema定义
2. **emergency_response_data_01.json** 至 **emergency_response_data_05.json** - 5个随机生成的应急救援场景数据

### 数据特点

1. **真实性**：
   - 基于真实地理范围生成坐标
   - 模拟不同类型的灾害场景
   - 包含合理的物资、载体属性

2. **多样性**：
   - 多种任务类型和优先级
   - 不同类型的运输载体
   - 随机生成的风险点和路径

3. **完整性**：
   - 包含所有核心实体和关系
   - 覆盖各种可能的状态组合
   - 包含任务反馈和救援指标

4. **可扩展性**：
   - 代码结构清晰，易于添加新的字段或实体
   - 生成策略可调整，可根据需要增加特定场景的数据

### 使用建议

1. **测试算法**：
   - 可用于测试任务指派、路径规划、ETA预测等算法
   - 包含各种边界情况（高优先级任务、复杂路径、设备故障等）

2. **系统集成**：
   - 可作为应急物资运输调度系统的测试数据
   - 支持系统功能验证和性能测试

3. **场景模拟**：
   - 可用于模拟不同类型的灾害救援场景
   - 支持应急响应演练和决策支持系统测试

这个数据生成器可以满足你对多智能体协同调度、动态在线路径规划等场景的测试需求，生成的随机数据具有较高的真实性和多样性。