from typing import List, Dict, Optional, Any, Union
from pydantic import BaseModel, Field, field_validator  # 关键修改：导入 field_validator
import uuid
from enum import Enum, unique

# 1. 任务状态枚举（关联可视化符号与说明）
@unique
class TaskStatus(str, Enum):
    PENDING = "pending"  # 待执行
    PROCESSING = "processing"  # 正在执行
    COMPLETED = "completed"  # 执行成功
    FAILED = "failed"  # 执行失败
    RETRY = "retry"  # 重试
    SKIPPED = "skipped"  # 已跳过

    @property
    def display_symbol(self) -> str:
        """状态对应的可视化符号"""
        symbol_map = {
            self.PENDING: "[⏳]",
            self.PROCESSING: "[➡️]",
            self.COMPLETED: "[✅]",
            self.FAILED: "[❌]",
            self.RETRY: "[♻️]",
            self.SKIPPED: "[➖]"
        }
        return symbol_map[self]

    @property
    def display_desc(self) -> str:
        """状态对应的中文说明"""
        desc_map = {
            self.PENDING: "待执行",
            self.PROCESSING: "正在执行",
            self.COMPLETED: "执行成功",
            self.FAILED: "执行失败",
            self.RETRY: "重试",
            self.SKIPPED: "已跳过"  # 说明：因前置条件变更/优先级调整，主动跳过该任务，不影响整体流程
        }
        return desc_map[self]


# 2. 递归计划树节点模型（核心任务单元）
class RecursivePlanTreeNode(BaseModel):
    """递归计划树节点（层级嵌套的任务单元）"""
    task_id: str = Field(default_factory=lambda: f"TASK-{str(uuid.uuid4())}", description="任务唯一ID（本次工具调用必须唯一，后续推理如果是指代同一个任务直接引用）")
    task_name: str = Field(..., description="任务名称（简洁描述核心动作），大语言模型生成，必须全局唯一，会被dependencies列表引用")
    description: str = Field(default="", description="任务详细说明（可选，补充执行要求/预期结果）")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description=f"任务状态枚举：{[status.value for status in TaskStatus]}")
    output: str = Field(default="", description="执行结果（完成/失败时填写）")
    dependencies: Optional[List[str]] = Field(default=None, description="依赖的任务名称的列表，任务名称必须是task_name")  # 可选，列出前置任务名称
    research_directions: Optional[List[str]] = Field(default=None, description="深度研究方向（可选，仅复杂任务需要）")
    children: Optional[List["RecursivePlanTreeNode"]] = Field(default=None, description="子任务列表（层级嵌套）")

    @field_validator("children")
    def empty_children_to_none(cls, v: Optional[List["RecursivePlanTreeNode"]]) -> Optional[List["RecursivePlanTreeNode"]]:
        return v if v and len(v) > 0 else None

    class Config:
        # use_enum_values = True  # 序列化时使用枚举值（如"pending"）而非枚举对象
        arbitrary_types_allowed = True  # 允许任意类型（适配嵌套模型）

# 解决自引用问题（V2 仍需手动调用 model_rebuild）
RecursivePlanTreeNode.model_rebuild()


# 3. 完整递归计划树模型
class RecursivePlanTree(BaseModel):
    """完整递归计划树：包含层级任务树、核心目标、状态统计等"""
    # plan_tree_id: str = Field(default_factory=lambda: f"RPT-{str(uuid.uuid4())}", description="计划树唯一ID（自动生成）")
    core_goal: str = Field(..., description="核心目标（计划树要达成的最终目的）")
    # current_status: Dict[str, int] = Field(default_factory=dict, description="状态统计（各状态的任务数量）")
    tree_nodes: List[RecursivePlanTreeNode] = Field(default_factory=list, description="计划树根任务列表")
    next_action: Dict[str, Any] = Field(default_factory=dict, description="下一步建议动作（可选）")
    references: Optional[List[str]] = Field(default=None, description="参考资源列表（可选，如文档链接、数据来源）")

    class Config:
        # use_enum_values = True  # 序列化时使用枚举值
        arbitrary_types_allowed = True

