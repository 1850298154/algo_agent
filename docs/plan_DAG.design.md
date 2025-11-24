# https://www.doubao.com/chat/30797684892182274
好的，你的思路非常棒，我们来对代码进行修改，让它支持**基于任务名称（`task_name`）的依赖关系定义**，并在后端自动完成名称到 ID 的映射。这样可以充分利用 LLM 的语义理解能力，同时保证 ID 的唯一性和依赖关系的正确性。

以下是修改后的完整代码和说明：

### 核心修改点：

1.  **在 `RecursivePlanTreeNode` 中增加 `dependencies` 字段**：该字段在接收 LLM 输出时，存储依赖的**任务名称**。
2.  **新增一个 `PlanTreeCompiler` 类**：这个类是核心，它负责：
    *   接收 LLM 生成的、基于名称的“蓝图”（`RawPlanTreeBlueprint`）。
    *   递归地为所有节点生成 `task_id`。
    *   构建一个从 `task_name` 到 `task_id` 的全局映射。
    *   将蓝图中的所有名称依赖关系“编译”（替换）为 ID 依赖关系。
    *   最终输出一个结构正确、可以直接使用的 `RecursivePlanTree` 对象。
3.  **新增 `RawPlanTreeBlueprint` 和 `RawPlanTreeNodeBlueprint` 模型**：这两个模型用于接收和验证 LLM 输出的原始结构，它们的 `dependencies` 字段是 `List[str]` 类型，代表任务名称。

---

### 修改后的完整代码：

```python
import uuid
from enum import Enum, unique
from typing import List, Optional, Dict, Any, Set
from pydantic import BaseModel, Field, field_validator, root_validator

# 1. 任务状态枚举（无修改）
@unique
class TaskStatus(str, Enum):
    PENDING = "pending"    # 待执行
    PROCESSING = "processing" # 正在执行
    COMPLETED = "completed"  # 执行成功
    FAILED = "failed"     # 执行失败
    RETRY = "retry"       # 重试
    SKIPPED = "skipped"    # 已跳过

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

# ==============================================================================
# == 新增：用于接收LLM输出的“蓝图”模型 ==
# ==============================================================================

class RawPlanTreeNodeBlueprint(BaseModel):
    """
    原始计划树节点蓝图。
    由LLM生成，其中 dependencies 字段存储的是任务名称 (str)。
    """
    task_name: str = Field(..., description="任务名称（必须全局唯一）")
    description: str = Field(default="", description="任务详细说明")
    # LLM生成时无需关心status，默认为PENDING
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="任务状态")
    output: str = Field(default="", description="执行结果")
    research_directions: Optional[List[str]] = Field(default=None, description="深度研究方向")
    children: Optional[List["RawPlanTreeNodeBlueprint"]] = Field(default=None, description="子任务列表")
    dependencies: Optional[List[str]] = Field(default=None, description="依赖的任务名称列表")

    @field_validator("children", "dependencies")
    def empty_list_to_none(cls, v: Optional[List[Any]]) -> Optional[List[Any]]:
        return v if v and len(v) > 0 else None

# 解决自引用
RawPlanTreeNodeBlueprint.model_rebuild()

class RawPlanTreeBlueprint(BaseModel):
    """
    原始计划树蓝图。
    由LLM生成，包含核心目标和基于名称依赖的节点树。
    """
    core_goal: str = Field(..., description="核心目标")
    tree_nodes: List[RawPlanTreeNodeBlueprint] = Field(..., description="计划树根任务列表（蓝图形式）")

# ==============================================================================
# == 原有模型：现在它们的 dependencies 字段将存储 task_id ==
# ==============================================================================

# 2. 递归计划树节点模型（核心任务单元）
class RecursivePlanTreeNode(BaseModel):
    """递归计划树节点（层级嵌套的任务单元）"""
    task_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="任务唯一ID（自动生成，全局唯一）")
    task_name: str = Field(..., description="任务名称（简洁描述核心动作）")
    description: str = Field(default="", description="任务详细说明（可选，补充执行要求/预期结果）")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description=f"任务状态枚举：{[status.value for status in TaskStatus]}")
    output: str = Field(default="", description="执行结果（完成/失败时填写）")
    research_directions: Optional[List[str]] = Field(default=None, description="深度研究方向（可选，仅复杂任务需要）")
    children: Optional[List["RecursivePlanTreeNode"]] = Field(default=None, description="子任务列表（层级嵌套）")
    # 【修改】dependencies 现在存储的是 task_id
    dependencies: Optional[List[str]] = Field(default=None, description="依赖的任务ID列表")

    @field_validator("children", "dependencies")
    def empty_list_to_none(cls, v: Optional[List[Any]]) -> Optional[List[Any]]:
        return v if v and len(v) > 0 else None

    class Config:
        arbitrary_types_allowed = True

RecursivePlanTreeNode.model_rebuild()

# 3. 完整递归计划树模型
class RecursivePlanTree(BaseModel):
    """完整递归计划树：包含层级任务树、核心目标、状态统计等"""
    plan_tree_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="计划树唯一ID（自动生成）")
    core_goal: str = Field(..., description="核心目标（计划树要达成的最终目的）")
    current_status: Dict[str, Any] = Field(default_factory=dict, description="状态统计（各状态的任务数量）")
    tree_nodes: List[RecursivePlanTreeNode] = Field(default_factory=list, description="计划树根任务列表")
    next_action: Dict[str, Any] = Field(default_factory=dict, description="下一步建议动作（可选）")
    references: Optional[List[str]] = Field(default=None, description="参考资源列表（可选，如文档链接、数据来源）")

    @root_validator(pre=True)
    def calculate_status_statistics(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """根据所有任务状态自动生成统计信息"""
        if 'tree_nodes' not in values:
            return values
        
        tree_nodes = values['tree_nodes']
        
        # 初始化所有状态的计数为 0
        status_count = {status.value: 0 for status in TaskStatus}
        
        # 递归统计所有任务状态
        def count_status(nodes: List[RecursivePlanTreeNode]):
            for node in nodes:
                status_count[node.status.value] += 1
                if node.children:
                    count_status(node.children)
        
        count_status(tree_nodes)
        
        # 计算总数，以及完成率、待执行率
        total_tasks = sum(status_count.values())
        statistics = {
            "__total": total_tasks,
        }
        if total_tasks > 0:
            statistics["completion_rate"] = round(
                status_count[TaskStatus.COMPLETED.value] / total_tasks * 100, 2
            )
            statistics["pending_rate"] = round(
                status_count[TaskStatus.PENDING.value] / total_tasks * 100, 2
            )
        else:
            statistics["completion_rate"] = 0.0
            statistics["pending_rate"] = 0.0
            
        status_count.update(statistics)
        values['current_status'] = status_count
        return values

    class Config:
        arbitrary_types_allowed = True

# ==============================================================================
# == 新增：计划树编译器 ==
# ==============================================================================

class PlanTreeCompiler:
    """
    将 RawPlanTreeBlueprint 编译为最终的 RecursivePlanTree。
    主要职责：
    1. 为所有节点生成唯一的 task_id。
    2. 检查任务名称的全局唯一性。
    3. 将基于名称的依赖关系转换为基于 ID 的依赖关系。
    """
    
    def __init__(self):
        self.name_to_id_map: Dict[str, str] = {}

    def compile(self, blueprint: RawPlanTreeBlueprint) -> RecursivePlanTree:
        """
        执行编译过程。
        :param blueprint: LLM生成的原始计划树蓝图。
        :return: 编译后的、可直接使用的 RecursivePlanTree 对象。
        """
        self.name_to_id_map.clear() # 每次编译前清空映射表
        
        # 第一步：递归创建节点并生成ID，同时检查名称唯一性
        compiled_root_nodes = self._compile_nodes_recursive(blueprint.tree_nodes)
        
        # 第二步：创建最终的计划树对象
        compiled_tree = RecursivePlanTree(
            core_goal=blueprint.core_goal,
            tree_nodes=compiled_root_nodes
        )
        
        return compiled_tree

    def _compile_nodes_recursive(self, blueprint_nodes: List[RawPlanTreeNodeBlueprint]) -> List[RecursivePlanTreeNode]:
        """递归编译节点"""
        compiled_nodes = []
        
        for blueprint_node in blueprint_nodes:
            task_name = blueprint_node.task_name
            
            # 检查任务名称是否唯一
            if task_name in self.name_to_id_map:
                raise ValueError(f"任务名称 '{task_name}' 不唯一，无法生成唯一ID。请确保所有任务名称全局唯一。")
            
            # 生成ID并记录映射关系
            task_id = str(uuid.uuid4())
            self.name_to_id_map[task_name] = task_id

            # 递归编译子节点
            compiled_children = None
            if blueprint_node.children:
                compiled_children = self._compile_nodes_recursive(blueprint_node.children)

            # 创建编译后的节点（此时依赖关系还是名称）
            compiled_node = RecursivePlanTreeNode(
                task_id=task_id,
                task_name=task_name,
                description=blueprint_node.description,
                status=blueprint_node.status,
                output=blueprint_node.output,
                research_directions=blueprint_node.research_directions,
                children=compiled_children,
                dependencies=blueprint_node.dependencies # 暂时还是名称
            )
            
            compiled_nodes.append(compiled_node)
        
        # 所有节点ID生成完毕后，统一处理依赖关系（名称 -> ID）
        for compiled_node in compiled_nodes:
            if compiled_node.dependencies:
                try:
                    compiled_node.dependencies = [self.name_to_id_map[name] for name in compiled_node.dependencies]
                except KeyError as e:
                    missing_task_name = str(e).strip("'")
                    raise ValueError(f"任务 '{compiled_node.task_name}' 依赖了一个不存在的任务名称: '{missing_task_name}'")
        
        return compiled_nodes

# ==============================================================================
# == 计划树管理工具（无需修改） ==
# ==============================================================================

# 4. 计划树管理工具（存储+变更对比+Markdown渲染）
class RecursivePlanTreeTodoTool(BaseTool):
    """
    递归计划树管理工具：
    1. 自动存储当前计划树，维护历史版本
    2. 对比当前与上一版本，识别任务变更（新增/状态变更/层级调整）
    3. 渲染Markdown格式的树状Todo清单，包含状态可视化
    """
    name: str = "recursive_plan_tree_todo_manager"
    description: str = "用于管理递归结构的计划树，支持变更追踪、状态可视化和Markdown渲染"
    
    # 存储历史计划树（仅保留上一版本用于对比）
    _last_plan_tree: Optional[RecursivePlanTree] = None

    def _run(
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
        self._last_plan_tree = current_plan_tree.model_copy(deep=True)

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

            # 补充依赖关系（非空时）
            if node.dependencies:
                # 将依赖的task_id转换为task_name，增强可读性
                dep_names = []
                for dep_id in node.dependencies:
                    dep_task = self._get_task_by_id(self._last_plan_tree.tree_nodes if self._last_plan_tree else [], dep_id)
                    dep_names.append(dep_task.task_name if dep_task else dep_id) # 如果找不到，显示ID
                task_line += f"\n{indent}  > 依赖：{', '.join(dep_names)}"
            
            markdown_lines.append(task_line)

            # 递归渲染子任务
            if node.children:
                child_lines = self._render_plan_tree_markdown(node.children, indent_level + 1)
                markdown_lines.append(child_lines)

        return "\n".join(markdown_lines)

```

### 如何使用这个新架构：

1.  **调用 LLM**：你向 LLM 发送一个 Prompt，要求它根据某个目标生成一个 `RawPlanTreeBlueprint` 的 JSON 对象。
    *   **Prompt 示例**：
        > "请为我制定一个学习Python数据分析的计划。请生成一个符合以下JSON Schema的计划树蓝图（`RawPlanTreeBlueprint`）。`tree_nodes` 中的每个任务可以有 `dependencies` 字段，其值是一个字符串数组，包含它所依赖的**其他任务的名称**。请确保所有任务名称在整个计划中是唯一的。
        >
        > ```json
        > {
        >   "core_goal": "学习Python数据分析",
        >   "tree_nodes": [
        >     {
        >       "task_name": "安装Python和pip",
        >       "description": "安装最新版本的Python和包管理器pip",
        >       "dependencies": []
        >     },
        >     {
        >       "task_name": "安装数据分析库",
        >       "description": "安装numpy, pandas, matplotlib",
        >       "dependencies": ["安装Python和pip"]
        >     }
        >     // ... 更多任务
        >   ]
        > }
        > ```
        > "

2.  **解析 LLM 输出**：你的后端代码接收 LLM 返回的文本，将其解析为一个 Python 字典，然后用 `RawPlanTreeBlueprint(**data)` 来验证其结构是否正确。

3.  **编译计划树**：创建 `PlanTreeCompiler` 的实例，并调用其 `compile` 方法。
    ```python
    # 假设 llm_json_output 是你从LLM获取并解析后的字典
    try:
        blueprint = RawPlanTreeBlueprint(**llm_json_output)
        compiler = PlanTreeCompiler()
        final_plan_tree = compiler.compile(blueprint)
        
        # 现在 final_plan_tree 就是一个结构完整、依赖关系正确的 RecursivePlanTree 对象
        print(final_plan_tree)

    except ValueError as e:
        # 处理错误，例如任务名称不唯一、依赖了不存在的任务等
        print(f"计划树生成失败: {e}")
    ```

4.  **后续处理**：你可以将 `final_plan_tree` 传递给 `RecursivePlanTreeTodoTool` 进行渲染或变更管理，整个流程无缝衔接。

这个方案完美地解决了你的问题，既利用了 LLM 的优势，又保证了系统的健壮性和效率。

# 递归 schema
## https://www.doubao.com/chat/30804138603724802

# dependence id 策略
## https://www.doubao.com/chat/30798275242085122