from src.utils.log_decorator import global_logger

global_logger.info("---------- 0.1 在子线程执行任何 Matplotlib 相关代码前，先导入并执行 plt_back_chinese 模块，完成必要的初始化设置")
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
try:
    # ========== 第一步：强制设置无GUI后端（必配） ==========
    matplotlib.use("Agg")  # 服务器/后台运行必配，避免GUI字体加载问题

    # ========== 第二步：强制加载本地SimHei字体文件（Windows专属） ==========
    # SimHei（黑体）的绝对路径，Windows系统默认存在
    font_path = "C:/Windows/Fonts/simhei.ttf"
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"❌ 未找到黑体字体文件：{font_path}，请检查系统字体是否完整")

    # 创建字体属性对象，强制绑定字体文件
    chinese_font_prop = fm.FontProperties(fname=font_path)
    chinese_font_name = chinese_font_prop.get_name()

    # ========== 第三步：彻底覆盖所有字体配置，禁止回退到Arial ==========
    # 核心：将所有字体族都指向中文字体，杜绝回退
    plt.rcParams.clear()  # 清空原有配置，避免冲突
    plt.rcParams.update({
        # 全局字体族：强制使用无衬线字体（即我们的SimHei）
        'font.family': 'sans-serif',
        # 无衬线字体列表：只保留SimHei，不允许回退到其他字体
        'font.sans-serif': [chinese_font_name],
        # 等宽字体：也用SimHei，解决monospace文本乱码
        'font.monospace': [chinese_font_name],
        # 解决负号显示为方块
        'axes.unicode_minus': False,
    })
except Exception as e:
    # ① 设置无 GUI 后端（最关键）
    matplotlib.use("Agg")  

    # ② 设置中文字体
    plt.rcParams["font.sans-serif"] = ["SimHei"]
    plt.rcParams["axes.unicode_minus"] = False    
    global_logger.error(f"❌ Matplotlib 中文字体初始化失败: {e}")
    global_logger.error("请确保服务器环境完整，SimHei字体文件存在，并且Matplotlib版本兼容")

global_logger.info("---------- 0.2 plt_back_chinese 模块执行完毕，Matplotlib 已完成中文支持的初始化设置")