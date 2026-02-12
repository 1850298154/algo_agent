# import time
# start_time = time.time()
# print(f"模块加载时间: {start_time}")

import time
from functools import lru_cache
import streamlit as st
# @lru_cache(maxsize=None)
@st.cache_data()
def get_start_time():
    return time.time()


"""
模块启动时间: 1770907023.5005383
模块启动时间: 1770907119.509484
模块启动时间: 1770907536.769977
模块启动时间: 1770907536.769977

"""
start_time = get_start_time()
print(f"模块启动时间: {start_time}")

