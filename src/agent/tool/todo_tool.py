from typing import List, Dict, Optional, Any, Union
from pydantic import BaseModel, Field, field_validator  # 关键修改：导入 field_validator
import uuid
from enum import Enum, unique
from src.agent.tool.base_tool import BaseTool


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
    task_id: str = Field(default_factory=lambda: f"TASK-{str(uuid.uuid4())}", description="任务唯一ID（自动生成，全局唯一）")
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
    plan_tree_id: str = Field(default_factory=lambda: f"RPT-{str(uuid.uuid4())}", description="计划树唯一ID（自动生成）")
    core_goal: str = Field(..., description="核心目标（计划树要达成的最终目的）")
    current_status: Dict[str, int] = Field(default_factory=dict, description="状态统计（各状态的任务数量）")
    tree_nodes: List[RecursivePlanTreeNode] = Field(default_factory=list, description="计划树根任务列表")
    next_action: Dict[str, Any] = Field(default_factory=dict, description="下一步建议动作（可选）")
    references: Optional[List[str]] = Field(default=None, description="参考资源列表（可选，如文档链接、数据来源）")


    @field_validator("current_status")
    def calculate_status_statistics(cls, v: Dict[str, int], values: Dict[str, Any]) -> Dict[str, int]:
        """根据所有任务状态自动生成统计信息"""
        if "tree_nodes" not in values:
            return v
        
        # 初始化所有状态的计数为 0
        status_count = {status.value: 0 for status in TaskStatus}
        
        # 递归统计所有任务状态
        def count_status(nodes: List[RecursivePlanTreeNode]):
            for node in nodes:
                status_count[node.status.value] += 1
                if node.children:
                    count_status(node.children)
        
        count_status(values["tree_nodes"])
        
        # 计算一下总数，以及完成率、待执行率
        total_tasks = sum(status_count.values())
        statistics = {
            "__total": total_tasks,
            "__completion_rate": 0.0,
            "__pending_rate": 0.0,
        }
        statistics["completion_rate"] = round(
            status_count[TaskStatus.COMPLETED.value] / total_tasks * 100, 2
        ) if total_tasks > 0 else 0.0
        statistics["pending_rate"] = round(
            status_count[TaskStatus.PENDING.value] / total_tasks * 100, 2
        ) if total_tasks > 0 else 0.0
        status_count.update(statistics)
        return status_count

    class Config:
        # use_enum_values = True  # 序列化时使用枚举值
        arbitrary_types_allowed = True


# 4. 计划树管理工具（存储+变更对比+Markdown渲染）
class RecursivePlanTreeTodoTool(BaseTool):
    """
递归计划树管理工具：
1. 自动存储当前计划树，维护历史版本
2. 对比当前与上一版本，识别任务变更（新增/状态变更/层级调整）
3. 渲染Markdown格式的树状Todo清单，包含状态可视化
    """.strip()
    name: str = "recursive_plan_tree_todo_manager"
    description: str = "用于管理递归结构的计划树，支持变更追踪、状态可视化和Markdown渲染"
    
    # 存储历史计划树（仅保留上一版本用于对比）
    _last_plan_tree: Optional[RecursivePlanTree] = None

    def run(
        self,
        current_plan_tree: RecursivePlanTree,
    ) -> Dict[str, str]:
        """
        执行工具核心逻辑：
        1. 存储当前计划树，与上一版本对比
        2. 分析变更内容
        3. 渲染Markdown清单
        """
        # 1. 保存当前计划树为历史版本（执行对比前）
        last_plan = self._last_plan_tree
        self._last_plan_tree = current_plan_tree.model_copy(deep=True)  # V2 中 copy → model_copy

        # 2. 分析变更（首次运行无历史版本，仅渲染）
        changes_summary = self._analyze_changes(last_plan, current_plan_tree) if last_plan else "✅ 首次创建计划树"

        # 3. 渲染Markdown Todo清单
        markdown_todo = self._render_plan_tree_markdown(current_plan_tree.tree_nodes)

        # 4. 组装返回结果
        return {
            "plan_tree_id": current_plan_tree.plan_tree_id,
            "changes_summary": changes_summary,
            "markdown_todo_list": markdown_todo,
            "status_statistics": current_plan_tree.current_status
        }

    def _get_task_by_id(self, nodes: List[RecursivePlanTreeNode], task_id: str) -> Optional[RecursivePlanTreeNode]:
        """递归根据task_id查找任务节点"""
        for node in nodes:
            if node.task_id == task_id:
                return node
            if node.children:
                found = self._get_task_by_id(node.children, task_id)
                if found:
                    return found
        return None

    def _analyze_changes(
        self,
        last_plan: RecursivePlanTree,
        current_plan: RecursivePlanTree
    ) -> str:
        """对比两个计划树，分析变更内容"""
        changes = []

        # 辅助函数：递归收集所有任务ID
        def collect_all_task_ids(nodes: List[RecursivePlanTreeNode]) -> List[str]:
            ids = [node.task_id for node in nodes]
            for node in nodes:
                if node.children:
                    ids.extend(collect_all_task_ids(node.children))
            return ids

        # 收集历史和当前的所有任务ID
        last_task_ids = collect_all_task_ids(last_plan.tree_nodes)
        current_task_ids = collect_all_task_ids(current_plan.tree_nodes)

        # 1. 识别新增任务
        new_task_ids = set(current_task_ids) - set(last_task_ids)
        if new_task_ids:
            new_tasks = [self._get_task_by_id(current_plan.tree_nodes, tid) for tid in new_task_ids if tid]
            new_task_names = [task.task_name for task in new_tasks if task]
            changes.append(f"🆕 新增任务：{', '.join(new_task_names)}")

        # 2. 识别删除任务（仅历史有、当前无的任务）
        deleted_task_ids = set(last_task_ids) - set(current_task_ids)
        if deleted_task_ids:
            deleted_tasks = [self._get_task_by_id(last_plan.tree_nodes, tid) for tid in deleted_task_ids if tid]
            deleted_task_names = [task.task_name for task in deleted_tasks if task]
            changes.append(f"🗑️ 删除任务：{', '.join(deleted_task_names)}")

        # 3. 识别状态变更任务
        common_task_ids = set(last_task_ids) & set(current_task_ids)
        status_changed = []
        for task_id in common_task_ids:
            last_task = self._get_task_by_id(last_plan.tree_nodes, task_id)
            current_task = self._get_task_by_id(current_plan.tree_nodes, task_id)
            if last_task and current_task and last_task.status != current_task.status:
                status_changed.append(
                    f"{current_task.task_name}（{last_task.status.display_desc} → {current_task.status.display_desc}）"
                )
        if status_changed:
            changes.append(f"🔄 状态变更：{', '.join(status_changed)}")

        # 4. 识别层级调整（简化：通过父任务是否变化判断）
        level_changed = []
        for task_id in common_task_ids:
            last_parent = self._find_parent_task(last_plan.tree_nodes, task_id)
            current_parent = self._find_parent_task(current_plan.tree_nodes, task_id)
            last_parent_name = last_parent.task_name if last_parent else "根节点"
            current_parent_name = current_parent.task_name if current_parent else "根节点"
            if last_parent_name != current_parent_name:
                task = self._get_task_by_id(current_plan.tree_nodes, task_id)
                level_changed.append(f"{task.task_name}（父任务：{last_parent_name} → {current_parent_name}）")
        if level_changed:
            changes.append(f"📌 层级调整：{', '.join(level_changed)}")

        return "\n".join(changes) if changes else "ℹ️ 计划树无明显变更"

    def _find_parent_task(
        self,
        nodes: List[RecursivePlanTreeNode],
        target_task_id: str
    ) -> Optional[RecursivePlanTreeNode]:
        """递归查找目标任务的父任务"""
        for node in nodes:
            if node.children:
                if target_task_id in [child.task_id for child in node.children]:
                    return node
                parent = self._find_parent_task(node.children, target_task_id)
                if parent:
                    return parent
        return None

    def _render_plan_tree_markdown(
        self,
        nodes: List[RecursivePlanTreeNode],
        indent_level: int = 0
    ) -> str:
        """递归渲染计划树为Markdown Todo列表"""
        markdown_lines = []
        indent = "  " * indent_level  # 每级缩进2个空格

        for node in nodes:
            # 基础信息：状态符号 + 任务名称 + 任务ID（括号内）
            status_symbol = node.status.display_symbol
            status_desc = node.status.display_desc
            task_line = f"{indent}- {status_symbol} **{node.task_name}**（ID：{node.task_id}）"
            
            # 补充状态说明（失败/重试/跳过需额外提示）
            if node.status in [TaskStatus.FAILED, TaskStatus.RETRY, TaskStatus.SKIPPED]:
                task_line += f" | 状态：{status_desc}"
            
            # 补充任务描述（非空时）
            if node.description:
                task_line += f"\n{indent}  > 说明：{node.description}"
            
            # 补充执行结果（非空时）
            if node.output:
                task_line += f"\n{indent}  > 结果：{node.output}"
            
            markdown_lines.append(task_line)

            # 递归渲染子任务
            if node.children:
                child_lines = self._render_plan_tree_markdown(node.children, indent_level + 1)
                markdown_lines.append(child_lines)

        return "\n".join(markdown_lines)


# ------------------------------
# 使用示例（与V1完全兼容）
# ------------------------------
if __name__ == "__main__":
    # 1. 创建首个计划树
    first_tree = RecursivePlanTree(
        core_goal="完成Python项目开发",
        tree_nodes=[
            RecursivePlanTreeNode(
                task_name="需求分析",
                description="梳理核心功能和非功能需求",
                status=TaskStatus.PROCESSING,
                children=[
                    RecursivePlanTreeNode(
                        task_name="收集用户需求",
                        status=TaskStatus.COMPLETED,
                        output="已收集3类核心需求"
                    ),
                    RecursivePlanTreeNode(
                        task_name="撰写需求文档",
                        status=TaskStatus.PENDING
                    )
                ]
            ),
            RecursivePlanTreeNode(
                task_name="技术选型",
                description="选择合适的框架和工具",
                status=TaskStatus.PENDING
            )
        ]
    )

    json_dict = first_tree.model_dump()  # V2 中 dict() → model_dump()
    print(type(json_dict), json_dict)
    # 2. 初始化工具并执行首次运行
    tool = RecursivePlanTreeTodoTool(**json_dict)
    result1 = tool.run()
    print("=== 首次运行结果 ===")
    print(f"计划树ID：{result1['plan_tree_id']}")
    print(f"变更总结：\n{result1['changes_summary']}")
    print(f"Markdown清单：\n{result1['markdown_todo_list']}\n")

    # 3. 创建更新后的计划树（状态变更+新增任务）
    updated_tree = RecursivePlanTree(
        core_goal="完成Python项目开发",
        tree_nodes=[
            RecursivePlanTreeNode(
                task_id=first_tree.tree_nodes[0].task_id,  # 保持原任务ID
                task_name="需求分析",
                description="梳理核心功能和非功能需求",
                status=TaskStatus.COMPLETED,
                output="需求文档已评审通过",
                children=[
                    RecursivePlanTreeNode(
                        task_id=first_tree.tree_nodes[0].children[0].task_id,
                        task_name="收集用户需求",
                        status=TaskStatus.COMPLETED,
                        output="已收集3类核心需求"
                    ),
                    RecursivePlanTreeNode(
                        task_id=first_tree.tree_nodes[0].children[1].task_id,
                        task_name="撰写需求文档",
                        status=TaskStatus.COMPLETED,
                        output="V1.0版本已完成"
                    ),
                    RecursivePlanTreeNode(
                        task_name="需求评审",  # 新增子任务
                        status=TaskStatus.COMPLETED,
                        output="评审无重大问题"
                    )
                ]
            ),
            RecursivePlanTreeNode(
                task_id=first_tree.tree_nodes[1].task_id,
                task_name="技术选型",
                description="选择合适的框架和工具",
                status=TaskStatus.PROCESSING,
                children=[
                    RecursivePlanTreeNode(
                        task_name="框架对比",
                        status=TaskStatus.PENDING
                    )
                ]
            ),
            RecursivePlanTreeNode(
                task_name="项目初始化",  # 新增根任务
                status=TaskStatus.SKIPPED,
                description="因技术选型未完成，暂跳过"
            )
        ]
    )

    # 4. 执行第二次运行（对比变更）
    result2 = tool.run(current_plan_tree=updated_tree)
    print("=== 第二次运行结果（变更对比）===")
    print(f"计划树ID：{result2['plan_tree_id']}")
    print(f"变更总结：\n{result2['changes_summary']}")
    print(f"Markdown清单：\n{result2['markdown_todo_list']}")