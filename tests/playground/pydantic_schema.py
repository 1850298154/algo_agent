from pydantic import BaseModel, model_validator, field_validator, field_serializer
from datetime import datetime
import time

# ==============================================================================
print("1. 实例化时执行：@model_validator (替代 @root_validator)")
print("-" * 40)
# ==============================================================================

class User(BaseModel):
    username: str
    email: str
    full_name: str = None

    @model_validator(mode='before')
    @classmethod
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

print()

# ==============================================================================
print("2. 修改字段时执行：@field_validator (替代 @validator) + validate_assignment")
print("-" * 40)
# ==============================================================================

class Product(BaseModel):
    name: str
    price: float

    @field_validator('price')
    @classmethod
    def price_must_be_positive(cls, v):
        """确保 price 始终为正数。"""
        if v <= 0:
            raise ValueError('Price must be a positive number')
        return v

    model_config = {
        'validate_assignment': True  # 关键：开启赋值验证
    }

# 使用示例
try :
    # 尝试用无效值实例化
    product = Product(name="Book", price=-29.99)
except ValueError as e:
    print(f"-----------Error creating product: {e}")

product = Product(name="Book", price=29.99)

# 尝试修改为一个无效值
try:
    product.price = -5.0
except ValueError as e:
    print(f"-----------Error setting price: {e}")

# 修改为一个有效值
product.price = 39.99
print(product)
# 输出: name='Book' price=39.99

print()

# ==============================================================================
print("3. 修改/访问字段时执行：使用 @property (自定义 setter/getter)")
print("-" * 40)
# ==============================================================================

class ProductWithProperty(BaseModel):
    name: str
    _price: float = None  # 使用下划线作为私有字段

    @property
    def price(self) -> float:
        """自定义 price 的 getter 方法。"""
        return self._price

    @price.setter
    def price(self, value: float):
        """自定义 price 的 setter 方法。"""
        if value <= 0:
            raise ValueError('Price must be a positive number')
        self._price = value

    @model_validator(mode='before')
    @classmethod
    def init_price(cls, values):
        """在实例化时，将传入的 'price' 值赋给内部的 '_price'。"""
        if 'price' in values:
            price_value = values.pop('price')
            if price_value <= 0:
                raise ValueError('Price must be a positive number')
            values['_price'] = price_value
        return values

# 使用示例
try:
    # 尝试用无效值实例化
    product_prop = ProductWithProperty(name="Book", price=-29.99)
except ValueError as e:
    print(f"Error creating product: {e}")

product_prop = ProductWithProperty(name="Book", price=29.99)
try:
    product_prop.price = -5.0
except ValueError as e:
    print(f"Error setting price: {e}")

product_prop.price = 39.99
print(f"product_prop.price: {product_prop.price}")
print(f"product_prop.model_dump(): {product_prop.model_dump()}")

print()

# ==============================================================================
print("4. 访问字段时执行：使用 @property (动态计算)")
print("-" * 40)
# ==============================================================================

class UserSession(BaseModel):
    user_id: int
    login_time: datetime

    @property
    def session_duration(self) -> float:
        """计算并返回当前会话持续的秒数。"""
        return (datetime.now() - self.login_time).total_seconds()

# 使用示例
session = UserSession(user_id=1, login_time=datetime.now())
time.sleep(2)  # 模拟 2 秒的时间流逝

# 访问 session_duration "字段"
print(f"Session duration: {session.session_duration:.2f} seconds")
print(f"session.model_dump(): {session.model_dump()}")

print()

# ==============================================================================
print("5. 序列化时执行：@field_serializer")
print("-" * 40)
# ==============================================================================

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
tx_dict = tx.model_dump()
print(f"tx.model_dump(): {tx_dict}")
# 输出: tx.model_dump(): {'id': 101, 'amount': '199.90', 'timestamp': '2023-10-05 14:30:00'}

# 序列化为 JSON
tx_json = tx.model_dump_json()
print(f"tx.model_dump_json(): {tx_json}")
# 输出: tx.model_dump_json(): {"id":101,"amount":"199.90","timestamp":"2023-10-05 14:30:00"}

print("\n" + "=" * 40)


# ==============================================================================
print("6. 组合使用多种验证器和序列化器")
print("-" * 40)
# ==============================================================================
from pydantic import BaseModel, model_validator, field_validator

class Product(BaseModel):
    name: str
    price: float
    discount_price: float

    # 字段验证器：验证 price 必须为正数
    @field_validator('price')
    @classmethod
    def validate_positive(cls, v):
        if v <= 0:
            raise ValueError(f"Must be positive, got {v}")
        return v

    # 模型验证器：验证 discount_price 必须小于 price
    @model_validator(mode='before')
    @classmethod
    def validate_discount(cls, values):
        price = values.get('price')
        discount = values.get('discount_price')
        if price is not None and discount is not None:
            if discount >= price:
                raise ValueError("Discount must be less than price")
        return values

# 测试
try:
    product = Product(name="Book", price=29.99, discount_price=39.99)
except ValueError as e:
    print(e)  # 输出：1 validation error for Product
              #        __root__
              #          Discount must be less than price (type=value_error)

try:
    product = Product(name="Book", price=-29.99, discount_price=-119.99)
except ValueError as e:
    print(e)  # 输出：1 validation error for Product
              #        price
              #          Must be positive, got -29.99 (type=value_error)