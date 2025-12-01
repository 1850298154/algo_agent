from typing_extensions import Annotated
from pydantic import Field, BaseModel

# 元数据可以是多个：先写描述，再写校验规则
Phone = Annotated[
    str,
    "用户手机号",  # 元数据1：描述
    Field(pattern=r"^1[3-9]\d{9}$")  # 元数据2：Pydantic校验规则 # 意思是
]

class User(BaseModel):
    phone: Phone
def print_phone_info(p: Phone):
    print(p.__metadata__[0])
    print('---------')
    
    
# 测试：校验不合法的手机号会报错
try:
    print_phone_info(p = "13123456789")

    User(phone="123456")
    
except Exception as e:
    print(e)  # 输出：String should match pattern '^1[3-9]\\d{9}$'

from typing_extensions import Annotated

# 元数据是字符串（表示字段含义）
Age = Annotated[int, "用户的年龄，必须大于0", Field(pattern=r"^\d+$")]
Name = Annotated[str, "用户的姓名，不能为空"]

def print_user_info(age: Age, name: Name):
    # 可以通过 __metadata__ 获取元数据（需要自己写逻辑读取）
    print(f"姓名：{name}，年龄：{age}")
    print(f"字段说明：{Age.__metadata__[0]}")  # 输出：用户的年龄，必须大于0
    print(f"字段说明：{Age.__metadata__}")  # 输出：用户的年龄，必须大于0

print_user_info(age=18, name="豆包")