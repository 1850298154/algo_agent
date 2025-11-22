# https://www.doubao.com/chat/30273598436483074

我明白你的需求了，你想知道在 Pydantic 模型的不同生命周期阶段（实例化、字段修改、访问、序列化）分别可以使用哪些机制来执行自定义函数或逻辑。

下面我将为你详细梳理每个阶段可用的方法和对应的代码示例。

### 1. 实例化时 (Initialization)

这个阶段指的是当你通过 `Model(** data)` 创建一个新的模型实例时。

**可用方法：** `root_validator`

`root_validator` 可以在模型完全初始化之前和之后对整个数据进行验证和修改。它非常适合在实例化时执行一次性的、涉及多个字段的逻辑。

-   `pre=True`: 在字段被解析和验证之前运行。
-   `pre=False` (默认): 在字段被解析和验证之后运行。

**示例：**

```python
from pydantic import BaseModel, root_validator

class User(BaseModel):
    username: str
    email: str
    full_name: str = None

    @root_validator(pre=True)
    def create_full_name(cls, values):
        """在实例化时，如果没有提供 full_name，则自动从 username 创建。"""
        username = values.get('username')
        if username and 'full_name' not in values:
            values['full_name'] = f"User {username.capitalize()}"
        return values

# 使用示例
user = User(username="john_doe", email="john@example.com")
print(user)
# 输出: username='john_doe' email='john@example.com' full_name='User John_doe'
```

### 2. 后续修改模型字段时 (Field Modification)

这个阶段指的是在实例化之后，通过 `instance.field = new_value` 的方式修改字段值。

**可用方法：** `validator` (带有 `always=True`) 或自定义 `setter`。

Pydantic 的 `validator` 默认只在实例化时运行。要让它在后续修改时也运行，需要使用 `always=True` 参数。

**示例 (使用 `validator`):**

```python
from pydantic import BaseModel, validator

class Product(BaseModel):
    name: str
    price: float

    @validator('price', always=True)
    def price_must_be_positive(cls, v):
        """确保 price 始终为正数，无论是在实例化还是修改时。"""
        if v <= 0:
            raise ValueError('Price must be a positive number')
        return v

# 使用示例
product = Product(name="Book", price=29.99)

# 尝试修改为一个无效值
try:
    product.price = -5.0
except ValueError as e:
    print(f"Error setting price: {e}")
    # 输出: Error setting price: 1 validation error for Product
    #      price
    #        Price must be a positive number (type=value_error)

# 修改为一个有效值
product.price = 39.99
print(product)
# 输出: name='Book' price=39.99
```

**另一种更灵活的方式 (使用 `@property` 自定义 `setter`)：**

这种方式可以让你对字段的修改拥有完全的控制权。

```python
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    _price: float = None # 使用下划线作为私有字段

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float):
        """自定义 price 的 setter 方法。"""
        if value <= 0:
            raise ValueError('Price must be a positive number')
        self._price = value

    # 为了让 Pydantic 正确处理 _price，需要一个 root_validator
    @root_validator(pre=True)
    def init_price(cls, values):
        if 'price' in values:
            # 将传入的 'price' 值赋给 _price
            values['_price'] = values.pop('price')
        return values

# 使用示例
product = Product(name="Book", price=29.99)
try:
    product.price = -5.0
except ValueError as e:
    print(f"Error setting price: {e}")
    # 输出: Error setting price: Price must be a positive number

product.price = 39.99
print(product.price) # 输出: 39.99
```

### 3. 访问模型字段时 (Field Access)

这个阶段指的是当你通过 `instance.field` 读取字段的值时。

**可用方法：** `@property`

通过 Python 的 `property` 装饰器，你可以将一个方法伪装成一个字段。当访问这个“字段”时，对应的方法就会被执行。

**示例：**

```python
from pydantic import BaseModel
from datetime import datetime

class UserSession(BaseModel):
    user_id: int
    login_time: datetime

    @property
    def session_duration(self) -> float:
        """计算并返回当前会话持续的秒数。"""
        return (datetime.now() - self.login_time).total_seconds()

# 使用示例
import time
session = UserSession(user_id=1, login_time=datetime.now())
time.sleep(2) # 模拟 2 秒的时间流逝

# 访问 session_duration "字段"
print(f"Session duration: {session.session_duration:.2f} seconds")
# 输出: Session duration: 2.00 seconds (实际值可能略有不同)

# 注意：session_duration 不是一个真正的字段
print(session.dict())
# 输出: {'user_id': 1, 'login_time': datetime.datetime(...)}
```

### 4. 序列化时 (Serialization)

这个阶段指的是当你调用 `model.dict()` 或 `model.json()` 将模型转换为字典或 JSON 字符串时。

**可用方法：** `field_serializer`

`field_serializer` 用于在序列化特定字段时执行自定义逻辑，比如格式化日期、转换数据类型等。

**示例：**

```python
from pydantic import BaseModel, field_serializer
from datetime import datetime

class Transaction(BaseModel):
    id: int
    amount: float
    timestamp: datetime

    @field_serializer('timestamp')
    def serialize_timestamp(self, value: datetime) -> str:
        """将 datetime 对象序列化为 'YYYY-MM-DD HH:MM:SS' 格式的字符串。"""
        return value.strftime('%Y-%m-%d %H:%M:%S')

    @field_serializer('amount')
    def serialize_amount(self, value: float) -> str:
        """将金额格式化为带两位小数的字符串。"""
        return f"{value:.2f}"

# 使用示例
tx = Transaction(
    id=101,
    amount=199.9,
    timestamp=datetime(2023, 10, 5, 14, 30, 0)
)

# 序列化为字典
tx_dict = tx.dict()
print(tx_dict)
# 输出: {'id': 101, 'amount': '199.90', 'timestamp': '2023-10-05 14:30:00'}

# 序列化为 JSON
tx_json = tx.json()
print(tx_json)
# 输出: {"id": 101, "amount": "199.90", "timestamp": "2023-10-05 14:30:00"}
```

### 总结

| 阶段 | 目的 | 推荐方法 | 示例代码 |
| :--- | :--- | :--- | :--- |
| **实例化时** | 在对象创建时进行数据预处理或衍生计算 | `@root_validator(pre=True)` | 在创建 `User` 时自动生成 `full_name` |
| **修改字段时** | 在字段值被更改时进行验证或副作用处理 | `@validator(always=True)` 或 `@property.setter` | 确保 `Product` 的 `price` 始终为正 |
| **访问字段时** | 在读取字段值时动态计算或格式化 | `@property` | 动态计算 `UserSession` 的 `session_duration` |
| **序列化时** | 在转换为字典/JSON 前格式化或转换字段 | `@field_serializer` | 将 `datetime` 格式化为特定字符串 |

通过灵活运用这些机制，你可以完全控制 Pydantic 模型在其整个生命周期中的行为。

# 三种情况（ model_validator  、field_validator 、field_serializer ）

## https://www.doubao.com/chat/30273598436483074

