# 修复点1：替换自定义日志为标准logging（避免依赖缺失报错）
import logging

# 配置标准日志
logging.basicConfig(level=logging.INFO)
global_logger = logging.getLogger(__name__)

global_logger.info("---------- 0.1 初始化Matplotlib，配置中文和后端")
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

# ① 无GUI环境（子线程/服务器）启用Agg后端，有GUI环境可注释
# 若在本地桌面运行（有GUI），建议注释这行；若在后台/子线程运行，取消注释
# matplotlib.use("Agg")  

# ② 修复：增加多系统中文备选字体（兼容Windows/Mac/Linux）
plt.rcParams["font.sans-serif"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题
global_logger.info("---------- 0.2 Matplotlib中文支持初始化完成")

# 初始化核心参数
p = 0.5  # 事件A发生的整体概率（如“顾客购买商品”的总概率）
n = 100  # 样本数量（代码中未实际使用，保留仅作注释参考）

# 创建画布：2行1列的子图，设置尺寸
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
plt.subplots_adjust(left=0.1, bottom=0.25)  # 预留滑块空间

# 核心函数1：计算信息熵 H(p)
def calculate_entropy(p):
    # 兼容数组/单个值输入：若p是数组，用numpy向量化计算（更高效）
    if isinstance(p, np.ndarray):
        # 避免log2(0)报错：概率为0/1时熵为0，否则按公式计算
        return np.where((p == 0) | (p == 1), 0, -p * np.log2(p) - (1 - p) * np.log2(1 - p))
    # 单个值的情况
    if p == 0 or p == 1:
        return 0
    return -p * np.log2(p) - (1 - p) * np.log2(1 - p)

# 核心函数2：计算信息增益 IG(D,A) = H(D) - H(D|A)
def calculate_info_gain(p, split_p=0.5):
    """
    参数说明：
    - p: 事件A的整体概率（划分前的总概率）
    - split_p: 特征划分后第一部分数据的占比（默认均分，即0.5）
    """
    # 生成子节点1的概率范围（0.01~0.99，避免0/1）
    p1 = np.linspace(0.01, 0.99, 100)
    # 修复点2：修正注释（原注释错误，实际是保持整体概率=p）
    # 推导：整体概率p = split_p*p1 + (1-split_p)*p2 → p2 = (p - split_p*p1)/(1-split_p)
    p2 = (p - split_p * p1) / (1 - split_p)
    p2 = np.clip(p2, 0.01, 0.99)  # 限制p2范围，避免log2(0)
    
    # 计算划分前的总熵 H(D)
    h_d = calculate_entropy(p)
    # 计算划分后的条件熵 H(D|A) = 加权平均子节点熵
    h_da = split_p * calculate_entropy(p1) + (1 - split_p) * calculate_entropy(p2)
    # 信息增益 = 总熵 - 条件熵
    return h_d - h_da

# ========== 绘制第一张图：信息熵随事件概率的变化 ==========
p_values = np.linspace(0.01, 0.99, 100)  # 概率从0.01到0.99
entropy_values = calculate_entropy(p_values)  # 修复点3：直接用数组计算（更高效，替代列表推导）
entropy_line, = ax1.plot(p_values, entropy_values, 'b-', label='信息熵 H(p)')
ax1.set_xlabel('事件概率 p')
ax1.set_ylabel('信息熵值')
ax1.set_title('信息熵随事件概率的变化（p=0.5时熵最大）')
ax1.legend()
ax1.grid(True, alpha=0.3)  # 增加网格透明度，更美观

# ========== 绘制第二张图：信息增益随子节点概率的变化 ==========
p1_values = np.linspace(0.01, 0.99, 100)
info_gain_values = calculate_info_gain(p)  # 初始信息增益
gain_line, = ax2.plot(p1_values, info_gain_values, 'r-', label=f'信息增益 IG (整体p={p:.2f})')
ax2.set_xlabel('子节点1事件概率 p1')
ax2.set_ylabel('信息增益值')
ax2.set_title('信息增益随子节点概率的变化（子节点差异越大，增益越高）')
ax2.legend()
ax2.grid(True, alpha=0.3)

# ========== 添加交互滑块：控制整体概率p ==========
axcolor = 'lightgoldenrodyellow'  # 滑块背景色
# 创建滑块位置：[左, 下, 宽, 高]
ax_p = plt.axes([0.1, 0.1, 0.8, 0.03], facecolor=axcolor)
# 滑块参数：轴对象、标签、最小值、最大值、初始值
slider_p = Slider(ax_p, '整体事件概率 p', 0.01, 0.99, valinit=p)

# 滑块更新函数：拖动滑块时实时更新信息增益曲线
def update(val):
    p_new = slider_p.val  # 获取滑块当前值
    # 重新计算信息增益
    new_gain = calculate_info_gain(p_new)
    # 更新曲线数据
    gain_line.set_ydata(new_gain)
    # 更新图例标签
    gain_line.set_label(f'信息增益 IG (整体p={p_new:.2f})')
    ax2.legend()
    # 刷新画布
    fig.canvas.draw_idle()

# 绑定滑块事件：滑块值变化时调用update函数
slider_p.on_changed(update)

# 显示图形（若启用Agg后端，需替换为plt.savefig("xxx.png")）
plt.show()