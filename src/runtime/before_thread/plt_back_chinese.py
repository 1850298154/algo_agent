from src.utils import global_logger

global_logger.info("---------- 0.1 在子线程执行任何 Matplotlib 相关代码前，先导入并执行 plt_back_chinese 模块，完成必要的初始化设置")
import matplotlib
import matplotlib.pyplot as plt

# ① 设置无 GUI 后端（最关键）
matplotlib.use("Agg")  

# ② 设置中文字体
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
global_logger.info("---------- 0.2 plt_back_chinese 模块执行完毕，Matplotlib 已完成中文支持的初始化设置")