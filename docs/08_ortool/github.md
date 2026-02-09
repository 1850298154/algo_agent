以下是覆盖组合优化、数学规划、启发式/进化算法、深度学习优化等领域的强大开源优化算法GitHub仓库，按类型速览如下：
### 一、组合优化/运筹学（LP/MIP/CP/VRP等）
1. **google/or-tools**（Apache-2.0）：Google工业级组合优化套件，含CP‑SAT、GLOP、CBC等求解器；支持线性/整数规划、约束满足、VRP、调度、图优化。https://github.com/google/or-tools
2. **coin-or/Cbc**（EPL-1.0）：COIN‑OR分支定界求解器，高效解大规模MILP。https://github.com/coin-or/Cbc
3. **timefoldai/timefold-solver**（Apache-2.0）：Java/Kotlin约束规划与启发式求解器；擅长排班、车辆路径、任务分配。https://github.com/TimefoldAI/timefold-solver
4. **Pyomo/pyomo**（BSD-3-Clause）：Python建模框架，支持LP/MIP/NLP/随机规划，适配CBC、GLPK、Gurobi等。https://github.com/Pyomo/pyomo

### 二、数学规划/非线性优化（NLP/QP/MINLP等）
1. **casadi/casadi**（LGPL-3.0）：非线性优化与自动微分工具，支持最优控制与NLP/MINLP；对接IPOPT、BONMIN等。https://github.com/casadi/casadi
2. **coin-or/Ipopt**（EPL-1.0）：内点法求解大规模非线性规划，工程优化常用。https://github.com/coin-or/Ipopt
3. **ERGO-Code/HiGHS**（MIT）：高性能线性/混合整数规划求解器，C++/Python接口。https://github.com/ERGO-Code/HiGHS

### 三、元启发式/群体智能优化
1. **guofei9987/scikit-opt**（MIT）：Python群体智能库，含PSO、GA、SA、DE、ACO等，适配组合与连续优化。https://github.com/guofei9987/scikit-opt
2. **nnaisense/evotorch**（Apache-2.0）：PyTorch进化计算库，支持神经进化与黑盒优化。https://github.com/nnaisense/evotorch
3. **PyGMO/PyGMO2**（LGPL-3.0）：并行优化框架，集成多种全局优化算法，适配大规模问题。https://github.com/esa/pygmo2

### 四、深度学习优化（模型训练/超参调优）
1. **facebookresearch/optimizers**（MIT）：PyTorch优化器库，含Distributed Shampoo等先进算法。https://github.com/facebookresearch/optimizers
2. **CMA-ES/pycma**（BSD-3-Clause）：Python实现CMA‑ES，适合无梯度高维非凸优化。https://github.com/CMA-ES/pycma
3. **microsoft/AgentLightning**（MIT）：智能体提示词优化框架，基于强化学习优化LLM提示词。https://github.com/microsoft/AgentLightning

### 五、其他常用优化库
1. **scipy/scipy**（BSD-3-Clause）：科学计算核心库，scipy.optimize含LP、NLP等基础优化函数。https://github.com/scipy/scipy
2. **cvxpy/cvxpy**（Apache-2.0）：Python凸优化建模语言，对接CLP、ECOS、SCS等求解器。https://github.com/cvxpy/cvxpy

需要我按你的问题类型（如MIP/VRP/NLP/深度学习调参）给你筛出3个最优先的仓库并附快速上手示例吗？



以下按领域列出**高通用性+丰富示例+完善文档**的开源优化库，覆盖组合优化、数学规划、元启发式、深度学习调参等场景，每个都附核心能力、示例与文档入口。

### 一、组合优化/运筹学（LP/MIP/CP/VRP/调度）
1. **google/or-tools**（Apache-2.0）
    - 核心：工业级组合优化套件，含**CP‑SAT**、**GLOP**、**CBC**等求解器；支持线性/整数规划、约束满足、VRP、TSP、任务分配、图优化等。
    - 示例：官方Python/C++/Java/.NET示例覆盖TSP、VRP（带时间窗/容量）、排班、网络流；提供**Colab可直接运行**。
    - 文档：开发者指南+API参考+Awesome OR‑Tools社区案例集。
    - 仓库：https://github.com/google/or-tools

2. **timefoldai/timefold-solver**（Apache-2.0）
    - 核心：Java/Kotlin约束规划+启发式求解器；擅长**排班、车辆路径、任务分配**等NP难问题。
    - 示例：含员工排班、医院床位、会议排期、VRP等端到端示例；提供**快速入门教程**与实战项目。
    - 文档：官方指南+示例库+社区论坛。
    - 仓库：https://github.com/TimefoldAI/timefold-solver

3. **Pyomo/pyomo**（BSD-3-Clause）
    - 核心：Python建模框架，支持**LP/MIP/NLP/随机规划**；适配CBC、GLPK、Gurobi、CPLEX等求解器。
    - 示例：官方教程含电力调度、供应链优化、工程设计等；附**Jupyter Notebook**。
    - 文档：完整用户指南+API文档+案例库。
    - 仓库：https://github.com/Pyomo/pyomo

### 二、数学规划/非线性优化（NLP/QP/MINLP）
1. **casadi/casadi**（LGPL-3.0）
    - 核心：非线性优化+自动微分工具，支持最优控制与**NLP/MINLP**；对接IPOPT、BONMIN、SNOPT等。
    - 示例：机械臂轨迹优化、模型预测控制（MPC）、参数识别；含Python/Matlab/C++示例。
    - 文档：用户手册+API参考+教程视频。
    - 仓库：https://github.com/casadi/casadi

2. **coin-or/Ipopt**（EPL-1.0）
    - 核心：内点法求解大规模**非线性规划（NLP）**，工程优化常用。
    - 示例：官方C++/Fortran示例+第三方Python接口案例（如Pyomo集成）。
    - 文档：详细用户指南+API文档+FAQ。
    - 仓库：https://github.com/coin-or/Ipopt

3. **ERGO-Code/HiGHS**（MIT）
    - 核心：高性能**线性/混合整数规划**求解器，C++/Python接口，支持大规模问题。
    - 示例：LP/MIP基准测试+Python快速建模示例；附CMake编译指南。
    - 文档：ReadTheDocs+API参考+示例库。
    - 仓库：https://github.com/ERGO-Code/HiGHS

### 三、元启发式/群体智能优化（无梯度/黑盒）
1. **guofei9987/scikit-opt**（MIT）
    - 核心：Python群体智能库，含**PSO、GA、SA、DE、ACO**等；适配连续/组合优化、函数极值、TSP等。
    - 示例：函数优化、TSP、车间调度、参数调优；附详细注释与对比实验。
    - 文档：GitHub Wiki+示例代码+中文教程。
    - 仓库：https://github.com/guofei9987/scikit-opt

2. **nnaisense/evotorch**（Apache-2.0）
    - 核心：PyTorch进化计算库，支持**神经进化、黑盒优化**；兼容自动微分与GPU加速。
    - 示例：强化学习策略优化、超参数搜索、约束优化；含Colab演示。
    - 文档：ReadTheDocs+API参考+教程。
    - 仓库：https://github.com/nnaisense/evotorch

3. **CMA-ES/pycma**（BSD-3-Clause）
    - 核心：**CMA‑ES**无梯度优化，适合高维非凸、多模态连续问题；支持并行计算。
    - 示例：函数优化、神经网络调参、工程设计；附命令行工具与Python脚本。
    - 文档：用户指南+API参考+案例集。
    - 仓库：https://github.com/CMA-ES/pycma

### 四、深度学习优化（超参调优/提示词优化）
1. **optuna/optuna**（MIT）
    - 核心：Python超参数优化框架，支持**TPE、CMA‑ES、贝叶斯优化**；适配PyTorch/TensorFlow/XGBoost等。
    - 示例：分类模型调参、LLM提示词优化、多目标优化；含可视化与分布式训练示例。
    - 文档：官方指南+API参考+集成教程。
    - 仓库：https://github.com/optuna/optuna

2. **facebookresearch/optimizers**（MIT）
    - 核心：PyTorch优化器库，含**Distributed Shampoo**等先进算法；提升模型训练效率。
    - 示例：ImageNet训练、Transformer调优；附与AdamW等传统优化器对比实验。
    - 文档：GitHub README+论文链接+使用示例。
    - 仓库：https://github.com/facebookresearch/optimizers

### 五、凸优化/通用数学工具
1. **cvxpy/cvxpy**（Apache-2.0）
    - 核心：Python凸优化建模语言，对接**CLP、ECOS、SCS**等求解器；支持LP、QP、SOCP等。
    - 示例：投资组合优化、信号处理、机器学习正则化；含Jupyter Notebook教程。
    - 文档：用户指南+API参考+案例库。
    - 仓库：https://github.com/cvxpy/cvxpy

2. **scipy/scipy**（BSD-3-Clause）
    - 核心：科学计算库，**scipy.optimize**模块含LP、NLP、最小二乘等基础优化函数。
    - 示例：曲线拟合、约束优化、根查找；附Python交互式示例。
    - 文档：官方教程+API参考+示例库。
    - 仓库：https://github.com/scipy/scipy

### 六、辅助资源（示例/教程仓库）
- **or-tools/awesome_or-tools**：社区精选OR‑Tools案例，覆盖调度、路由、分配等场景；https://github.com/or-tools/awesome_or_tools
- **Pyomo/pyomo-examples**：官方示例库，含建模模板与行业应用；https://github.com/Pyomo/pyomo-examples

需要我从上面挑3个最符合你场景的库，各给一段可直接运行的Python示例代码吗？