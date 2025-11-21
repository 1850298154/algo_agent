from collections import OrderedDict

# 创建一个 OrderedDict 作为全局命名空间
global_ns = OrderedDict()
global_ns['a'] = 100
# 创建一个 OrderedDict 作为局部命名空间
local_ns = OrderedDict()
local_ns['x'] = 10
local_ns['y'] = 20
code = r"""
b = a * 2
print(f"a * 2 = {b}")
z = x + y
print(f"x + y = {z}")
"""

# 将 OrderedDict 传入 exec 的 globals 参数
# 注意：第二个参数是 globals，第三个参数我们传入 local_ns 作为 locals
exec(code, global_ns, local_ns)

"""
a * 2 = 200
x + y = 30
"""