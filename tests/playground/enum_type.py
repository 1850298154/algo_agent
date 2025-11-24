from pydantic import BaseModel, Field
import uuid
from typing import Optional, List
import enum
class TaskStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class RecursivePlanTreeNode(BaseModel):
    task_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="任务唯一ID")
    task_name: str = Field(..., description="任务名称")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="任务状态")
    # （省略其他字段）

# 方式1：用枚举实例初始化（推荐）
node1 = RecursivePlanTreeNode(task_name="任务1", status=TaskStatus.PROCESSING)

# 方式2：用枚举值（字符串）初始化（正确，Pydantic自动解析）
node2 = RecursivePlanTreeNode(task_name="任务2", status="completed")

# 方式3：用字符串变量初始化（正确）
status_str = "failed"
node3 = RecursivePlanTreeNode(task_name="任务3", status=status_str)

# 验证结果（枚举字段会自动转为实例）
print(node1.status)  # 输出：TaskStatus.PROCESSING
print(node2.status)  # 输出：TaskStatus.COMPLETED
print(node3.status)  # 输出：TaskStatus.FAILED

enum_list = [status.value for status in TaskStatus]
print('enum_list:', enum_list)  # 输出：['pending', 'processing', 'completed', 'failed']
# 错误1：用枚举名称（"PROCESSING" 是名称，不是值）
try:
    RecursivePlanTreeNode(task_name="任务4", status="PROCESSING")
except ValueError as e:
    print("错误1：", e)  # 输出：Value error, invalid value for Enum 'TaskStatus'

# 错误2：用不存在的字符串
try:
    RecursivePlanTreeNode(task_name="任务5", status="invalid_status")
except ValueError as e:
    print("错误2：", e)  # 输出：Value error, invalid value for Enum 'TaskStatus'