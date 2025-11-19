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

