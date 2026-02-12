


import sys

package_name = "streamlit"  # 替换成你要判断的包名
if package_name not in sys.modules:
    print(f"{package_name} 尚未导入，执行其他方法")
    pass  # 没导入过，执行其他方法
else:
    import streamlit  # 导入过，再进行导入操作
    print(f"{package_name} 已经导入，版本：{streamlit.__version__}")
