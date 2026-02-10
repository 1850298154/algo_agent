import pprint
from pydantic import BaseModel, Field, ValidationError
from typing import List, Dict, Optional
from src.agent.tool.tool_base import ToolBase
from src.memory.tree_todo.schemas import RecursivePlanTreeNode, RecursivePlanTree, TaskStatus
from src.memory.tree_todo import todo_track


# 4. 计划树管理工具（存储+变更对比+Markdown渲染）
class RecursivePlanTreeTodoTool(ToolBase):
    """
必须调用作为计划推理过程的思考与记录，然后再调用其他工具。
递归计划树管理工具：
1. 自动存储当前计划树，维护历史版本
2. 对比当前与上一版本，识别任务变更（新增/状态变更/层级调整）
3. 渲染Markdown格式的树状Todo清单，包含状态可视化
    """
    
    recursive_plan_tree: RecursivePlanTree = Field(
        ..., 
        description=(
        "要管理的递归计划树对象，包含任务节点、状态和子任务。只增加、不修改、不删除任务节点。"
        ),
        examples=["print('Hello, World!')"]
    )


    async def run(
        self,
    ) -> str:
        result = todo_track.run(self.recursive_plan_tree)
        s  = (f"变更总结：\n{result['changes_summary']}")
        s += (f"Markdown清单：\n{result['markdown_todo_list']}\n")
        s += (f"status_statistics: {pprint.pformat(result['status_statistics'])}")
        s = ""
        return s

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
    tool = RecursivePlanTreeTodoTool(
        tool_call_purpose="执行任务",
        recursive_plan_tree=first_tree
    )
    s = tool.run()
    print("=== 首次运行结果 ===")
    print(s)

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
    s = tool.run()
    print(s)