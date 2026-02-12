import streamlit as st
import test_module
import test_import
import os
import sys
package_name = "streamlit"  # 替换成你要判断的包名
if package_name not in sys.modules:
    print(f"{package_name} 尚未导入，执行其他方法")
    pass  # 没导入过，执行其他方法
else:
    import streamlit  # 导入过，再进行导入操作
    print(f"{package_name} 已经导入，版本：{streamlit.__version__}")


st.write(f"当前进程ID: {os.getpid()}")
st.write(f"模块启动时间: {test_module.start_time}")





# import streamlit as st
# from test_module import get_start_time

# if 'start_time' not in st.session_state:
#     st.session_state.start_time = get_start_time()

# st.write(f"当前进程ID: {os.getpid()}")
# st.write(f"模块启动时间: {st.session_state.start_time}")







