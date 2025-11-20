from pydantic import BaseModel, Field
from typing import List, Optional

class RecursiveTask(BaseModel):
    task_id: str = Field(..., description="任务ID")
    task_name: str = Field(..., description="任务名称")
    status: str = Field(default="pending")
    # 递归嵌套：子任务是自身类型的列表
    children: Optional[List["RecursiveTask"]] = Field(default=None, description="子任务列表")

# 必须显式声明递归引用（Pydantic 语法要求）
# RecursiveTask.model_rebuild()

# 实例化（原生嵌套结构）
root_task = RecursiveTask(
    task_id="T001",
    task_name="收集文献",
    children=[
        RecursiveTask(task_id="T001-1", task_name="筛选文献"),
        RecursiveTask(task_id="T001-2", task_name="下载文献")
    ]
)

# 测试深度超过4层的嵌套
root_task = RecursiveTask(
    task_id="T001",
    task_name="收集文献",
    children=[
        RecursiveTask(task_id="T001-2", task_name="下载文献", children=[
            RecursiveTask(task_id="T001-2-1", task_name="创建文件夹 A", children=[
                RecursiveTask(task_id="T001-2-1-1", task_name="子文件夹 A1", children=[
                    RecursiveTask(task_id="T001-2-1-1-1", task_name="文件 A1-1")
                ]),
            ]),
        ]),
    ]
)
# 测试用json初始化
json_data = {
    "task_id": "T002",
    "task_name": "撰写报告",
    "children": [
        {
            "task_id": "T002-1",
            "task_name": "收集数据"
        },
        {
            "task_id": "T002-2",
            "task_name": "分析数据",
            "children": [
                {
                    "task_id": "T002-2-1",
                    "task_name": "统计分析"
                }
            ]
        }
    ]
}
root_task_from_json = RecursiveTask(**json_data)
print(root_task_from_json.model_dump())
print(root_task_from_json.model_dump_json())

# # 实例化（原生嵌套结构）
# root_task = RecursiveTask(
#     task_id="T001",
#     task_name="收集文献",
#     children=[
#         RecursiveTask(task_id="T001-1", task_name="筛选文献"),
#         RecursiveTask(task_id="T001-2")
#     ]
# )

# """
# Traceback (most recent call last):
#   File "d:\zyt\git_ln\algo_agent\tests\playground\agent\tool\todo_tool.py", line 45, in <module>
#     RecursiveTask(task_id="T001-2")
#   File "D:\zyt\git_ln\algo_agent\.venv\Lib\site-packages\pydantic\main.py", line 250, in __init__
#     validated_self = self.__pydantic_validator__.validate_python(data, self_instance=self)
#                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# pydantic_core._pydantic_core.ValidationError: 1 validation error for RecursiveTask
# task_name
#   Field required [type=missing, input_value={'task_id': 'T001-2'}, input_type=dict]
#     For further information visit https://errors.pydantic.dev/2.12/v/missing
# """

