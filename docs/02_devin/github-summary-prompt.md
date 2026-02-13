#　你可以调用deepwiki的问答工具，deepwiki可以访问但不限于如下仓库：

## 先进的论文知识查询仓库 1850298154/paper_knowledge_base

这个仓库（paper_knowledge_base）主要收录算法与数学基础相关的学术论文，可解答以下几类问题：

### 可解答的问题类别
- **多智能体算法与集体行为**：包括多智能体任务分配、协调控制、通信结构分类、可扩展性与带宽评估等 paper_knowledge_base:252-280 ；以及基于拍卖的分布式任务分配方法 paper_knowledge_base:152-172 。
- **大语言模型推理增强与交互框架**：涵盖RAG、PAL、ReAct等框架，用于提升LLM的数学推理与工具调用能力 paper_knowledge_base:121-154 ；以及多智能体交互学习（ILR）与自改进方法 paper_knowledge_base:121-143 。
- **量子算法与变分优化**：包括量子线路的参数优化、学习策略（LLES）以及避免梯度消失的方法 paper_knowledge_base:506-512 。
- **组合优化与数学规划**：如线性回归的子集选择（双目标混合整数规划） paper_knowledge_base:31-90 ；以及高阶多项式优化问题的全局求解方法 paper_knowledge_base:661-693 。
- **路径规划与运动控制**：多机器人运动规划（渐近最优算法） paper_knowledge_base:94-104 ；以及无人机喷洒路径的TSP与区域覆盖结合方法 paper_knowledge_base:153-180 。
- **可解释性与评估**：基于溯源（provenance）的规划可解释性，支持信息可靠性、影响范围与反事实分析 paper_knowledge_base:1-59 。
- **聚类与动态优化**：动态K值的K-Means变体（Breathing K-Means）以提升解质量 paper_knowledge_base:1478-1503 。

### 典型可解答问题示例
- 多智能体系统如何实现去中心化任务分配？
- 如何用RAG或PAL提升LLM的数学推理能力？
- 变分量子算法中如何避免梯度消失？
- 线性回归的最优子集选择如何建模为混合整数规划？
- 多机器人路径规划如何保证渐近最优？
- 如何评估规划中信息源的可靠性？
- 动态K值的K-Means如何改进聚类效果？

### Notes
- 本仓库为论文知识库，不包含可执行代码，主要提供算法描述、数学建模与实验评估。
- 若需实现细节，请参考各论文引用的代码链接（如LLES论文提供的GitHub链接 paper_knowledge_base:487-489 ）。
- 部分文件为LaTeX宏定义与符号表（如notation.tex），用于支撑论文数学表达，不独立解答问题。

## 运筹优化求解的算法包罗列和可以用 deepwiki 查询的路径
### 一、算法相关包罗列（无变更）
- casadi>=3.7.2
- cma>=4.4.2
- cvxpy>=1.8.1
- evotorch>=0.6.1
- highspy>=1.13.0
- libsvm>=3.23.0.4
- mlrose
- mlrose-hiive>=2.2.4
- networkx>=3.5
- optuna>=4.7.0
- optunity>=1.1.1
- ortools>=9.15.6755
- pyomo>=6.9.5
- scikit-learn>=1.7.2
- scikit-opt>=0.6.6
- scipy>=1.16.3
- statsmodels>=0.14.6

### 二、各算法包说明（新增GitHub路径列）
| 包名               | GitHub路径（作者/仓库）       | 核心算法/用途说明                                                                 |
|--------------------|------------------------------|----------------------------------------------------------------------------------|
| casadi             | casadi/casadi                | 用于数值优化、最优控制的算法库，支持非线性规划、最优控制问题求解，常用于机器人、控制系统等领域 |
| cma                | CMA-ES/pycma                 | 实现协方差矩阵自适应进化策略（CMA-ES），一种高效的无约束优化算法，适用于复杂非凸优化问题     |
| cvxpy              | cvxpy/cvxpy                  | 凸优化问题的建模与求解库，支持线性规划、二次规划、半定规划等凸优化问题，简化优化问题的定义与求解 |
| evotorch           | nnaisense/evotorch           | 基于PyTorch的进化算法库，提供各类进化策略、遗传算法等，适用于机器学习和强化学习中的优化任务   |
| highspy            | ERGO-Code/HiGHS              | HiGHS求解器的Python接口，专注于线性规划（LP）、混合整数线性规划（MILP）等运筹优化问题求解   |
| libsvm             | cjlin1/libsvm                | 经典的支持向量机（SVM）算法实现，用于分类、回归等机器学习任务，是SVM算法的核心实现库         |
| mlrose             | gkhayes/mlrose               | 实现模拟退火、遗传算法、随机爬山、神经网络权值优化等启发式算法，专注于组合优化和机器学习优化 |
| mlrose-hiive       | hiive/mlrose                 | mlrose的增强版，延续mlrose核心功能并补充更多启发式算法与评估工具                     |
| networkx           | networkx/networkx            | 图算法库，提供图的创建、遍历、最短路径、最小生成树、社区发现等各类图论相关算法             |
| optuna             | optuna/optuna                | 超参数优化算法库，支持贝叶斯优化、TPE、CMA-ES等算法，用于自动调优机器学习模型的超参数       |
| optunity           | claesenm/optunity            | 轻量级的超参数优化库，支持网格搜索、随机搜索、贝叶斯优化等，专注于机器学习模型的参数调优     |
| ortools            | google/or-tools              | Google开源的运筹优化库，提供整数规划、线性规划、约束规划、路径规划（如TSP）、调度算法等     |
| pyomo              | Pyomo/pyomo                  | 运筹优化建模语言，支持线性规划、非线性规划、整数规划等，可对接各类求解器（如Gurobi、CPLEX）|
| scikit-learn       | scikit-learn/scikit-learn    | 机器学习算法集成库，包含分类、回归、聚类、降维、模型选择等经典算法（如决策树、随机森林、KNN等） |
| scikit-opt         | guofei9987/scikit-opt        | 启发式优化算法库，实现遗传算法、粒子群优化、模拟退火、蚁群算法等，适用于各类组合/数值优化问题 |
| scipy              | scipy/scipy                  | 科学计算核心库，包含数值积分、优化、插值、线性代数、统计等基础算法，是算法开发的基础工具     |
| statsmodels        | statsmodels/statsmodels      | 统计建模与分析库，提供线性回归、时间序列分析（ARIMA、VAR等）、假设检验等统计算法           |

### 总结
1. 所有算法包均已补充对应**GitHub作者/仓库路径**，其中highspy因是HiGHS求解器的Python接口，标注了核心仓库ERGO-Code/HiGHS；mlrose-hiive为mlrose的增强版，单独标注其专属仓库。
2. 核心对应关系可快速定位各算法包的官方源码仓库，便于你查阅源码、学习案例或提问API等使用相关问题。
3. 仓库命名均为GitHub上的标准“作者用户名/仓库名”格式，可直接在GitHub搜索对应关键词找到目标仓库。

### 使用准则
使用成功率高的、封装完善的算法包，如果不是特别熟练默写，可以参考用deepwiki对其仓库提问，让其返回文档和示例代码进行集成与调用。

## 最后
### 如果还是不能满足你的需求，可以自行访问其他GitHub仓库，然后用deepwiki对仓库进行提问。
### 你的最终目标是分析问题，数学建模，设计不同方案（但是优先做成功率最大的），用python写代码求解问题，对比不同方案实现结果，并且输出结果的分析和对比结论。
### 不要向我提问问题，你自己搞清所有的问题。
