from typing import List, Dict, Optional, Any
from src.memory.tree_todo.schemas import RecursivePlanTreeNode, RecursivePlanTree, TaskStatus
from src.utils.log_decorator import global_logger, traceable


arg_todo_list: List[RecursivePlanTree] = [
    RecursivePlanTree(
        # plan_tree_id="RPT-0",
        core_goal="空计划树等待初始化",
    )
]
out_todo_list: List[RecursivePlanTree] = [
    RecursivePlanTree(
        # plan_tree_id="RPT-0",
        core_goal="空计划树等待初始化",
    )
]
track_diff_result_list: List[str] = []


def run(
    current_plan_tree: RecursivePlanTree,
) -> Dict[str, str]:
    """
    执行工具核心逻辑：
    1. 存储当前计划树，与上一版本对比
    2. 分析变更内容
    3. 渲染Markdown清单
    """
    # 1. 保存当前计划树为历史版本（执行对比前）
    last_plan = arg_todo_list[-1] if arg_todo_list else None
    arg_todo_list.append(current_plan_tree.model_copy(deep=True))  # V2 中 copy → model_copy

    # 2. 分析变更（首次运行无历史版本，仅渲染）
    changes_summary = _analyze_changes(last_plan, current_plan_tree) if last_plan else "✅ 首次创建计划树"

    # 3. 渲染Markdown Todo清单
    markdown_todo = _render_plan_tree_markdown(current_plan_tree.tree_nodes, indent_level=0)

    # 4. 计算状态统计
    current_status = _calculate_status_statistics(current_plan_tree)

    # 4. 组装返回结果
    return {
        # "plan_tree_id": current_plan_tree.plan_tree_id,
        "changes_summary": changes_summary,
        "markdown_todo_list": markdown_todo,
        "status_statistics": current_status,
    }

def _get_task_by_id(nodes: List[RecursivePlanTreeNode], task_id: str) -> Optional[RecursivePlanTreeNode]:
    """递归根据task_id查找任务节点"""
    for node in nodes:
        if node.task_id == task_id:
            return node
        if node.children:
            found = _get_task_by_id(node.children, task_id)
            if found:
                return found
    return None

def _analyze_changes(
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
        new_tasks = [_get_task_by_id(current_plan.tree_nodes, tid) for tid in new_task_ids if tid]
        new_task_names = [task.task_name for task in new_tasks if task]
        changes.append(f"🆕 新增任务：{', '.join(new_task_names)}")

    # 2. 识别删除任务（仅历史有、当前无的任务）
    deleted_task_ids = set(last_task_ids) - set(current_task_ids)
    if deleted_task_ids:
        deleted_tasks = [_get_task_by_id(last_plan.tree_nodes, tid) for tid in deleted_task_ids if tid]
        deleted_task_names = [task.task_name for task in deleted_tasks if task]
        changes.append(f"🗑️ 删除任务：{', '.join(deleted_task_names)}")

    # 3. 识别状态变更任务
    common_task_ids = set(last_task_ids) & set(current_task_ids)
    status_changed = []
    for task_id in common_task_ids:
        last_task = _get_task_by_id(last_plan.tree_nodes, task_id)
        current_task = _get_task_by_id(current_plan.tree_nodes, task_id)
        if last_task and current_task and last_task.status != current_task.status:
            status_changed.append(
                f"{current_task.task_name}（{last_task.status.display_desc} → {current_task.status.display_desc}）"
            )
    if status_changed:
        changes.append(f"🔄 状态变更：{', '.join(status_changed)}")

    # 4. 识别层级调整（简化：通过父任务是否变化判断）
    level_changed = []
    for task_id in common_task_ids:
        last_parent = _find_parent_task(last_plan.tree_nodes, task_id)
        current_parent = _find_parent_task(current_plan.tree_nodes, task_id)
        last_parent_name = last_parent.task_name if last_parent else "根节点"
        current_parent_name = current_parent.task_name if current_parent else "根节点"
        if last_parent_name != current_parent_name:
            task = _get_task_by_id(current_plan.tree_nodes, task_id)
            level_changed.append(f"{task.task_name}（父任务：{last_parent_name} → {current_parent_name}）")
    if level_changed:
        changes.append(f"📌 层级调整：{', '.join(level_changed)}")

    return "\n".join(changes) if changes else "ℹ️ 计划树无明显变更"

def _find_parent_task(
    nodes: List[RecursivePlanTreeNode],
    target_task_id: str
) -> Optional[RecursivePlanTreeNode]:
    """递归查找目标任务的父任务"""
    for node in nodes:
        if node.children:
            if target_task_id in [child.task_id for child in node.children]:
                return node
            parent = _find_parent_task(node.children, target_task_id)
            if parent:
                return parent
    return None

def _render_plan_tree_markdown(
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
            child_lines = _render_plan_tree_markdown(node.children, indent_level + 1)
            markdown_lines.append(child_lines)

    return "\n".join(markdown_lines)


def _calculate_status_statistics(recursive_plan_tree: RecursivePlanTree) -> Dict[str, int]:
    """根据所有任务状态自动生成统计信息"""
    # 初始化所有状态的计数为 0
    status_count = {status.value: 0 for status in TaskStatus}
    
    # 递归统计所有任务状态
    def count_status(nodes: List[RecursivePlanTreeNode]):
        nonlocal status_count
        for node in nodes:
            status_count[node.status.value] += 1
            if node.children:
                count_status(node.children)
    
    count_status(recursive_plan_tree.tree_nodes)
    
    # 计算一下总数，以及完成率、待执行率
    total_tasks = sum(status_count.values())
    statistics = {
        "__total": total_tasks,
    }
    statistics["__completion_rate"] = round(
        status_count[TaskStatus.COMPLETED.value] / total_tasks, 2
    ) if total_tasks > 0 else 0.0
    statistics["__pending_rate"] = round(
        status_count[TaskStatus.PENDING.value] / total_tasks, 2
    ) if total_tasks > 0 else 0.0
    status_count.update(statistics)
    return status_count
