# 开源优化算法与传统机器学习/统计学习仓库 整理去重+详细说明
本文对所有仓库进行**去重整合**，按**组合优化/数学规划/元启发式优化**、**传统机器学习/统计学习（轻量直接求解）** 两大核心领域分类，每个仓库均明确**开发语言、deepwiki路径、核心功能、解决的问题**，信息清晰无冗余、易理解。

## 一、组合优化/数学规划/元启发式优化类
此类仓库聚焦各类优化问题求解，覆盖线性/整数规划、非线性规划、约束满足、群体智能优化等，适用于运筹学、工程优化、调度路由等场景，无重复仓库。

### 1. google/or-tools
- **开发语言**：核心C++，提供Python/C++/Java/.NET接口
- **deepwiki路径**：https://deepwiki.com/google/or-tools
- **核心功能**：工业级组合优化套件，内置CP‑SAT、GLOP、CBC等求解器；支持线性/整数规划、约束满足、图优化、网络流计算，集成TSP/VRP专用求解逻辑
- **解决的问题**：车辆路径规划（带时间窗/容量）、员工/设备排班、任务分配、旅行商问题（TSP）、生产调度、物流路径优化、网络流分配问题

### 2. coin-or/Cbc
- **开发语言**：C++，提供多语言调用接口
- **deepwiki路径**：https://deepwiki.com/coin-or/Cbc
- **核心功能**：COIN‑OR旗下经典分支定界求解器，专为大规模混合整数线性规划（MILP）设计，可独立使用也可作为其他建模框架的底层求解器
- **解决的问题**：大规模整数规划调度问题、供应链批量规划、资源分配优化、生产排程的整数约束优化问题

### 3. timefoldai/timefold-solver
- **开发语言**：Java/Kotlin，支持跨语言集成
- **deepwiki路径**：https://deepwiki.com/TimefoldAI/timefold-solver
- **核心功能**：约束规划+启发式算法求解器，针对NP难组合优化问题做了专门优化，主打智能调度与路径规划，支持自定义约束规则
- **解决的问题**：医院床位调度、会议排期、员工排班（多约束）、车辆路径规划、设备任务分配、物流配送路线优化

### 4. Pyomo/pyomo
- **开发语言**：Python
- **deepwiki路径**：https://deepwiki.com/Pyomo/pyomo
- **核心功能**：通用数学规划建模框架，支持线性规划（LP）、混合整数规划（MIP）、非线性规划（NLP）、随机规划；可无缝对接CBC、GLPK、Gurobi、CPLEX等第三方求解器，提供灵活的建模语法
- **解决的问题**：电力调度优化、供应链网络设计、工程设计参数优化、金融投资组合规划、随机场景下的资源分配问题

### 5. casadi/casadi
- **开发语言**：核心C++，提供Python/Matlab/C++接口
- **deepwiki路径**：https://deepwiki.com/casadi/casadi
- **核心功能**：非线性优化+自动微分一体化工具，支持最优控制、NLP/MINLP（混合整数非线性规划）求解；对接IPOPT、BONMIN、SNOPT等底层求解器，内置自动微分引擎简化梯度计算
- **解决的问题**：机械臂轨迹优化、模型预测控制（MPC）、化工过程优化、机器人运动规划、参数识别与系统辨识问题

### 6. coin-or/Ipopt
- **开发语言**：C++/Fortran，提供第三方Python接口
- **deepwiki路径**：https://deepwiki.com/coin-or/Ipopt
- **核心功能**：内点法专用求解器，主打大规模非线性规划（NLP）问题，对连续变量的非线性优化支持性极佳，是工程领域非线性优化的主流工具
- **解决的问题**：化工流程参数优化、航空航天工程设计优化、机械结构优化、连续变量的复杂目标函数寻优问题

### 7. ERGO-Code/HiGHS
- **开发语言**：C++，提供Python/C++接口
- **deepwiki路径**：https://deepwiki.com/ERGO-Code/HiGHS
- **核心功能**：高性能线性/混合整数规划求解器，针对大规模LP/MIP问题做了性能优化，接口简洁，支持并行计算
- **解决的问题**：大规模线性规划的资源分配、混合整数规划的生产调度、物流网络的线性优化、大规模数据下的整数约束规划问题

### 8. guofei9987/scikit-opt
- **开发语言**：Python
- **deepwiki路径**：https://deepwiki.com/guofei9987/scikit-opt
- **核心功能**：Python群体智能优化库，集成PSO（粒子群）、GA（遗传算法）、SA（模拟退火）、DE（差分进化）、ACO（蚁群算法）等经典元启发式算法，适配连续优化和组合优化双场景
- **解决的问题**：函数极值寻优、车间调度、TSP问题、参数调优、无梯度的黑盒优化问题、复杂约束下的组合寻优问题

### 9. nnaisense/evotorch
- **开发语言**：Python（基于PyTorch）
- **deepwiki路径**：https://deepwiki.com/nnaisense/evotorch
- **核心功能**：PyTorch生态的进化计算库，融合进化算法与深度学习，支持神经进化、黑盒优化，兼容自动微分和GPU加速，可处理带约束的优化问题
- **解决的问题**：强化学习策略优化、神经网络超参数搜索、深度学习模型结构优化、高维黑盒优化问题、GPU加速的大规模进化优化问题

### 10. PyGMO/PyGMO2
- **开发语言**：C++/Python
- **deepwiki路径**：https://deepwiki.com/esa/pygmo2
- **核心功能**：并行全局优化框架，集成数十种全局优化算法，支持多线程/分布式并行计算，适配大规模、高维的全局优化问题
- **解决的问题**：高维非凸函数寻优、大规模工程全局优化、多目标并行优化问题、分布式环境下的全局寻优问题

### 11. scipy/scipy
- **开发语言**：核心C/Fortran，提供Python接口
- **deepwiki路径**：https://deepwiki.com/scipy/scipy
- **核心功能**：Python科学计算核心库，`scipy.optimize`模块包含基础优化函数，支持LP、NLP、最小二乘、根查找、无约束/有约束的基础优化，是轻量优化的入门工具
- **解决的问题**：曲线拟合、简单的参数寻优、基础的约束/无约束优化问题、数据拟合中的最小二乘求解、简单的数学规划问题

### 12. cvxpy/cvxpy
- **开发语言**：Python
- **deepwiki路径**：https://deepwiki.com/cvxpy/cvxpy
- **核心功能**：Python凸优化专用建模语言，支持线性规划（LP）、二次规划（QP）、二阶锥规划（SOCP）等凸优化问题建模，对接CLP、ECOS、SCS等底层求解器，自动验证凸性
- **解决的问题**：投资组合优化、信号处理与恢复、机器学习正则化优化、凸约束下的工程设计问题、金融风险度量优化

### 13. CMA-ES/pycma
- **开发语言**：Python
- **deepwiki路径**：https://deepwiki.com/CMA-ES/pycma
- **核心功能**：CMA-ES（协方差矩阵自适应进化策略）无梯度优化库，专为高维、非凸、多模态的连续优化问题设计，支持并行计算
- **解决的问题**：高维神经网络调参、工程设计的高维连续寻优、多模态函数极值求解、无梯度的黑盒连续优化问题

### 14. optuna/optuna
- **开发语言**：Python
- **deepwiki路径**：https://deepwiki.com/optuna/optuna
- **核心功能**：Python超参数优化专用框架，支持TPE、CMA‑ES、贝叶斯优化等多种优化算法，适配各类机器学习/深度学习框架，提供可视化和分布式调参功能
- **解决的问题**：机器学习模型超参数搜索、LLM提示词优化、多目标优化问题、深度学习模型训练的超参调优、分布式超参数寻优

### 15. facebookresearch/optimizers
- **开发语言**：Python（基于PyTorch）
- **deepwiki路径**：https://deepwiki.com/facebookresearch/optimizers
- **核心功能**：PyTorch生态的高级优化器库，集成Distributed Shampoo等先进优化算法，优化深度学习模型的训练效率，提升模型收敛速度和精度
- **解决的问题**：Transformer模型训练优化、ImageNet等大规模数据集的模型训练、深度学习模型的梯度下降优化、分布式训练的优化器适配问题

## 二、传统机器学习/统计学习类（轻量直接求解，无大规模训练）
此类仓库聚焦**基础分类/统计推断**，核心特点是**基于求解器直接求解**、无需大规模模型训练，覆盖经典ML分类、统计学习、优化+分类结合、专用求解器直用等场景，无重复仓库。

### 1. scikit-learn
- **开发语言**：核心Cython/C++，提供Python接口
- **deepwiki路径**：https://deepwiki.com/scikit-learn/scikit-learn
- **核心功能**：经典通用传统机器学习库，覆盖所有基础分类/回归/聚类算法，所有模型均为“拟合-预测”极简流程，底层集成各类专用求解器（如SVM的SMO、逻辑回归的拟牛顿法），支持小数据集秒级求解
- **解决的问题**：鸢尾花等数据集的分类问题、文本简单分类、数值特征的二分类/多分类问题、客户分群后的分类预测、简单的工业数据分类识别

### 2. statsmodels
- **开发语言**：Python
- **deepwiki路径**：https://deepwiki.com/statsmodels/statsmodels
- **核心功能**：聚焦统计学习的Python库，基于统计求解器实现分类/回归，输出详细的统计参数（系数、p值、置信区间），支持逻辑回归、有序分类、多分类逻辑回归，无梯度下降训练流程
- **解决的问题**：需要统计推断的分类问题、基于统计显著性的二分类/多分类预测、社会科学数据的分类分析、分类模型的参数显著性检验

### 3. mlrose
- **开发语言**：Python
- **deepwiki路径**：https://deepwiki.com/gkhayes/mlrose
- **核心功能**：将机器学习问题转化为优化问题求解的Python库，集成模拟退火、遗传算法、随机爬山等经典优化求解器，通过优化目标函数实现分类/回归，可清晰体现“优化+ML”的底层逻辑
- **解决的问题**：简单神经网络的分类问题、基于启发式优化的特征选择+分类、小数据集的优化驱动分类、理解优化算法在ML中的应用的教学/实践问题

### 4. Optunity
- **开发语言**：Python
- **deepwiki路径**：https://deepwiki.com/claesenm/optunity
- **核心功能**：优化求解器+ML分类一体化库，集成贝叶斯优化、网格搜索、随机搜索等超参优化算法，自动调优传统ML分类器超参并直接求解分类模型，一键完成“超参优化+分类预测”
- **解决的问题**：无需手动调参的SVM/决策树分类问题、小数据集的贝叶斯优化驱动分类、传统ML模型的快速超参调优+分类预测

### 5. LIBSVM
- **开发语言**：C++，提供Python/命令行接口
- **deepwiki路径**：https://deepwiki.com/cjlin1/libsvm
- **核心功能**：经典轻量级SVM专用求解器，底层基于SMO算法，无多余依赖，可直接通过命令行/Python接口输入小数据集求解分类/回归，支持自定义SVM核函数
- **解决的问题**：小数据集的SVM二分类/多分类问题、无框架依赖的轻量分类需求、快速的SVM求解验证问题

### 6. PyMC
- **开发语言**：Python
- **deepwiki路径**：https://deepwiki.com/pymc-devs/pymc
- **核心功能**：贝叶斯概率编程库，基于MCMC（马尔可夫链蒙特卡洛）求解器构建贝叶斯模型，通过采样后验分布实现概率分类，输出分类结果的概率分布，支持贝叶斯逻辑回归等分类模型
- **解决的问题**：需要概率推断的分类问题、贝叶斯逻辑回归分类、小数据集的统计概率分类、分类结果的不确定性评估问题

## 三、辅助资源仓库
### 1. or-tools/awesome_or_tools
- **开发语言**：无（案例集，含多语言代码）
- **deepwiki路径**：https://deepwiki.com/or-tools/awesome_or_tools
- **核心功能**：Google OR-Tools的社区精选案例集，整理了各类基于OR-Tools的实际应用案例，覆盖调度、路由、分配、规划等场景
- **解决的问题**：为OR-Tools的实际使用提供参考案例，解决开发者不知道如何用OR-Tools落地具体优化问题的难题

### 2. Pyomo/pyomo-examples
- **开发语言**：Python（示例代码）
- **deepwiki路径**：https://deepwiki.com/Pyomo/pyomo-tutorials
- **核心功能**：Pyomo官方示例库+教程，包含各类数学规划建模的模板、行业应用案例和Jupyter Notebook教程，覆盖电力、供应链、工程设计等领域
- **解决的问题**：为Pyomo建模提供实战模板，解决开发者不会用Pyomo构建具体优化问题模型的难题
















# 补充Demo资源仓库（按原分类体系扩展）
以下新增Demo资源均围绕“可直接学习复用的代码案例”展开，覆盖原两大核心领域+辅助资源，每个仓库明确Demo的核心场景、代码形式和学习价值，便于你的agent直接参考写代码。

## 一、组合优化/数学规划/元启发式优化类（补充Demo仓库）
### 16. or-tools/docs
- **开发语言**：Python/C++/Java（多语言Demo）
- **deepwiki路径**：https://deepwiki.com/google/or-tools/docs
- **核心功能**：OR-Tools官方文档+配套完整Demo库，包含TSP/VRP/排班/调度等场景的可运行代码，每个Demo均有“问题定义→建模→求解→结果可视化”全流程，代码注释详细，覆盖基础到工业级场景
- **解决的问题**：学习OR-Tools的工程化建模方法、快速复现经典优化场景（如带时间窗的VRP）、掌握优化问题的代码实现范式
- **Demo核心场景**：
  - 基础TSP求解（含可视化）
  - 带容量+时间窗的车辆路径规划（CVRPTW）
  - 员工多约束排班（班次+技能+休息规则）
  - 生产任务调度（机器约束+工期约束）

### 17. Pyomo/pyomo-examples（补充细化）
- **开发语言**：Python（Jupyter Notebook/脚本）
- **deepwiki路径**：https://deepwiki.com/Pyomo/pyomo-tutorials
- **核心功能**：在原有基础上，新增“行业级完整Demo”，包含电力机组组合优化、供应链网络设计、碳排放约束下的生产规划等端到端案例，每个Demo均提供“数据输入→模型定义→求解器调用→结果分析”全代码，适配不同求解器（CBC/GLPK/Gurobi）
- **解决的问题**：掌握Pyomo的灵活建模语法、学习不同行业优化问题的建模思路、适配第三方求解器的代码写法
- **Demo核心场景**：
  - 线性规划：电力系统经济调度（含负荷约束）
  - 混合整数规划：仓库选址+配送路径联合优化
  - 非线性规划：化工反应器参数优化（对接Ipopt）

### 18. guofei9987/scikit-opt/examples
- **开发语言**：Python
- **deepwiki路径**：https://deepwiki.com/guofei9987/scikit-opt/examples
- **核心功能**：scikit-opt官方示例库，覆盖所有内置算法的基础用法+实战场景，每个Demo均对比不同算法的求解效果，包含“参数调优→约束处理→结果可视化”全流程代码
- **解决的问题**：学习群体智能算法的代码实现、掌握组合优化/连续优化的适配技巧、对比不同算法的求解效率
- **Demo核心场景**：
  - PSO：神经网络超参数寻优
  - GA：车间作业调度（JSP）
  - SA：TSP问题求解（含动态邻域搜索）
  - DE：高维函数极值寻优（对比CMA-ES）

### 19. casadi/casadi/examples
- **开发语言**：Python/Matlab/C++
- **deepwiki路径**：https://deepwiki.com/casadi/casadi/examples
- **核心功能**：CasADi官方示例库，聚焦最优控制和非线性规划的工程化Demo，包含自动微分、求解器对接、轨迹优化等场景的完整代码，适配机器人、化工、控制等领域
- **解决的问题**：学习非线性优化+自动微分的代码结合、掌握最优控制问题的建模方法、对接Ipopt/SNOPT等求解器的工程代码
- **Demo核心场景**：
  - 机械臂轨迹优化（MPC模型预测控制）
  - 化工过程动态优化（含约束处理）
  - 车辆路径跟踪优化（非线性约束）
  - 参数识别（基于最小二乘的系统辨识）

### 20. optuna/optuna-examples
- **开发语言**：Python
- **deepwiki路径**：https://deepwiki.com/optuna/optuna-examples
- **核心功能**：Optuna官方示例库，覆盖超参数优化的全场景Demo，包含单机/分布式调参、多目标优化、与主流ML框架（sklearn/PyTorch）的集成代码，每个Demo均有可视化分析模块
- **解决的问题**：学习超参数优化的工程代码、掌握分布式调参的实现方法、适配不同ML模型的调参逻辑
- **Demo核心场景**：
  -  sklearn模型（SVM/随机森林）超参调优
  -  PyTorch模型（CNN）的学习率+批次大小调优
  -  多目标优化：精度+推理速度双目标调参
  -  贝叶斯优化vs TPE vs CMA-ES效果对比

## 二、传统机器学习/统计学习类（补充Demo仓库）
### 7. scikit-learn/scikit-learn.github.io
- **开发语言**：Python（Jupyter Notebook）
- **deepwiki路径**：https://deepwiki.com/scikit-learn/scikit-learn.github.io
- **核心功能**：scikit-learn官方示例库，覆盖所有基础算法的“数据预处理→模型训练→评估→调参”全流程Demo，包含小数据集（鸢尾花/红酒）和中等数据集（波士顿房价/新闻分类）的可运行代码，注释详细且适配新手
- **解决的问题**：学习传统ML的标准化代码流程、掌握不同分类/回归算法的实现细节、理解特征工程的代码落地
- **Demo核心场景**：
  - 二分类：逻辑回归（含特征选择+交叉验证）
  - 多分类：SVM（不同核函数对比）
  - 回归：随机森林（含特征重要性分析）
  - 聚类：K-Means（含肘部法则选K值）

### 8. statsmodels/statsmodels-examples
- **开发语言**：Python
- **deepwiki路径**：https://deepwiki.com/statsmodels/statsmodels.github.io
- **核心功能**：statsmodels官方示例库，聚焦统计学习的“建模→统计推断→可视化”全流程Demo，每个案例均输出详细的统计参数（p值/置信区间/残差分析），适配社会科学、金融等需要统计解释的场景
- **解决的问题**：学习统计驱动的分类/回归代码、掌握统计参数的解读与输出、实现分类模型的显著性检验
- **Demo核心场景**：
  - 逻辑回归：信用卡违约预测（含参数显著性分析）
  - 有序分类：客户满意度分级预测（Probit模型）
  - 多分类：产品故障类型识别（多项Logit模型）

### 9. gkhayes/mlrose/examples
- **开发语言**：Python
- **deepwiki路径**：https://deepwiki.com/gkhayes/mlrose/examples
- **核心功能**：mlrose官方示例库，将ML问题转化为优化问题的核心Demo，包含“优化算法选择→目标函数定义→分类/回归求解”全流程，对比不同优化算法在ML场景的效果
- **解决的问题**：理解“优化+ML”的底层代码逻辑、掌握启发式算法在ML中的应用、实现优化驱动的特征选择
- **Demo核心场景**：
  - 模拟退火：简单神经网络分类（手写数字识别）
  - 遗传算法：特征选择+SVM分类（乳腺癌数据集）
  - 随机爬山：决策树超参优化（分类精度提升）

### 10. cjlin1/libsvm/tools
- **开发语言**：Python/C++/命令行脚本
- **deepwiki路径**：https://deepwiki.com/cjlin1/libsvm/tools
- **核心功能**：LIBSVM配套工具库+Demo，包含小数据集分类的极简代码，支持命令行快速求解和Python接口调用，提供数据格式转换、参数调优、结果评估的辅助脚本
- **解决的问题**：学习轻量SVM的无框架代码实现、掌握小数据集的快速分类求解、适配自定义核函数的代码写法
- **Demo核心场景**：
  - 命令行：鸢尾花数据集二分类（快速验证）
  - Python接口：文本分类（TF-IDF特征+SVM）
  - 自定义核函数：高斯核SVM分类（对比线性核）

### 11. pymc-devs/pymc-examples
- **开发语言**：Python
- **deepwiki路径**：https://deepwiki.com/pymc-devs/pymc-examples
- **核心功能**：PyMC官方示例库，聚焦贝叶斯分类的全流程Demo，包含MCMC采样、后验分布可视化、概率分类结果解读的完整代码，适配小数据集的概率推断场景
- **解决的问题**：学习贝叶斯分类的代码实现、掌握概率分布的采样与分析、评估分类结果的不确定性
- **Demo核心场景**：
  - 贝叶斯逻辑回归：疾病诊断分类（输出患病概率）
  - 贝叶斯多分类：手写数字识别（概率分布输出）
  - 分层贝叶斯模型：多组数据的联合分类

## 三、辅助资源仓库（补充Demo类）
### 4. HiGHS/HiGHS/examples
- **开发语言**：C++/Python
- **deepwiki路径**：https://deepwiki.com/ERGO-Code/HiGHS/examples
- **核心功能**：HiGHS求解器官方示例库，包含LP/MIP问题的极简调用代码，支持并行计算、大规模数据求解的Demo，对比HiGHS与Cbc/GLPK的求解效率
- **解决的问题**：学习高性能求解器的代码调用、掌握并行优化的实现方法、适配大规模规划问题的代码写法
- **Demo核心场景**：
  - 并行LP求解：物流网络资源分配（10万+变量）
  - MIP求解：工厂生产批量规划（整数约束）
  - Python接口快速验证：小规模LP问题（对比scipy）

### 5. PyGMO/PyGMO2/examples
- **开发语言**：Python/C++
- **deepwiki路径**：https://deepwiki.com/esa/pygmo2/examples
- **核心功能**：PyGMO2官方示例库，聚焦并行全局优化的Demo，包含多线程/分布式求解、多目标优化、高维函数寻优的完整代码，适配工程全局优化场景
- **解决的问题**：学习并行优化的代码实现、掌握多目标优化的求解逻辑、适配高维全局寻优问题
- **Demo核心场景**：
  - 多线程全局优化：高维非凸函数寻优
  - 分布式优化：工程设计参数全局寻优
  - 多目标优化：成本+效率双目标规划

### 总结
1. 新增Demo仓库均聚焦**可运行的完整代码**，覆盖“问题定义→建模→求解→结果分析”全流程，适配你的agent直接学习复用；
2. 优化类Demo侧重**不同求解器对接、算法对比、工程约束处理**，ML类Demo侧重**统计推断、优化+ML结合、概率分类**；
3. 辅助Demo仓库提供**标准化调用模板**，降低agent学习不同求解器/库的代码适配成本。