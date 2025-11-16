def myadd(a, b):
    return a+b

def main():
    lg=globals().keys()
    ll=locals().keys()
    print('global :', lg)
    print('local :',  ll)
    ll=locals().keys()
    print('global :', lg)
    print('local :',  ll)
    locals()['abc']=123
    ll=locals().keys()
    print('local :',  ll)
    
    ll=locals()
    x=10
    # 尝试修改已存在的变量x
    ll["x"] = 100
    print("修改x后locals()：", ll)  # 输出：{'x': 100}（字典变了）
    print("实际x的值：", x)  # 输出：10（局部变量未同步）
        
    print(abc) # NameError: name 'abc' is not defined. Did you mean: 'abs'? Or did you forget to import 'abc'?

    myadd(1, 2)
    print("核心逻辑执行", myadd(1, 2))
g=globals().keys()
l=locals().keys()
print('global :', g)
print('local :',  l)
main()