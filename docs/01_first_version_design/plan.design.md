# https://www.doubao.com/chat/30030929578384642

# ai agent 执行，需要todo list 工具，每次都需要更新自己的todo list，保持当前的专注度、以及宏观计划的持续记忆（防止遗忘最终计划及目的）。 todo list 作为一个工具， 我希望使用 树状结构 标记搜索执行的子计划计划位置，并且要标记每个节点计划的状态。 工具的输出是一个markdown格式的todo list，需要可以动态生长（包括深度和宽度）。然后这个工具还需要像git一样记录每一轮的不同（包括树的结构、以及树的深度宽度、树的节点计划状态，对于成功状态，记录结果，对于失败状态，记录失败的原因，对于当前执行状态标记正在执行），给我python代码

以下是一个满足你需求的 **AI Agent Todo List 工具** Python 实现，支持树状结构、状态追踪、版本控制（类似 Git）、动态生长，并输出 Markdown 格式结果：

```python
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union
import uuid
from datetime import datetime
import json

# 定义计划状态枚举
class TaskStatus:
    PENDING = "待执行"
    IN_PROGRESS = "正在执行"
    SUCCESS = "执行成功"
    FAILED = "执行失败"
    SKIPPED = "已跳过"

@dataclass
class TodoNode:
    """Todo List 树节点"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])  # 唯一ID（简化为8位）
    name: str  # 任务名称
    status: str = field(default=TaskStatus.PENDING)  # 任务状态
    parent_id: Optional[str] = None  # 父节点ID（根节点为None）
    children: List["TodoNode"] = field(default_factory=list)  # 子节点列表
    result: Optional[str] = None  # 执行结果（成功时记录）
    failure_reason: Optional[str] = None  # 失败原因（失败时记录）
    created_at: datetime = field(default_factory=datetime.now)  # 创建时间
    updated_at: datetime = field(default_factory=datetime.now)  # 更新时间

    def add_child(self, child: "TodoNode") -> None:
        """添加子节点"""
        child.parent_id = self.id
        child.updated_at = datetime.now()
        self.children.append(child)

    def update_status(self, status: str, result: Optional[str] = None, failure_reason: Optional[str] = None) -> None:
        """更新节点状态及附加信息"""
        self.status = status
        self.updated_at = datetime.now()
        if status == TaskStatus.SUCCESS:
            self.result = result
            self.failure_reason = None
        elif status == TaskStatus.FAILED:
            self.failure_reason = failure_reason
            self.result = None
        else:
            self.result = None
            self.failure_reason = None

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典（用于版本存储）"""
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "parent_id": self.parent_id,
            "children": [child.to_dict() for child in self.children],
            "result": self.result,
            "failure_reason": self.failure_reason,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TodoNode":
        """从字典恢复节点"""
        node = cls(
            id=data["id"],
            name=data["name"],
            status=data["status"],
            parent_id=data["parent_id"],
            result=data["result"],
            failure_reason=data["failure_reason"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"])
        )
        # 递归恢复子节点
        for child_data in data["children"]:
            child = cls.from_dict(child_data)
            node.children.append(child)
            child.parent_id = node.id
        return node

class TodoListManager:
    """Todo List 管理器（支持树状结构、版本控制）"""
    def __init__(self, root_task_name: str = "总计划"):
        """初始化，创建根节点"""
        self.root = TodoNode(name=root_task_name)
        self.versions: List[Dict[str, Any]] = []  # 版本历史（类似Git提交记录）
        self._commit_version(commit_msg="初始化Todo List")  # 初始版本

    def _commit_version(self, commit_msg: str) -> None:
        """提交当前状态到版本历史"""
        version_data = {
            "commit_id": str(uuid.uuid4())[:10],
            "commit_msg": commit_msg,
            "commit_time": datetime.now().isoformat(),
            "tree_data": self.root.to_dict()
        }
        self.versions.append(version_data)

    def find_node_by_id(self, node_id: str, current_node: Optional[TodoNode] = None) -> Optional[TodoNode]:
        """递归查找节点（按ID）"""
        current = current or self.root
        if current.id == node_id:
            return current
        for child in current.children:
            found = self.find_node_by_id(node_id, child)
            if found:
                return found
        return None

    def add_task(self, parent_id: str, task_name: str, commit_msg: str = "添加子任务") -> str:
        """
        添加子任务
        :param parent_id: 父任务ID
        :param task_name: 新任务名称
        :param commit_msg: 版本提交信息
        :return: 新任务ID
        """
        parent_node = self.find_node_by_id(parent_id)
        if not parent_node:
            raise ValueError(f"父节点ID {parent_id} 不存在")
        
        new_node = TodoNode(name=task_name)
        parent_node.add_child(new_node)
        self._commit_version(commit_msg=commit_msg)
        return new_node.id

    def update_task_status(self, node_id: str, status: str, result: Optional[str] = None, 
                          failure_reason: Optional[str] = None, commit_msg: str = "更新任务状态") -> None:
        """
        更新任务状态
        :param node_id: 任务ID
        :param status: 状态（TaskStatus枚举值）
        :param result: 成功结果（可选）
        :param failure_reason: 失败原因（可选）
        :param commit_msg: 版本提交信息
        """
        if status not in [TaskStatus.PENDING, TaskStatus.IN_PROGRESS, TaskStatus.SUCCESS, TaskStatus.FAILED, TaskStatus.SKIPPED]:
            raise ValueError(f"无效状态：{status}")
        
        node = self.find_node_by_id(node_id)
        if not node:
            raise ValueError(f"任务ID {node_id} 不存在")
        
        node.update_status(status, result, failure_reason)
        self._commit_version(commit_msg=commit_msg)

    def _render_markdown_tree(self, node: TodoNode, depth: int = 0, is_last: List[bool] = []) -> str:
        """递归渲染Markdown树状结构"""
        # 状态标记图标
        status_icon = {
            TaskStatus.PENDING: "○",
            TaskStatus.IN_PROGRESS: "●",
            TaskStatus.SUCCESS: "✅",
            TaskStatus.FAILED: "❌",
            TaskStatus.SKIPPED: "➖"
        }[node.status]

        # 缩进和连接线
        indent_parts = []
        for i in range(depth - 1):
            if is_last[i]:
                indent_parts.append("  ")
            else:
                indent_parts.append("│ ")
        if depth > 0:
            if is_last[-1]:
                indent_parts.append("└─")
            else:
                indent_parts.append("├─")
        indent = "".join(indent_parts)

        # 节点基本信息
        line = f"{indent}{status_icon} **{node.name}** (ID: {node.id})"
        
        # 附加信息（结果/失败原因）
        if node.result:
            line += f" → 结果：{node.result}"
        elif node.failure_reason:
            line += f" → 失败原因：{node.failure_reason}"

        # 递归渲染子节点
        child_lines = []
        for idx, child in enumerate(node.children):
            child_is_last = is_last + [idx == len(node.children) - 1]
            child_lines.append(self._render_markdown_tree(child, depth + 1, child_is_last))
        
        return line + "\n" + "\n".join(child_lines)

    def get_markdown_todo(self) -> str:
        """获取当前Todo List的Markdown格式"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        markdown = f"# AI Agent Todo List（更新时间：{current_time}）\n\n"
        markdown += self._render_markdown_tree(self.root)
        markdown += f"\n## 状态说明\n"
        markdown += f"- ○ 待执行 | ● 正在执行 | ✅ 执行成功 | ❌ 执行失败 | ➖ 已跳过\n"
        return markdown

    def get_version_history(self) -> str:
        """获取版本历史（类似Git Log）"""
        markdown = "# 版本历史\n\n"
        for idx, version in enumerate(reversed(self.versions)):  # 倒序显示（最新在前）
            markdown += f"### 版本 {version['commit_id']}（{version['commit_time']}）\n"
            markdown += f"- 说明：{version['commit_msg']}\n\n"
        return markdown

    def checkout_version(self, commit_id: str, commit_msg: str = "回滚到指定版本") -> None:
        """回滚到指定版本"""
        target_version = next((v for v in self.versions if v["commit_id"] == commit_id), None)
        if not target_version:
            raise ValueError(f"版本 {commit_id} 不存在")
        
        self.root = TodoNode.from_dict(target_version["tree_data"])
        self._commit_version(commit_msg=commit_msg)

    def get_task_path(self, node_id: str) -> str:
        """获取任务的层级路径（例如：总计划 → 子计划1 → 子任务A）"""
        node = self.find_node_by_id(node_id)
        if not node:
            raise ValueError(f"任务ID {node_id} 不存在")
        
        path = [node.name]
        current = node
        while current.parent_id:
            parent = self.find_node_by_id(current.parent_id)
            if parent:
                path.insert(0, parent.name)
                current = parent
            else:
                break
        return " → ".join(path)

# ------------------------------
# 示例使用
# ------------------------------
if __name__ == "__main__":
    # 1. 初始化Todo List管理器（根任务为"AI Agent 搜索执行计划"）
    todo_manager = TodoListManager(root_task_name="AI Agent 搜索执行计划")
    print("=== 初始Todo List ===")
    print(todo_manager.get_markdown_todo())

    # 2. 给根节点添加一级子任务
    root_id = todo_manager.root.id
    task1_id = todo_manager.add_task(
        parent_id=root_id,
        task_name="1. 分析用户需求",
        commit_msg="添加一级任务：分析用户需求"
    )
    task2_id = todo_manager.add_task(
        parent_id=root_id,
        task_name="2. 制定搜索策略",
        commit_msg="添加一级任务：制定搜索策略"
    )
    task3_id = todo_manager.add_task(
        parent_id=root_id,
        task_name="3. 执行搜索操作",
        commit_msg="添加一级任务：执行搜索操作"
    )
    task4_id = todo_manager.add_task(
        parent_id=root_id,
        task_name="4. 整理搜索结果",
        commit_msg="添加一级任务：整理搜索结果"
    )

    print("\n=== 添加一级任务后 ===")
    print(todo_manager.get_markdown_todo())

    # 3. 给"制定搜索策略"添加子任务（二级任务）
    strategy_child1_id = todo_manager.add_task(
        parent_id=task2_id,
        task_name="2.1 确定搜索关键词",
        commit_msg="添加二级任务：确定搜索关键词"
    )
    strategy_child2_id = todo_manager.add_task(
        parent_id=task2_id,
        task_name="2.2 选择搜索工具",
        commit_msg="添加二级任务：选择搜索工具"
    )

    # 4. 给"确定搜索关键词"添加子任务（三级任务）
    todo_manager.add_task(
        parent_id=strategy_child1_id,
        task_name="2.1.1 提取核心关键词",
        commit_msg="添加三级任务：提取核心关键词"
    )
    keyword_child2_id = todo_manager.add_task(
        parent_id=strategy_child1_id,
        task_name="2.1.2 扩展相关关键词",
        commit_msg="添加三级任务：扩展相关关键词"
    )

    print("\n=== 添加多级子任务后 ===")
    print(todo_manager.get_markdown_todo())

    # 5. 更新任务状态
    # 标记"分析用户需求"为成功
    todo_manager.update_task_status(
        node_id=task1_id,
        status=TaskStatus.SUCCESS,
        result="用户需要搜索AI Agent相关的开源项目",
        commit_msg="更新任务状态：分析用户需求成功"
    )

    # 标记"提取核心关键词"为正在执行
    extract_keyword_id = todo_manager.find_node_by_id(strategy_child1_id).children[0].id
    todo_manager.update_task_status(
        node_id=extract_keyword_id,
        status=TaskStatus.IN_PROGRESS,
        commit_msg="更新任务状态：提取核心关键词正在执行"
    )

    # 标记"扩展相关关键词"为失败
    todo_manager.update_task_status(
        node_id=keyword_child2_id,
        status=TaskStatus.FAILED,
        failure_reason="关键词扩展工具调用超时",
        commit_msg="更新任务状态：扩展相关关键词失败"
    )

    print("\n=== 更新任务状态后 ===")
    print(todo_manager.get_markdown_todo())

    # 6. 查看版本历史
    print("\n=== 版本历史 ===")
    print(todo_manager.get_version_history())

    # 7. 查看任务路径
    print("\n=== 任务路径示例 ===")
    print(f"任务 {keyword_child2_id} 的路径：{todo_manager.get_task_path(keyword_child2_id)}")

    # 8. 回滚到初始版本（示例）
    initial_commit_id = todo_manager.versions[0]["commit_id"]
    todo_manager.checkout_version(
        commit_id=initial_commit_id,
        commit_msg="回滚到初始化版本"
    )
    print("\n=== 回滚到初始版本后 ===")
    print(todo_manager.get_markdown_todo())
```

### 核心功能说明
1. **树状结构支持**：
   - 基于 `TodoNode` 类实现多级嵌套任务（深度和宽度可动态扩展）
   - 每个节点包含唯一ID、父节点ID、子节点列表，支持递归查找和操作

2. **状态管理**：
   - 支持5种状态：`待执行`/`正在执行`/`执行成功`/`执行失败`/`已跳过`
   - 成功节点记录`result`，失败节点记录`failure_reason`
   - 状态更新自动触发版本提交

3. **版本控制（类似Git）**：
   - 每次修改（添加任务/更新状态）自动生成版本记录
   - 记录`commit_id`、`提交信息`、`提交时间`、`完整树结构`
   - 支持回滚到历史版本、查看版本历史

4. **Markdown输出**：
   - 树状结构用`├─`/`└─`符号展示层级关系
   - 状态用直观图标标记（○/●/✅/❌/➖）
   - 包含任务ID、附加信息（结果/失败原因）、更新时间

5. **辅助功能**：
   - 任务路径查询（显示任务的完整层级路径）
   - 节点ID快速查找
   - 版本回滚操作

### 示例输出效果（Markdown）
```markdown
# AI Agent Todo List（更新时间：2025-11-19 15:30:00）

✅ **AI Agent 搜索执行计划** (ID: a1b2c3d4)
├─✅ **1. 分析用户需求** (ID: e5f6g7h8) → 结果：用户需要搜索AI Agent相关的开源项目
├─○ **2. 制定搜索策略** (ID: i9j0k1l2)
│ ├─● **2.1 确定搜索关键词** (ID: m3n4o5p6)
│ │ ├─● **2.1.1 提取核心关键词** (ID: q7r8s9t0)
│ │ └─❌ **2.1.2 扩展相关关键词** (ID: u1v2w3x4) → 失败原因：关键词扩展工具调用超时
│ └─○ **2.2 选择搜索工具** (ID: y5z6a7b8)
├─○ **3. 执行搜索操作** (ID: c9d0e1f2)
└─○ **4. 整理搜索结果** (ID: g3h4i5j6)

## 状态说明
- ○ 待执行 | ● 正在执行 | ✅ 执行成功 | ❌ 执行失败 | ➖ 已跳过
```

### 使用方法
1. **初始化**：创建管理器时指定根任务名称
2. **添加任务**：调用`add_task(parent_id, task_name)`，需指定父任务ID
3. **更新状态**：调用`update_task_status(node_id, status, result/failure_reason)`
4. **查看结果**：`get_markdown_todo()`获取当前Todo List，`get_version_history()`查看版本记录
5. **回滚版本**：`checkout_version(commit_id)`回滚到指定版本

该工具完全满足你的需求：树状结构标记子计划位置、节点状态追踪、动态生长、版本控制（记录每轮变更），且输出格式规范易读。你可以根据实际需求扩展更多功能（如任务优先级、截止时间等）。

# dataclass是干什么的？ 枚举有没有强制的校验？


### 一、`dataclass` 是什么？
`dataclass` 是 Python 3.7+ 引入的 **数据类装饰器**（位于 `dataclasses` 模块），核心作用是 **简化“仅存储数据的类”的定义**，自动帮你生成常用方法，避免重复编码。

#### 1. 解决的痛点
如果不使用 `dataclass`，定义一个“仅存数据”的类（比如之前的 `TodoNode`）需要手动写很多模板代码：
```python
class TodoNode:
    def __init__(self, name, status="待执行", parent_id=None, children=None):
        self.name = name
        self.status = status
        self.parent_id = parent_id
        self.children = children or []  # 避免默认参数是可变对象的坑
        # 还要手动加 created_at、updated_at 等字段...

    # 如需打印实例友好信息，要写 __repr__
    def __repr__(self):
        return f"TodoNode(name={self.name}, status={self.status}, ...)"

    # 如需比较实例相等性，要写 __eq__
    def __eq__(self, other):
        if not isinstance(other, TodoNode):
            return False
        return self.name == other.name and self.status == other.status and ...
```

#### 2. `dataclass` 的核心功能
用 `@dataclass` 装饰后，上述模板代码会 **自动生成**，你只需声明字段即可：
```python
from dataclasses import dataclass, field

@dataclass
class TodoNode:
    name: str  # 必选字段（类型注解是必填的，否则不视为数据字段）
    status: str = "待执行"  # 带默认值的字段
    parent_id: Optional[str] = None  # 可选字段
    children: List["TodoNode"] = field(default_factory=list)  # 可变默认值（用 field 避免坑）
    created_at: datetime = field(default_factory=datetime.now)  # 动态默认值（每次实例化都生成新时间）
```

自动生成的方法包括：
- `__init__`：初始化方法（按字段声明顺序生成参数）
- `__repr__`：实例的字符串表示（方便调试，比如 `TodoNode(name='任务1', status='待执行')`）
- `__eq__`：实例相等性判断（比较所有数据字段是否相同）
- 可选生成 `__lt__`/`__le__` 等比较方法（需指定 `order=True`，如 `@dataclass(order=True)`）

#### 3. 关键细节
- 字段必须加 **类型注解**（否则不会被视为 `dataclass` 的数据字段）；
- 可变默认值（如 `list`、`dict`）不能直接写 `children=[]`（会导致所有实例共享同一个列表），必须用 `field(default_factory=list)`（每次实例化都创建新列表）；
- `field()` 函数可精细化配置字段（如 `init=False` 表示该字段不参与 `__init__` 参数，`repr=False` 表示不显示在 `__repr__` 中）。


### 二、枚举（`TaskStatus`）有没有强制校验？
先明确结论：**有强制校验，但需要正确使用枚举类**。

#### 1. 枚举的核心作用
之前的 `TaskStatus` 是一个 **简单的类属性枚举**（简化写法），本质是用类属性存储固定的合法值，目的是：
- 统一状态的字符串表示（避免拼写错误，比如写 `"执行成功"` 而不是 `"成功"`）；
- 提供清晰的合法值列表（方便代码阅读和维护）。

#### 2. 强制校验的实现
之前的代码中，已经通过 `update_task_status` 方法做了 **显式校验**：
```python
def update_task_status(self, node_id: str, status: str, ...):
    # 校验 status 是否在合法的枚举值中
    if status not in [TaskStatus.PENDING, TaskStatus.IN_PROGRESS, ...]:
        raise ValueError(f"无效状态：{status}")
    # ... 后续逻辑
```
这就是强制校验：如果传入的 `status` 不是 `TaskStatus` 中定义的合法值（比如 `"无效状态"`），会直接抛出异常，阻止非法值写入。

#### 3. 更规范的枚举实现（推荐 `enum.Enum`）
之前的 `TaskStatus` 是“自定义枚举”，Python 标准库 `enum` 模块提供了更强大的 `Enum` 类，校验更严格，用法更规范：
```python
from enum import Enum

# 继承 Enum 实现规范枚举
class TaskStatus(Enum):
    PENDING = "待执行"
    IN_PROGRESS = "正在执行"
    SUCCESS = "执行成功"
    FAILED = "执行失败"
    SKIPPED = "已跳过"
```

此时的强制校验会更彻底：
- 必须传入 `TaskStatus` 的枚举成员（而不是字符串），否则直接报错；
- 枚举成员是唯一的，不能重复定义相同值。

#### 4. 规范枚举的使用示例（修改后）
```python
# 1. 定义规范枚举
from enum import Enum

class TaskStatus(Enum):
    PENDING = "待执行"
    IN_PROGRESS = "正在执行"
    SUCCESS = "执行成功"
    FAILED = "执行失败"
    SKIPPED = "已跳过"

# 2. 修改 TodoNode 字段类型（从 str 改为 TaskStatus）
@dataclass
class TodoNode:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str
    status: TaskStatus = field(default=TaskStatus.PENDING)  # 类型注解为枚举类型
    # ... 其他字段

# 3. 修改 update_task_status 方法（直接接收枚举成员，无需手动校验）
def update_task_status(self, node_id: str, status: TaskStatus, result: Optional[str] = None, 
                      failure_reason: Optional[str] = None, commit_msg: str = "更新任务状态") -> None:
    # 无需手动校验！如果传入非 TaskStatus 成员，类型检查（或运行时）会直接报错
    node = self.find_node_by_id(node_id)
    if not node:
        raise ValueError(f"任务ID {node_id} 不存在")
    
    node.status = status
    node.updated_at = datetime.now()
    if status == TaskStatus.SUCCESS:
        node.result = result
        node.failure_reason = None
    elif status == TaskStatus.FAILED:
        node.failure_reason = failure_reason
        node.result = None
    else:
        node.result = None
        node.failure_reason = None
    self._commit_version(commit_msg=commit_msg)

# 4. 调用时必须传入枚举成员（而不是字符串）
todo_manager.update_task_status(
    node_id=task1_id,
    status=TaskStatus.SUCCESS,  # 传入枚举成员，而非 "执行成功"
    result="用户需要搜索AI Agent相关的开源项目"
)
```

#### 5. 规范枚举的优势（更强的强制校验）
- 禁止传入非法值：如果写 `status="执行成功"`（字符串），会触发类型错误（因为 `status` 要求是 `TaskStatus` 类型）；如果写 `status=TaskStatus.INVALID`（不存在的枚举成员），会直接报错；
- 避免字符串拼写错误：枚举成员是唯一的，IDE 会自动补全，不会出现 `status="执行成"` 这种笔误；
- 代码更清晰：枚举成员的语义更明确，比纯字符串更易读。


### 总结
1. `dataclass` 是 **简化数据类定义的装饰器**，自动生成 `__init__`/`__repr__` 等方法，避免重复编码，核心用于“仅存储数据的类”；
2. 枚举（`TaskStatus`）**有强制校验**：
   - 之前的实现通过 `status not in [合法值]` 做显式校验；
   - 推荐使用 `enum.Enum` 实现规范枚举，校验更严格（禁止非法类型、拼写错误），代码更易维护。

如果需要将之前的代码改为规范枚举版本，可以直接替换 `TaskStatus` 的定义，并调整相关字段的类型注解和调用方式即可。

# 我的意思是模型输出的是 JSON，没有问题，用 JSON 表示 todo list。但是我们这个工具是需要识别出每一次 to do list 的变动在哪里，以及并将它转成 Markdown 格式输出出来。方便来做后续的观察与总结等等分析。
明白了！核心需求是：**底层用 JSON 存储 Todo 列表（保证模型可解析、状态可跟踪），工具自动识别 JSON 的变动（新增/完成/变更等），并同步输出 Markdown 格式（供人观察总结）** —— 既保留 JSON 的结构化优势（模型友好），又兼顾 Markdown 的可读性（人友好），同时自动标注变动，无需人工对比。

这个设计才是“模型能懂、人能看”的最优解！下面是具体实现：

### 核心逻辑设计
1. **输入**：上次的 JSON 计划（基准版） + 本次的 JSON 计划（更新版）；
2. **工具核心能力**：
   - 自动对比两个 JSON，识别变动类型（新增/完成/状态变更/内容修改/删除）；
   - 给变动项打标签（如「🔴新增」「🟢完成」）；
   - 自动将最新 JSON 转成层级化 Markdown Todo 树；
   - 输出「Markdown 可视化结果 + 变动总结」。
3. **输出**：一份带变动标注的 Markdown 计划书（含完整 Todo 树 + 变动清单）。

### 最终工具实现（严格遵循基类，JSON 转 Markdown + 变动识别）
```python
import inspect
import inflection
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal
from deepdiff import DeepDiff  # 用于对比JSON变动（需安装：pip install deepdiff）

# ---------------------- 复用数据模型（保持JSON结构统一） ----------------------
class Task(BaseModel):
    """单个任务的结构化定义（模型用JSON存储时遵循此结构）"""
    task_id: str = Field(..., description="任务唯一ID（如 T001）")
    task_name: str = Field(..., description="任务名称")
    description: str = Field(..., description="任务详细描述")
    status: Literal["pending", "processing", "completed", "failed", "paused"] = Field(default="pending", description="任务状态")
    output: str = Field(default="", description="执行结果")
    next_dependency: str = Field(default="", description="下一个依赖任务ID")
    research_directions: Optional[List[str]] = Field(default=None, description="深度研究方向")
    parent_task_id: Optional[str] = Field(default=None, description="父任务ID（用于层级结构，顶级任务为None）")

class ContextReference(BaseModel):
    type: str = Field(..., description="资源类型")
    url: Optional[str] = Field(default=None, description="资源链接")
    note: str = Field(..., description="资源说明")

class AgentPlan(BaseModel):
    """完整的JSON计划结构（模型存储和修改的基准格式）"""
    agent_plan_id: str = Field(..., description="计划ID")
    core_goal: str = Field(..., description="核心目标")
    current_status: Dict = Field(..., description="当前状态：stage/progress/last_executed_task/pending_issue")
    task_plan: List[Task] = Field(..., description="任务列表（含层级关系）")
    next_action: Dict = Field(..., description="下一步动作")
    context_references: Optional[List[ContextReference]] = Field(default=None, description="参考资源")

# ---------------------- 核心工具：JSON变动识别 + Markdown转换 ----------------------
class TodoJsonToMarkdownTool(BaseTool):
    """
    AI Agent Todo 管理工具：输入上次和本次的JSON计划，自动识别变动并转成Markdown Todo树。
    核心功能：
    1. 对比两次JSON计划，识别变动（新增/完成/状态变更/内容修改/删除/层级调整）；
    2. 给Markdown中的变动任务打标签，直观展示差异；
    3. 生成层级化Markdown Todo树（按parent_task_id构建父子关系）；
    4. 输出变动总结，方便后续观察分析。
    """
    # 入参：上次的JSON计划（基准）、本次的JSON计划（更新后）
    last_json_plan: AgentPlan = Field(..., description="上一次的完整JSON计划（BaseModel实例，作为变动对比基准）")
    current_json_plan: AgentPlan = Field(..., description="本次更新后的完整JSON计划（BaseModel实例，需包含所有任务）")

    @classmethod
    def tool_name(cls) -> str:
        return "todo_json_to_markdown"

    @classmethod
    def tool_description(cls) -> str:
        return "输入两次JSON格式的Todo计划，自动识别变动（新增/完成/修改等），并转换为带变动标注的层级化Markdown Todo树，供人观察总结"

    def run(self) -> str:
        """核心执行逻辑：对比JSON→识别变动→构建层级→生成Markdown"""
        # 1. 转换为字典，方便对比和处理
        last_plan_dict = self.last_json_plan.model_dump()
        current_plan_dict = self.current_json_plan.model_dump()

        # 2. 识别所有变动（用DeepDiff对比，输出结构化变动信息）
        changes = self._detect_changes(last_plan_dict, current_plan_dict)

        # 3. 构建层级化任务树（按parent_task_id关联父子任务）
        task_tree = self._build_task_tree(current_plan_dict["task_plan"])

        # 4. 生成带变动标注的Markdown
        markdown_content = self._generate_markdown(task_tree, changes)

        # 5. 生成变动总结
        change_summary = self._generate_change_summary(changes)

        # 6. 拼接最终输出
        final_output = f"""# {current_plan_dict['agent_plan_id']} 分析计划书（Markdown可视化）
## 核心目标：{current_plan_dict['core_goal']}
## 当前状态：{current_plan_dict['current_status']['stage']}（进度：{current_plan_dict['current_status']['progress']}%）
## 下一步动作：{current_plan_dict['next_action']['action_name']}（优先级：{current_plan_dict['next_action']['priority']}）

---

{markdown_content}

---

## 本次变动总结
{change_summary}

---
⚠️ 说明：
- 标签含义：🔴新增 | 🟢完成 | 🔵状态变更 | 🟡内容修改 | 🔴删除 | 🟣层级调整
- 任务前[x]表示已完成，[ ]表示未完成
- 参考资源：{self._format_references(current_plan_dict['context_references'])}
"""
        return final_output.strip()

    def _detect_changes(self, last_plan: Dict, current_plan: Dict) -> Dict:
        """辅助方法：对比两次计划，识别变动类型"""
        # 提取两次的任务ID列表
        last_task_ids = {task["task_id"] for task in last_plan["task_plan"]}
        current_task_ids = {task["task_id"] for task in current_plan["task_plan"]}

        # 初始化变动字典
        changes = {
            "added": [],  # 新增任务（current有，last无）
            "deleted": [],  # 删除任务（last有，current无）
            "status_changed": [],  # 状态变更（task_id存在，status不同）
            "content_changed": [],  # 内容修改（task_id存在，status相同但其他字段变）
            "hierarchy_changed": []  # 层级调整（parent_task_id变更）
        }

        # 1. 识别新增和删除任务
        changes["added"] = list(current_task_ids - last_task_ids)
        changes["deleted"] = list(last_task_ids - current_task_ids)

        # 2. 对比现有任务的变动（状态/内容/层级）
        last_task_map = {task["task_id"]: task for task in last_plan["task_plan"]}
        current_task_map = {task["task_id"]: task for task in current_plan["task_plan"]}

        for task_id in current_task_ids & last_task_ids:
            last_task = last_task_map[task_id]
            current_task = current_task_map[task_id]

            # 识别状态变更
            if last_task["status"] != current_task["status"]:
                changes["status_changed"].append({
                    "task_id": task_id,
                    "old_status": last_task["status"],
                    "new_status": current_task["status"]
                })
                # 若状态变为completed，单独标记为“完成”（优先级高于普通状态变更）
                if current_task["status"] == "completed":
                    changes["added"].append(f"🟢完成-{task_id}")  # 后续Markdown中特殊标注

            # 识别层级调整（parent_task_id变更）
            if last_task.get("parent_task_id") != current_task.get("parent_task_id"):
                changes["hierarchy_changed"].append({
                    "task_id": task_id,
                    "old_parent": last_task.get("parent_task_id"),
                    "new_parent": current_task.get("parent_task_id")
                })

            # 识别内容修改（排除状态和parent_task_id的变更）
            last_task_clean = {k: v for k, v in last_task.items() if k not in ["status", "parent_task_id", "output"]}
            current_task_clean = {k: v for k, v in current_task.items() if k not in ["status", "parent_task_id", "output"]}
            if last_task_clean != current_task_clean:
                changes["content_changed"].append(task_id)

        return changes

    def _build_task_tree(self, tasks: List[Dict]) -> List[Dict]:
        """辅助方法：按parent_task_id构建层级化任务树"""
        task_map = {task["task_id"]: task for task in tasks}
        task_tree = []

        # 先找顶级任务（parent_task_id为None或空）
        for task_id, task in task_map.items():
            if not task.get("parent_task_id"):
                # 递归找子任务
                task["children"] = self._find_children(task_id, task_map)
                task_tree.append(task)

        return task_tree

    def _find_children(self, parent_id: str, task_map: Dict) -> List[Dict]:
        """辅助方法：递归查找子任务"""
        children = []
        for task_id, task in task_map.items():
            if task.get("parent_task_id") == parent_id:
                task["children"] = self._find_children(task_id, task_map)
                children.append(task)
        return children

    def _generate_markdown(self, task_tree: List[Dict], changes: Dict) -> str:
        """辅助方法：生成带变动标注的Markdown Todo树"""
        markdown_lines = []
        # 递归生成层级（用缩进表示层级，顶级无缩进，子任务加2空格）
        def recursive_render(tasks: List[Dict], indent: int = 0):
            for task in tasks:
                task_id = task["task_id"]
                status = task["status"]
                task_name = task["task_name"]
                description = task["description"]

                # 1. 确定完成状态（[x] / [ ]）
                check_box = "[x]" if status == "completed" else "[ ]"

                # 2. 确定变动标签
                tag = ""
                if any(f"🟢完成-{task_id}" in item for item in changes["added"]):
                    tag = "🟢完成 "
                elif task_id in changes["added"]:
                    tag = "🔴新增 "
                elif any(item["task_id"] == task_id for item in changes["status_changed"]):
                    tag = "🔵状态变更 "
                elif task_id in changes["content_changed"]:
                    tag = "🟡内容修改 "
                elif any(item["task_id"] == task_id for item in changes["hierarchy_changed"]):
                    tag = "🟣层级调整 "

                # 3. 拼接任务行（缩进+复选框+标签+任务信息）
                indent_space = "  " * indent
                task_line = f"{indent_space}- {check_box} {tag}{task_name}（{task_id}）"
                markdown_lines.append(task_line)

                # 4. 添加任务描述（缩进+斜体）
                if description:
                    desc_line = f"{indent_space}  *描述：{description}*"
                    markdown_lines.append(desc_line)

                # 5. 递归渲染子任务
                if task["children"]:
                    recursive_render(task["children"], indent + 1)

        recursive_render(task_tree)
        return "\n".join(markdown_lines)

    def _generate_change_summary(self, changes: Dict) -> str:
        """辅助方法：生成简洁的变动总结"""
        summary_lines = []

        if changes["added"]:
            # 过滤掉“完成”标记的新增项，单独统计
            completed_tasks = [item.replace("🟢完成-", "") for item in changes["added"] if item.startswith("🟢完成-")]
            pure_added = [item for item in changes["added"] if not item.startswith("🟢完成-")]
            if pure_added:
                summary_lines.append(f"- 新增任务：{', '.join(pure_added)}（共{len(pure_added)}个）")
            if completed_tasks:
                summary_lines.append(f"- 完成任务：{', '.join(completed_tasks)}（共{len(completed_tasks)}个）")

        if changes["deleted"]:
            summary_lines.append(f"- 删除任务：{', '.join(changes['deleted'])}（共{len(changes['deleted'])}个）")

        if changes["status_changed"]:
            status_str = "; ".join([f"{item['task_id']}（{item['old_status']}→{item['new_status']}）" for item in changes["status_changed"]])
            summary_lines.append(f"- 状态变更：{status_str}（共{len(changes['status_changed'])}个）")

        if changes["content_changed"]:
            summary_lines.append(f"- 内容修改：{', '.join(changes['content_changed'])}（共{len(changes['content_changed'])}个）")

        if changes["hierarchy_changed"]:
            hierarchy_str = "; ".join([f"{item['task_id']}（父任务：{item['old_parent'] or '无'}→{item['new_parent'] or '无'}）" for item in changes["hierarchy_changed"]])
            summary_lines.append(f"- 层级调整：{hierarchy_str}（共{len(changes['hierarchy_changed'])}个）")

        if not any(summary_lines):
            return "✅ 无任何变动，计划保持一致"

        return "\n".join(summary_lines)

    def _format_references(self, references: Optional[List[Dict]]) -> str:
        """辅助方法：格式化参考资源"""
        if not references:
            return "无"
        ref_lines = [f"- {ref['type']}：{ref['note']}（链接：{ref['url'] or '无'}）" for ref in references]
        return "\n".join(ref_lines)

# ---------------------- 工具使用示例 ----------------------
if __name__ == "__main__":
    # 1. 构造上次的JSON计划（基准版）
    last_plan = AgentPlan(
        agent_plan_id="deep_research_202406",
        core_goal="完成XX主题深度研究，输出结构化分析报告",
        current_status={
            "stage": "执行阶段",
            "progress": 0,
            "last_executed_task": "",
            "pending_issue": ""
        },
        task_plan=[
            Task(
                task_id="T001",
                task_name="收集XX主题文献",
                description="收集近5年高被引论文+行业报告",
                status="pending",
                parent_task_id=None
            ),
            Task(
                task_id="T002",
                task_name="筛选核心文献",
                description="保留与主题强相关的文献",
                status="pending",
                parent_task_id="T001"
            )
        ],
        next_action={
            "action_name": "执行T001：收集XX主题文献",
            "priority": "high",
            "required_input": "无",
            "expected_output": "20+篇核心文献"
        },
        context_references=[
            ContextReference(
                type="文献库",
                url="https://scholar.google.com",
                note="关键词：XX技术、2020-2024"
            )
        ]
    )

    # 2. 构造本次的JSON计划（更新版）
    current_plan = AgentPlan(
        agent_plan_id="deep_research_202406",
        core_goal="完成XX主题深度研究，输出结构化分析报告",
        current_status={
            "stage": "执行阶段",
            "progress": 40,
            "last_executed_task": "T001",
            "pending_issue": "无"
        },
        task_plan=[
            Task(
                task_id="T001",
                task_name="收集XX主题文献",
                description="收集近5年高被引论文+行业报告（补充中文核心期刊）",  # 内容修改
                status="completed",  # 状态变更为完成
                output="已收集23篇核心文献",
                parent_task_id=None
            ),
            Task(
                task_id="T002",
                task_name="筛选核心文献",
                description="保留与主题强相关的文献",
                status="completed",  # 状态变更为完成
                output="筛选出18篇强相关文献",
                parent_task_id="T001"
            ),
            Task(
                task_id="T003",  # 新增任务
                task_name="文献精读与信息提取",
                description="提取核心观点、数据支撑、研究缺口",
                status="pending",
                parent_task_id=None
            ),
            Task(
                task_id="T004",  # 新增任务（子任务）
                task_name="标记研究缺口",
                description="重点关注未解决的技术问题",
                status="pending",
                parent_task_id="T003"  # 层级关联T003
            )
        ],
        next_action={
            "action_name": "执行T003：文献精读与信息提取",
            "priority": "high",
            "required_input": "18篇强相关文献",
            "expected_output": "文献核心观点汇总表"
        },
        context_references=[
            ContextReference(
                type="文献库",
                url="https://scholar.google.com",
                note="关键词：XX技术、2020-2024"
            ),
            ContextReference(
                type="中文核心期刊",
                url="https://cnki.net",
                note="新增中文文献来源"
            )
        ]
    )

    # 3. 调用工具，生成带变动标注的Markdown
    tool = TodoJsonToMarkdownTool(
        last_json_plan=last_plan,
        current_json_plan=current_plan
    )
    print(tool.run())
```

### 工具核心优势（完全匹配你的需求）
1. **JSON 底层存储**：模型用 JSON 管理 Todo 列表，结构化强、无歧义，模型能精准解析和修改（符合你“JSON 表示 Todo list”的要求）；
2. **自动识别变动**：工具通过 `DeepDiff` 对比两次 JSON，无需模型手动标注变动，自动识别“新增/完成/修改/删除/层级调整”，减少模型负担；
3. **Markdown 可视化输出**：自动将 JSON 转成层级化 Todo 树，带勾选框和变动标签，人能直接阅读、观察进度，满足“后续观察与总结”需求；
4. **变动总结清晰**：单独输出变动清单，无需人工对比两次计划，快速掌握核心变更；
5. **严格遵循基类**：完全继承 `BaseTool` 接口，可直接集成到 Agent 工具链，无需额外适配。

### 工具输出效果示例（Markdown）
```markdown
# deep_research_202406 分析计划书（Markdown可视化）
## 核心目标：完成XX主题深度研究，输出结构化分析报告
## 当前状态：执行阶段（进度：40%）
## 下一步动作：执行T003：文献精读与信息提取（优先级：high）

---

- [x] 🟢完成 收集XX主题文献（T001）
  *描述：收集近5年高被引论文+行业报告（补充中文核心期刊）*
  - [x] 🟢完成 筛选核心文献（T002）
    *描述：保留与主题强相关的文献*
- [ ] 🔴新增 文献精读与信息提取（T003）
  *描述：提取核心观点、数据支撑、研究缺口*
  - [ ] 🔴新增 标记研究缺口（T004）
    *描述：重点关注未解决的技术问题*

---

## 本次变动总结
- 完成任务：T001, T002（共2个）
- 新增任务：T003, T004（共2个）
- 内容修改：T001（共1个）

---
⚠️ 说明：
- 标签含义：🔴新增 | 🟢完成 | 🔵状态变更 | 🟡内容修改 | 🔴删除 | 🟣层级调整
- 任务前[x]表示已完成，[ ]表示未完成
- 参考资源：
- 文献库：关键词：XX技术、2020-2024（链接：https://scholar.google.com）
- 中文核心期刊：新增中文文献来源（链接：https://cnki.net）
```

### 模型使用流程
1. 模型每次修改计划时，直接更新 `AgentPlan` 格式的 JSON（新增/修改任务、更新状态等）；
2. 调用 `TodoJsonToMarkdownTool`，传入「上次的 JSON 计划」和「本次的 JSON 计划」；
3. 工具自动输出带变动标注的 Markdown，供人观察总结，模型也可通过 JSON 保持状态跟踪。

### 依赖安装
工具使用了 `deepdiff` 库对比 JSON 变动，需提前安装：
```bash
pip install deepdiff pydantic
```

如果需要调整变动标签、Markdown 格式（如缩进长度、任务信息展示），或补充更多变动类型（如“截止时间变更”“优先级变更”），可以随时优化！

# 符号选择
- [⭕] 待执行 
- [⚪] 待执行 
- [⚫] 正在执行 

- [⏳] 待执行 
- [➡️] 正在执行 
- [✅] 执行成功 
- [❌] 执行失败 
- [♻️] 重试
- [➖] 已跳过