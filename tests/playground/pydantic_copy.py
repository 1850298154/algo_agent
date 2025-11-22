from pydantic import BaseModel
import copy

class MyModel(BaseModel):
    data: dict

# 创建一个原始字典
original_dict = {"name": "Tom", "age": 20, "hobbies": ["reading", "sports"], "contact": {"email": "tom@example.com"}}

# 实例化模型
model = MyModel(data=original_dict)

# 修改原始字典
original_dict["age"] = 21
original_dict["hobbies"].append("coding")
original_dict["contact"]["email"] = "0000@example.com"
original_dict["contact"]["phone"] = "123-456-7890"

# 打印模型中的数据
print("浅拷贝验证：")
print(f"模型中的 data: {model.data}")
print(f"原始字典: {original_dict}")
print(f"模型中的 data 与原始字典是否是同一个对象: {model.data is original_dict}")
"""
浅拷贝验证：
模型中的 data: {'name': 'Tom', 'age': 20, 'hobbies': ['reading', 'sports', 'coding'], 'contact': {'email': '0000@example.com', 'phone': '123-456-7890'}}
原始字典: {'name': 'Tom', 'age': 21, 'hobbies': ['reading', 'sports', 'coding'], 'contact': {'email': '0000@example.com', 'phone': '123-456-7890'}}
模型中的 data 与原始字典是否是同一个对象: False
"""


from pydantic import BaseModel, Field
from typing import Dict
import copy

def deep_copy_factory(original: dict) -> dict:
    return copy.deepcopy(original)

class MyModel(BaseModel):
    data: Dict = Field(default_factory=lambda: deep_copy_factory(original_dict))

# 创建一个原始字典
original_dict = {"name": "Tom", "age": 20, "hobbies": ["reading", "sports"]}

# 实例化模型
model = MyModel()

# 修改原始字典
original_dict["age"] = 21
original_dict["hobbies"].append("coding")

# 打印模型中的数据
print("\n深拷贝验证（使用 default_factory）：")
print(f"模型中的 data: {model.data}")
print(f"原始字典: {original_dict}")
print(f"模型中的 data 与原始字典是否是同一个对象: {model.data is original_dict}")
"""
深拷贝验证（使用 default_factory）：
模型中的 data: {'name': 'Tom', 'age': 20, 'hobbies': ['reading', 'sports']}
原始字典: {'name': 'Tom', 'age': 21, 'hobbies': ['reading', 'sports', 'coding']}
模型中的 data 与原始字典是否是同一个对象: False
"""


from pydantic import BaseModel

class Person:
    def __init__(self, name):
        self.name = name

class MyModel(BaseModel):
    person: Person  # 这会报错！
    class Config:
        arbitrary_types_allowed = True # 允许任意类型
# 尝试实例化
try:
    model = MyModel(person=Person("Alice"))
except Exception as e:
    print(e)
"""
在默认情况下（arbitrary_types_allowed = False），
如果你尝试将一个 Pydantic 不认识的自定义对象赋值给模型字段，
Pydantic 会抛出一个 ValidationError。
"""



