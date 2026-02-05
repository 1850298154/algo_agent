from typing import cast
def fake_cast_demo():
    x = "123"  # 这是一个字符串
    
    # 告诉 Mypy：把 x 当成整数（其实它还是字符串）
    y = cast(int, x)
    
    print(f"y 的值是: {y}")
    print(f"y 的真实类型是: {type(y)}")
    
    # 报错！虽然你 cast 成了 int，但运行时它还是 str，不能加 1
    # print(y + 1) 

fake_cast_demo()