from typing import Dict, List, Literal, Tuple  
from pydantic import BaseModel, Field, ConfigDict  
import yaml  
from pathlib import Path  
  
  
class UavTypeNum(BaseModel):  
    """UAV类型数量配置"""  
    uavA: int  
    uavB: int  
    uavC: int  
    
    # 实现类似字典的 items 和 values 函数
    def items(self) -> List[Tuple[str, int]]:  
        return [("uavA", self.uavA), ("uavB", self.uavB), ("uavC", self.uavC)]
    
    def values(self) -> List[int]:  
        return [self.uavA, self.uavB, self.uavC]
  
  
class BaseConfig(BaseModel):  
    """基地配置"""  
    pos_init: List[float] = Field(..., description="初始位置 [x, y]")  
    pos_range: List[float] = Field(..., description="位置范围 [width, height]")  
    uav_type_2_num: UavTypeNum = Field(..., description="各类型UAV数量", alias="type_num")  
  
  
class EventConfig(BaseModel):  
    """事件配置"""  
    center_option: Literal["lattice", "sample"] = Field(..., description="中心点选项")  
    center_x: List[float] = Field(..., description="任务中心点X坐标列表")  
    center_y: List[float] = Field(..., description="任务中心点Y坐标列表")  
    precedence: List[List[int]] = Field(..., description="任务优先级关系 [[task_i, task_j], ...]")  
    radius: List[float] = Field(..., description="任务半径列表")  
    simultaneous: List[List[int]] = Field(..., description="可同时执行的任务组")  
    targetA_num: List[int] = Field(..., description="目标A数量列表")  
    targetB_num: List[int] = Field(..., description="目标B数量列表")  
    task_num: int = Field(..., description="任务总数")  
    task_type: List[Literal["capture", "attack", "surveillance"]] = Field(..., description="任务类型列表")  
    x: List[int] = Field(..., description="格子X坐标列表")  
    y: List[int] = Field(..., alias="y", description="格子Y坐标列表")  
  
  
class MetaConfig(BaseModel):  
    """元数据配置"""  
    alpha: float = Field(..., description="Alpha参数")  
    num_agents: int = Field(..., description="智能体总数")  
    num_tasks: int = Field(..., description="任务总数")  
  
  
class EnvironmentConfig(BaseModel):  
    """环境配置主模型"""  
    agents: Dict[str, BaseConfig] = Field(..., description="智能体基地配置")  
    events: Dict[int, EventConfig] = Field(..., description="事件配置，键为事件触发时间")  
    meta: MetaConfig = Field(..., description="元数据")  
    random_seed: int = Field(..., description="随机种子")  
    timestep: float = Field(..., description="时间步长")  
  
    model_config = ConfigDict(populate_by_name=True)  
  
