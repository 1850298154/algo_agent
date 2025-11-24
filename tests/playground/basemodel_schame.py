# import pydantic
# from pydantic import BaseModel, Field
# class MyModel(BaseModel):
#     name: str
#     _internal_field: int = Field(exclude=True)

# # 实例化模型
# obj = MyModel(name="Test", _internal_field=42)

# # 代码中可以正常访问
# print(obj.name)            # 输出: Test
# print(obj._internal_field) # 输出: 42

# # 序列化（比如 to_json）时，这些字段也会被排除
# print(obj.model_dump_json()) # 输出: {"name": "Test"}






# Pydantic V2 推荐写法
from pydantic import BaseModel, Field

class MyModel(BaseModel):
    name: str
    internal_field: int = Field(exclude=True) # 不再使用 _internal_field

# 生成 schema 时，internal_field 会被排除
schema = MyModel.model_json_schema()
import pprint
pprint.pprint(schema)

# 代码内依然可以正常使用
obj = MyModel(name="Test", internal_field=42)
print(obj.internal_field) # 输出: 42





from pydantic import BaseModel, Field

class MyModel(BaseModel):
    name: str
    internal_field: int = Field(...) # 注意，这里可以不加 exclude=True

# 在生成 schema 时，通过 exclude 参数指定要排除的字段
# schema = MyModel.model_json_schema(exclude={"internal_field"})

# print(schema)








from pydantic import BaseModel, Field
from typing import Type

class MyModel(BaseModel):
    name: str
    internal_field: int = Field(...)

    class Config:
        @staticmethod
        def schema_extra(schema: dict, model: Type['MyModel']) -> None:
            # 从 properties 中移除 'internal_field'
            if 'internal_field' in schema.get('properties', {}):
                del schema['properties']['internal_field']
            
            # 从 required 列表中移除 'internal_field'
            if 'internal_field' in schema.get('required', []):
                schema['required'].remove('internal_field')

# 直接生成 schema
schema = MyModel.model_json_schema()

pprint.pprint(schema)