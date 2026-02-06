
# DeepWiki Q&A with Code Context for Repository: 1850298154/HULK


## Q1

整个项目中使用了哪些求解器，给我全部都罗列出来，使用哪些外界拥有的库啊什么的，包括了求解器还有画图工具，然后告诉我用了他画了哪些图，哪些类型的图，给我分别特别详细的罗列。什么求解器、优化器等等，第三方的画图的等等


### Answer

您询问的是 HULK 项目中使用的求解器、优化器和可视化工具。让我详细列举项目中使用的所有第三方库及其用途。

## 求解器和优化器

### 1. **OR-Tools (Google OR-Tools)**
项目主要使用 OR-Tools 的线性规划求解器 SCIP: HULK:14-14 

**使用场景:**
- **MILP 任务分配** (`assign_uav_to_coalition_new`): 最小化 makespan,将智能体分配到联盟 HULK:1288-1332 
- **c_milp_1 规划器**: VRP 风格的任务序列规划,使用 MTZ 约束消除子回路 HULK:1632-1702 
- **c_milp_2 规划器**: 目标级别的智能体-目标分配 HULK:1783-1828 
- **c_milp_1_agent_assign_seq_k**: 带序列约束的 VRP 规划 HULK:1910-2054 
- **采样规划器** (`grow_sample_node`, `grow_sample_node_target`): 增量式任务分配 HULK:2234-2240 HULK:2405-2411 
- **最小智能体需求计算** (`calc_min_agent_demand`): 计算任务所需最少智能体数量 HULK:1413-1462 
- **运动规划** (`MILPlanner`): 多智能体路径规划 HULK:105-123 

### 2. **SciPy**
使用 `scipy.optimize.linprog` 进行线性规划 HULK:13-13 

**使用场景:**
- **LP 智能体分配** (`assign_uav_to_coalition`): 最小化旅行时间的线性规划 HULK:1192-1192 

## 可视化工具

### 1. **Matplotlib**
主要的绘图库 HULK:58-141 

**绘制的图表类型:**

#### (1) **堆叠面积图 (Stackplot)**
- `draw_stack_fig`: 显示智能体状态分布(导航/等待/执行)和任务数量随时间变化 HULK:81-132 
- `draw_stack_fig_alpha`: 带任务完成率的智能体状态图 HULK:694-738 

#### (2) **甘特图 (Gantt Chart)**
- `draw_task_gantt_fig`: 联盟任务执行时间线 HULK:212-342 
- `draw_task_real_time_gantt_fig`: 任务实时执行阶段(发布/导航/同步/执行) HULK:345-429 

#### (3) **直方图 (Histogram)**
- `draw_response_time_fig`: 响应时间分布 HULK:201-209 

#### (4) **茎叶图 (Stem Plot)**
- `draw_planning_time_fig`: 重规划时间成本 HULK:667-680 

#### (5) **实时仿真可视化**
在 `SimulationInterfaceMatplotlib` 和 `SimulationInterfaceMatplotlib2` 中: HULK:10-16 
- **散点图 (Scatter)**: 智能体位置、目标位置 HULK:417-419 
- **多边形/圆形填充**: 任务区域 HULK:450-458 
- **轨迹线 (LineCollection)**: 历史轨迹渐变显示 HULK:1011-1016 
- **规划轨迹线**: 未来计划路径 HULK:1033-1037 
- **任务依赖图**: 显示任务前序和同步关系 HULK:1313-1317 

### 2. **Plotly**
用于桑基图 HULK:662-665 

**绘制的图表:**
- **桑基图 (Sankey Diagram)**: 显示智能体-联盟-任务的流动关系

### 3. **PyQtGraph**
用于 Qt 界面的高性能绘图 HULK:4-4 

## 其他关键库

- **NetworkX**: 任务依赖图管理 HULK:11-11 
- **NumPy**: 数值计算和矩阵操作 HULK:10-10 
- **Shapely**: 几何对象操作 HULK:11-11 
- **PyQt5**: GUI 框架 HULK:5-6 

## Notes

所有求解器都使用 SCIP 后端(通过 OR-Tools),这是一个开源的混合整数规划求解器。项目没有使用商业求解器如 Gurobi 或 CPLEX。可视化主要依赖 Matplotlib 生成静态分析图表,PyQt5/PyQtGraph 用于实时仿真界面,Plotly 仅用于桑基图的交互式可视化。

Wiki pages you might want to explore:
- [Overview (1850298154/HULK)](/wiki/1850298154/HULK#1)


### Citations


**File:** src/task/planner.py (L10-10)

```python
import numpy as np # Import numpy for numerical operations and array handling
```

**File:** src/task/planner.py (L11-11)

```python
import networkx as nx # Import networkx for graph-based operations (task graphs)
```

**File:** src/task/planner.py (L13-13)

```python
from scipy.optimize import linprog # Import linprog for linear programming (SciPy)
```

**File:** src/task/planner.py (L14-14)

```python
from ortools.linear_solver import pywraplp # Import pywraplp wrapper for Google OR-Tools linear solver
```

**File:** src/task/planner.py (L1192-1192)

```python
        res = linprog(c=cost, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=(0, 1)) # Solve LP
```

**File:** src/task/planner.py (L1288-1332)

```python
        solver = pywraplp.Solver.CreateSolver("SCIP") # Create SCIP solver
        infinity = solver.infinity() # Infinity
        x = {} # Variable dict
        for i in range(N): # Iterate agents
            for j in range(M): # Iterate units
                x[(i,j)] = solver.BoolVar(f"x_{i}_{j}") # Create boolean var
            solver.Add(solver.Sum(x[(i,j)] for j in range(M)) <= 1) # Constraint: assigned max once

        t_exec = {} # Execution times
        t_arrive = {} # Arrival times
        for j, unit in enumerate(node.plan_units.values()): # Iterate units
            t_exec[j] = 0 # Init exec
            t_arrive[j] = solver.NumVar(0, infinity, f"t_arrive_{j}") # Create arrive var
            lb_total = 0 # Init lower bound sum
            ub_total = 0 # Init upper bound sum
            for uav_type, uav_num in unit.agent_num_dict.items(): # Iterate types
                s, e = agent_type_n_dict[uav_type] # Get range
                lb = uav_num # Lower bound
                ub = lb * 1.3   # TODO: how to make it resonable # Upper bound heuristic
                for task_id in unit.task_list: # Check tasks
                    if self.sharedInfo.tasks[task_id].task_type == "attack": # If attack
                        ub *= 1.4 # Increase bound
                        break # Stop
                solver.Add(solver.Sum(x[(i,j)] for i in range(s, e)) >= lb) # Constrain min agents
                solver.Add(solver.Sum(x[(i,j)] for i in range(s, e)) <= ub) # Constrain max agents
                lb_total += lb # Sum lb
                ub_total += ub # Sum ub
            for task in unit.task_list: # Iterate tasks for time estimation
                cur_task = self.sharedInfo.tasks[task] # Get task
                agent_limit = self.sharedInfo.get_available_agents_num_dict() # Get limits
                min_agent_num = self.matcher.calc_min_agent_demand([[cur_task]], agent_limit=agent_limit) # Get min agents
                max_exec_time = self.estimate_execute_time(min_agent_num[0], cur_task, self.sharedInfo.agents[0].vel) # Calc max time
                alpha = 0.8 # Heuristic factor
                # Linear approximation of execution time reduction with more agents
                t_exec[j] += (solver.Sum(x[(i,j)] for i in range(N)) - lb_total) * (alpha - 1) * max_exec_time / (ub_total - lb_total) + max_exec_time


        T = solver.NumVar(0, infinity, "T") # Makespan variable
        for j in range(M): # Iterate units
            for i in range(N): # Iterate agents
                solver.Add(t_arrive[j] >= time_matrix[i, j] + t_exec[j]) # Constrain arrive time
            solver.Add(T >= t_arrive[j] + t_exec[j]) # Constrain max makespan

        # solve the problem
        solver.Minimize(T) # Minimize makespan
```

**File:** src/task/planner.py (L1632-1702)

```python
        solver = pywraplp.Solver.CreateSolver("SCIP") # Create solver
        infinity = solver.infinity() # Infinity
        x = {} # Vars
        for i in range(N): # Agents
            for j in range(M): # Tasks
                x[(i,j)] = solver.BoolVar(f"x_{i}_{j}") # Bool var
            solver.Add(solver.Sum(x[(i,j)] for j in range(M)) <= 1) # Max 1 task


        task_wrapper = [[task] for task in tasks] # Wrap tasks
        agent_num_dict_all = self.matcher.calc_min_agent_demand(task_wrapper, self.sharedInfo.get_available_agents_num_dict()) # Get demands
        if agent_num_dict_all is None: # If impossible
            return None # Return
        t_arrive = {} # Arrive vars
        t_start_execute = {} # Start vars
        t_exec = {} # Exec times
        t_finish = {} # Finish times
        task_id_mapping = {} # Map
        for j, task in enumerate(tasks): # Iterate tasks
            task_id_mapping[task.task_id] = j # Map
            agent_num_dict = agent_num_dict_all[j] # Get demand
            t_arrive[j] = solver.NumVar(0, infinity, f"t_arrive_{j}") # Var
            t_start_execute[j] = solver.NumVar(0, infinity, f"t_start_execute_{j}") # Var
            lb_total = 0 # Init lb
            ub_total = 0 # Init ub
            for uav_type, uav_num in agent_num_dict.items(): # Iterate demand
                lb = uav_num # Lb
                if uav_type == "uavA": # Set ranges and ub
                    ub = lb * 1.2
                    s = 0
                    e = N_uavA
                elif uav_type == "uavB":
                    ub = lb * 1.3
                    s = N_uavA
                    e = N_uavB
                elif uav_type == "uavC":
                    ub = lb * 1.4
                    s = N_uavB
                    e = N_uavC
                if task.task_type == "attack": # Mod ub for attack
                    ub *= 1.4
                solver.Add(solver.Sum(x[(i,j)] for i in range(s, e)) >= lb) # Constrain lb
                solver.Add(solver.Sum(x[(i,j)] for i in range(s, e)) <= ub) # Constrain ub
                lb_total += lb # Sum
                ub_total += ub # Sum

            max_exec_time = self.estimate_execute_time(agent_num_dict, task, self.sharedInfo.agents[0].vel) # Calc max time
            alpha = 0.8 # Factor
            # Linear approx exec time
            t_exec[j] = (solver.Sum(x[(i,j)] for i in range(N)) - lb_total) * (alpha - 1) * max_exec_time / (ub_total - lb_total) + max_exec_time
            t_finish[j] = t_start_execute[j] + t_exec[j] # Finish time

        for j, task in enumerate(tasks): # Constraints
            all_predecessors = self.sharedInfo.tg.get_predecessors([task.task_id]) # Preds
            for t in all_predecessors: # Iterate preds
                if self.sharedInfo.tasks[t].task_id not in task_id_mapping: # If not in current set
                    continue
                idx = task_id_mapping[self.sharedInfo.tasks[t].task_id] # Get idx
                solver.Add(t_start_execute[j] >= t_finish[idx]) # Prec constraint



        T = solver.NumVar(0, infinity, "T") # Objective var
        for j in range(M): # Tasks
            for i in range(N): # Agents
                solver.Add(t_arrive[j] >= time_matrix[i, j]) # Arrive constraint (This seems incomplete compared to new method?)
            solver.Add(T >= t_finish[j]) # Makespan constraint

        # solve the problem
        solver.Minimize(T) # Min
        status = solver.Solve() # Solve
```

**File:** src/task/planner.py (L1783-1828)

```python
        solver = pywraplp.Solver.CreateSolver("SCIP") # Solver
        infinity = solver.infinity() # Inf
        x = {} # Vars
        for i in range(N): # Agents
            for j in range(M): # Targets
                x[(i,j)] = solver.BoolVar(f"x_{i}_{j}") # Bool
            solver.Add(solver.Sum(x[(i,j)] for j in range(M)) <= 1) # Max 1


        t_target_arrive = {} # Vars
        n_agents = {} # Vars
        for j, target in enumerate(self.target_lists): # Iterate targets
            task_id, _ = self.target_mapping[j] # Get info
            task = self.sharedInfo.tasks[task_id] # Get task
            t_target_arrive[j] = solver.NumVar(0, infinity, f"t_arrive_{j}") # Var
            n_agents[j] = 0 # Init count

            for uav_type in self.matcher.get_available_uav_types(task.task_type, target.target_type): # Check types
                if uav_type == "uavA": # Ranges
                    s = 0
                    e = N_uavA
                elif uav_type == "uavB":
                    s = N_uavA
                    e = N_uavB
                elif uav_type == "uavC":
                    s = N_uavB
                    e = N_uavC

                n_agents[j] += solver.Sum(x[(i,j)] for i in range(s, e)) # Sum agents
            if task.task_type == "capture": # Capture constraints
                # solver.Add(n_agents[j] >= 1)
                # solver.Add(n_agents[j] <= 2)
                solver.Add(n_agents[j] == 1) # Strict 1
            else: # Other
                solver.Add(n_agents[j] == 1) # Strict 1
            t_target_arrive[j] = solver.Sum(x[(i,j)] * time_matrix[i, j] for i in range(N)) # Arrive time


        # minimize the maxium arrival time
        T = solver.NumVar(0, infinity, "T") # Objective
        for j in range(M): # Targets
            solver.Add(T >= t_target_arrive[j]) # Max constraint

        # solve the problem
        solver.Minimize(T) # Min
        status = solver.Solve() # Solve
```

**File:** src/task/planner.py (L1910-2054)

```python
        solver = pywraplp.Solver.CreateSolver("SCIP") # Solver
        infinity = solver.infinity() # Inf

        def get_available_k(j:int): # Get successors based on precedence
            if j == 0: # Start
                return [i for i in range(1, M + 1)] # All tasks
            else: # From task j
                cur_task_id = tasks[j-1].task_id # ID
                all_predecessors = self.sharedInfo.tg.get_all_predecessors([cur_task_id]) # Preds
                simu_tasks = self.sharedInfo.tg.get_simultaneous_tasks(cur_task_id) # Simu
                available_j = [task_idx for task_id, task_idx in self.task_id_mapping.items() if task_id not in all_predecessors and task_id not in simu_tasks] # Filter
                available_j.append(M + 1) # dummy end # Add end
                return available_j

        def get_available_j(k:int): # Get predecessors
            if k == M + 1: # End
                return [i for i in range(1, M + 1)] # All tasks
            else: # To task k
                cur_task_id = tasks[k-1].task_id # ID
                all_successors = self.sharedInfo.tg.get_all_successors([cur_task_id]) # Succs
                simu_tasks = self.sharedInfo.tg.get_simultaneous_tasks(cur_task_id) # Simu
                available_k = [task_idx for task_id, task_idx in self.task_id_mapping.items() if task_id not in all_successors and task_id not in simu_tasks] # Filter
                available_k.append(0) # Add start
                return available_k


        x = {} # Flow vars
        for i in range(N): # Agents
            for j in range(M + 1): # 0 is dummy start # From
                for k in get_available_k(j): # To
                    x[(i, j, k)] = solver.BoolVar(f"x_{i}_{j}_{k}") # Var

        # flow constraints
        for i in range(N): # Agents
            solver.Add(solver.Sum([x[(i, 0, k)] for k in get_available_k(0)]) <= 1) # Start at most once
            solver.Add(solver.Sum([x[(i, j, M + 1)] for j in get_available_j(M + 1)]) <= 1) # End at most once

        # visit constraints
        for i in range(N): # Agents
            for k in range(1, M + 1): # Tasks
                solver.Add(solver.Sum([x[(i, j, k)] for j in get_available_j(k)]) <= 1) # Enter max once

            for j in range(1, M + 1): # Tasks
                solver.Add(solver.Sum([x[(i, j, k)] for k in get_available_k(j)]) <= 1) # Leave max once

        # visit then leave constraints
        for i in range(N): # Agents
            for j in range(1, M + 1): # Tasks
                solver.Add(solver.Sum([x[(i, j, k)] for k in get_available_k(j)]) == solver.Sum([x[(i, k, j)] for k in get_available_j(j)])) # Flow conservation

        # eliminate subtours, using MTZ
        # [1] https://blog.csdn.net/HsinglukLiu/article/details/107848461
        # [2] https://blog.csdn.net/lj614430634/article/details/138818297
        # u_ij - u_ik + M * x_ijk <= M - 1
        u = {} # MTZ vars
        for i in range(N): # Agents
            for j in range(1, M + 1): # Tasks
                u[(i, j)] = solver.IntVar(0, M, f"u_{i}_{j}") # Rank var

        for i in range(N): # Agents
            for j in range(1, M + 1): # From
                available_k = get_available_k(j) # To candidates
                available_k.remove(M+1) # Remove end
                for k in available_k: # To
                    solver.Add(u[(i, j)] - u[(i, k)] + M * x[(i, j, k)] <= M - 1) # MTZ constraint


        t_arrive = {} # Vars
        t_start_execute = {} # Vars
        t_exec = {} # Vars
        t_finish = {} # Vars
        t_finish[0] = 0 # Start time
        for idx, task in enumerate(tasks): # Iterate tasks
            k = idx + 1 # Index 1-based
            t_start_execute[k] = solver.NumVar(0, infinity, f"t_start_execute_{k}") # Var
            agent_num_dict = self.matcher.calc_min_agent_demand([[task]], agent_limit=self.sharedInfo.get_available_agents_num_dict())[0] # Demand
            lb_total = 0 # Init sum
            ub_total = 0 # Init sum
            for uav_type, uav_num in agent_num_dict.items(): # Iterate demand
                lb = uav_num # Lb
                if uav_type == "uavA": # Ranges
                    ub = lb * 1.2
                    s = 0
                    e = N_uavA
                elif uav_type == "uavB":
                    ub = lb * 1.3
                    s = N_uavA
                    e = N_uavB
                elif uav_type == "uavC":
                    ub = lb * 1.4
                    s = N_uavB
                    e = N_uavC
                if task.task_type == "attack": # Mod ub
                    ub *= 1.4
                solver.Add(solver.Sum(x[(i,j,k)] for i in range(s, e) for j in get_available_j(k)) >= lb) # Min agents flow in
                solver.Add(solver.Sum(x[(i,j,k)] for i in range(s, e) for j in get_available_j(k)) <= ub) # Max agents flow in
                lb_total += lb # Sum
                ub_total += ub # Sum

            max_exec_time = self.estimate_execute_time(agent_num_dict, task, self.sharedInfo.agents[0].vel) # Exec time
            alpha = 0.8 # Factor
            t_exec[k] = (solver.Sum(x[(i,j,k)] for i in range(N) for j in get_available_j(k)) - lb_total) * (alpha - 1) * max_exec_time / (ub_total - lb_total) + max_exec_time # Linear approx
            t_finish[k] = t_start_execute[k] + t_exec[k] # Finish

        C_large = 1e8 # Big M
        t_agent_arrive = {} # Agent arrival vars
        for i in range(N): # Agents
            for k in range(1, M + 1): # Tasks
                t_agent_arrive[(i, k)] = solver.NumVar(0, infinity, f"t_agent_arrive_{i}_{k}") # Var
                for j in get_available_j(k): # Predecessors
                    solver.Add(t_agent_arrive[(i, k)] >= t_finish[j] + get_nav_time(i, j, k) - (1 - x[(i, j, k)]) * C_large) # Arrival constraint

        for k in range(1, M + 1): # Tasks
            t_arrive[k] = solver.NumVar(0, infinity, f"t_arrive_{k}") # Task arrive
            for i in range(N): # Agents
                solver.Add(t_arrive[k] >= t_agent_arrive[(i, k)]) # Max over agents
            solver.Add(t_start_execute[k] >= t_arrive[k]) # Start >= Arrive
            all_predecessors = self.sharedInfo.tg.get_all_predecessors([tasks[k-1].task_id]) # Preds
            for task_id in all_predecessors: # Iterate preds
                if task_id in self.task_id_mapping.keys(): # If in current set
                    j = self.task_id_mapping[task_id] # Get idx
                    solver.Add(t_start_execute[k] >= t_finish[j]) # Precedence constraint

        # simultaneous constraints
        for k in range(1, M + 1): # Tasks
            task_id = tasks[k-1].task_id # ID
            all_simu = self.sharedInfo.tg.get_simultaneous_tasks(task_id) # Simu
            if len(all_simu) <= 1: # If single
                continue
            for task_id_ in all_simu: # Iterate group
                if task_id_ == task_id: # Skip self
                    continue
                j = self.task_id_mapping[task_id_] # Get idx
                solver.Add(t_start_execute[k] == t_start_execute[j]) # Sync start
                print(f"Task {task_id} and Task {task_id_} are simultaneous") # Print

        T = solver.NumVar(0, infinity, "T") # Objective
        for j in range(1, M + 1): # Tasks
            solver.Add(T >= t_finish[j]) # Max finish

        max_time = 10000 * M # Time limit scaling
        solver.set_time_limit(max_time) # Set limit

        # solve the problem
        solver.Minimize(T) # Min
```

**File:** src/task/planner.py (L2234-2240)

```python
        solver = pywraplp.Solver.CreateSolver("SCIP") # Solver
        infinity = solver.infinity() # Inf
        x = {} # Vars
        for i in range(N): # Agents
            for j in range(M): # Tasks
                x[(i,j)] = solver.BoolVar(f"x_{i}_{j}") # Bool
            solver.Add(solver.Sum(x[(i,j)] for j in range(M)) <= 1) # Max 1
```

**File:** src/task/planner.py (L2405-2411)

```python
        solver = pywraplp.Solver.CreateSolver("SCIP") # Solver
        infinity = solver.infinity() # Inf
        x = {} # Vars
        for i in range(N): # Agents
            for j in range(M): # Targets
                x[(i,j)] = solver.BoolVar(f"x_{i}_{j}") # Bool
            solver.Add(solver.Sum(x[(i,j)] for j in range(M)) <= 1) # Max 1
```

**File:** src/task/assignment.py (L11-11)

```python
import shapely  # Import shapely for manipulation and analysis of planar geometric objects
```

**File:** src/task/assignment.py (L1413-1462)

```python
        solver = pywraplp.Solver.CreateSolver("SCIP")  # Create solver
        if not solver:  # If solver failed
            return  # Return
        infinity = solver.infinity()  # Get infinity

        # create variables  # Comment variables
        x = {}  # Init variables dict
        for i in range(len(all_tasks)):  # Iterate task groups
            for uav_type in self.uav_types:  # Iterate UAV types
                x[(i, uav_type)] = solver.IntVar(0, infinity, f"x_{i}_{uav_type}")  # Create integer variable

        # create constraints  # Comment constraints
        action_lb_total = {}    # {task_idx: {action: lb}}  # Init lower bound dict
        for idx, tasks in enumerate(all_tasks):  # Iterate task groups
            action_lb = {action:0 for action in self.action_dict.keys()}  # Init action bounds
            for task in tasks:  # Iterate tasks
                cur_action_lb = {action:0 for action in self.action_dict.keys()}  # Init current bounds
                if task.task_type == 'capture':  # If capture
                    for target_type, target_num in task.target_num_dict.items():  # Iterate targets
                        for action in self.skill_dict['task'][task.task_type][target_type]:  # Iterate actions
                            cur_action_lb[action] += target_num * 1.7  # Increase bound
                if task.task_type == 'surveillance':  # If surveillance
                    for target_type, target_num in task.target_num_dict.items():  # Iterate targets
                        for action in self.skill_dict['task'][task.task_type][target_type]:  # Iterate actions
                            cur_action_lb[action] += 0.6 * target_num  # Increase bound
                if task.task_type == 'attack':  # If attack
                    for target in task.target_dict.values():  # Iterate targets
                        if target.valid == False:  # If invalid
                            continue  # Skip
                        for action in self.skill_dict['task'][task.task_type][target.target_type]:  # Iterate actions
                            cur_action_lb[action] += 1.3  # Increase bound

                for action in action_lb.keys():  # Iterate actions
                    action_lb[action] = max(action_lb[action], cur_action_lb[action])  # Take max bound
            action_lb_total[idx] = action_lb.copy()  # Store bounds

        for i in range(len(all_tasks)):  # Iterate groups
            for action, lb in action_lb_total[i].items():  # Iterate actions
                solver.Add(solver.Sum([x[(i, uav_type)] for uav_type in self.action_dict[action]]) >= lb)  # Add constraint

        for uav_type, limit in agent_limit.items():  # Iterate agent limits
            solver.Add(solver.Sum([x[(i, uav_type)] for i in range(len(all_tasks))]) <= limit)  # Add total limit constraint

        # create objective  # Comment objective
        if option == "min_numbers":  # If min numbers
            solver.Minimize(solver.Sum([x[(i, uav_type)] for i in range(len(all_tasks)) for uav_type in self.uav_types]))  # Minimize total count
        elif option == "min_cost":  # If min cost
            solver.Minimize(solver.Sum([self.cost_dict[uav_type]*x[(i, uav_type)] for i in range(len(all_tasks)) for uav_type in self.uav_types]))  # Minimize total cost

        status = solver.Solve()  # Solve
```

**File:** src/task/motion/milp_planner.py (L105-123)

```python
        for i in range(N):
            for j in range(1, M + 1):
                for k in range(1, M + 1):
                    if j != k:
                        solver.Add(u[(i, j)] - u[(i, k)] + M * x[(i, j, k)] <= M - 1)

        # cost constraints
        for i in range(N):
            dist = solver.Sum([x[(i, j, k)] * self.get_cost(i, j, k) for j in range(M + 1) for k in range(1, M + 1 + 1) if not (j == k or (j == 0 and k == M + 1)) ])
            solver.Add(D >= dist)

        # add max solving time
        if max_time is not None:
            solver.set_time_limit(max_time)
        import time
        start_time = time.time()
        # solve
        solver.Minimize(D)
        status = solver.Solve()
```

**File:** scripts/data_process.py (L58-141)

```python
    def calc_average_response_time(self):
        response_time_list = self.calc_response_time()
        return np.mean(response_time_list)


    def calc_replan_time(self):
        replan_max = max(self.sharedInfo.res_replan_time_cost)
        replan_mean = np.mean(self.sharedInfo.res_replan_time_cost)
        replan_per_task = [cost/num for cost, num in zip(self.sharedInfo.res_replan_time_cost, self.sharedInfo.res_replan_task_num)]
        replan_per_task_mean = np.mean(replan_per_task)
        replan_total = np.sum(self.sharedInfo.res_replan_time_cost)
        print(f"Replan mean: {replan_mean}, replan per task mean: {replan_per_task_mean}, replan total: {replan_total}")
        print(f"Replan max: {replan_max}")

    def calc_task_release_time(self):
        task_release_time_list = []
        for task in self.sharedInfo.tasks.values():
            task_release_time_list.append(task.r_release_time)
        mean = np.mean(task_release_time_list)
        sigma = np.std(task_release_time_list)
        mu = len(task_release_time_list)/max(task_release_time_list)
        print(f"Task release time mean: {mean}, std: {sigma}")

    def draw_stack_fig(self):
        fig, ax = plt.subplots(figsize=(6, 2))
        ax:Axes = ax

        travelling = self.sharedInfo.res_travelling_agents_num
        ready = self.sharedInfo.res_ready_agents_num
        working = self.sharedInfo.res_working_agents_num

        colors = ['#1077a0', '#dd7f3e', '#5ca02c']
        time_list = np.arange(len(travelling)) * 0.1
        ax.stackplot(
            time_list,
            [travelling, ready, working],
            labels=['nav.', 'wait', 'exec.'],
            colors=colors,
            alpha=0.8,
            )

        ax2 = ax.twinx()

        ax2.plot(time_list, self.sharedInfo.res_cur_unfinished_tasks_num, 'grey', label='unassigned tasks')
        assigned_tasks_num = [num - self.sharedInfo.res_cur_unassgined_tasks_num[idx] for idx, num in enumerate(self.sharedInfo.res_cur_unfinished_tasks_num)]
        ax2.plot(time_list, assigned_tasks_num, 'b', label='assigned tasks')

        first_line = True
        for ts in self.sharedInfo.res_replan_ts:
            if first_line:
                ax.axvline(ts, color='r', linestyle='--', linewidth=2, label='replan_ts')
                first_line = False
            else:
                ax.axvline(ts, color='r', linestyle='--', linewidth=2, label='_no_lengend_')
        for idx, (ts, count) in enumerate(zip(self.sharedInfo.res_new_task_ts, self.sharedInfo.res_new_task_count)):
            ax.annotate(
                f"$ \\varphi_{{t_{{{idx}}}}}$",
                xy=(ts, 80),
                textcoords="offset points",
                xytext=(15, 10),
                size=10,
                arrowprops=dict(arrowstyle="->", connectionstyle="angle,angleA=0,angleB=90,rad=0"),
            )

        ax.set_ylim(0, 80)
        ax.set_xlim(0, self.calc_make_span() + 5)
        ax2.set_ylim(0, max(self.sharedInfo.res_cur_unfinished_tasks_num)+0.5)

        ax2.legend(loc='upper right')
        ax.set_xlabel("Time[s]")
        ax.set_ylabel("Number of Agents")
        ax2.set_ylabel("Number of Tasks")
        ax.legend(loc='upper left')

        self.save_fig(fig, f"{self.tag}_stack.pdf")

        # calculate the average number of agents in each status
        print(f"Average number of agents in each status: ")
        print(f"Travelling: {np.mean(travelling)}, Ready: {np.mean(ready)}, Working: {np.mean(working)}")
        valid_num = self.sharedInfo.res_valid_agents_num
        print(f"Valid number of agents: {np.mean(valid_num)}")
        print(f"Final valid number of agents: {valid_num[-1]}")
        self.draw_stack_fig_2()

```

**File:** scripts/data_process.py (L201-209)

```python
    def draw_response_time_fig(self):
        fig, ax = plt.subplots()
        response_time_list = self.calc_response_time()
        ax.hist(response_time_list, bins=20, alpha=0.7, color='b', edgecolor='black')
        ax.set_title(f"Response Time Distribution")
        ax.set_xlabel("Response Time")
        ax.set_ylabel("Count")

        self.save_fig(fig, f"{self.tag}_response_time.png")
```

**File:** scripts/data_process.py (L212-342)

```python
    def draw_task_gantt_fig(self):
        fig, gantt_ax = plt.subplots()
        gantt_ax:Axes = gantt_ax

        interval = 2
        height = 0.8
        y_margin = 1

        max_idx = 0

        last_c_id_task_idx = {} # c_id: (task_id, c_idx)
        last_used_idx = []
        for replan_idx, replan_ts in enumerate(self.sharedInfo.res_replan_ts):
            gantt_ax.axvline(replan_ts, color='red', linestyle='--')
            cur_coalition_ids = self.sharedInfo.res_cur_coalition_ids[int(replan_ts*10)]
            for c_id, (task_id, c_idx) in last_c_id_task_idx.items():
                if replan_idx == len(self.sharedInfo.res_replan_ts) - 1:
                    continue
                if self.sharedInfo.coalitions[c_id].task_time_record[task_id]["finish"] > self.sharedInfo.res_replan_ts[replan_idx + 1]:
                    last_used_idx.append(c_idx)
            cur_used_idx = deepcopy(last_used_idx)
            last_used_idx = []

            for c_id in cur_coalition_ids:
                if c_id in last_c_id_task_idx.keys():
                    continue
                c = self.sharedInfo.coalitions[c_id]
                c_idx = 0
                while True:
                    if c_idx not in cur_used_idx:
                        cur_used_idx.append(c_idx)
                        max_idx = max(max_idx, c_idx)
                        break
                    c_idx += 1
                for task_id, task_time in c.task_time_record.items():
                    if "start_travel" not in task_time.keys():
                        continue
                    # text
                    st = task_time["start_travel"]
                    if "finish" in task_time.keys():
                        ft = task_time["finish"]
                    elif "start_execute" in task_time.keys():
                        ft = task_time["start_execute"]
                    elif "wait" in task_time.keys():
                        ft = task_time["wait"]
                    elif "ready" in task_time.keys():
                        ft = task_time["ready"]
                    else:
                        ft = self.sharedInfo.res_replan_ts[replan_idx + 1]
                    gantt_ax.text(x=(st+ft)/2, y=interval*c_idx+y_margin, s=f"$\\omega_{{{task_id}}}$", fontsize=10, horizontalalignment='left', verticalalignment='bottom')
                    gantt_ax.add_patch(plt.Rectangle((st, interval*c_idx+y_margin), ft-st, height, edgecolor='purple', facecolor='none', zorder=100))

                    # travelling time
                    if "ready" in task_time.keys():
                        ready_time = task_time["ready"]
                    else:
                        ready_time = self.sharedInfo.res_replan_ts[replan_idx + 1]
                    gantt_ax.broken_barh(
                        [(task_time["start_travel"], ready_time - task_time["start_travel"])],
                        [interval*c_idx+y_margin, height],
                        facecolor="silver",
                        alpha=0.8,
                        edgecolor="k",
                        )
                    if "ready" not in task_time.keys():
                        continue

                    # ready time
                    if "wait" not in task_time.keys():
                        if "start_execute" not in task_time.keys():
                            ready_end_time = self.sharedInfo.res_replan_ts[replan_idx + 1]
                        else:
                            ready_end_time = task_time["start_execute"]
                    else:
                        ready_end_time = task_time["wait"]
                    gantt_ax.broken_barh(
                        [(ready_time, ready_end_time - ready_time)],
                        [interval*c_idx+y_margin, height],
                        facecolor="lightblue",
                        alpha=0.8,
                        edgecolor="k",
                        )
                    if "wait" not in task_time.keys() and "start_execute" not in task_time.keys():
                        continue

                    # wait time
                    if "wait" in task_time.keys():
                        if "start_execute" not in task_time.keys():
                            wait_end_time = self.sharedInfo.res_replan_ts[replan_idx + 1]
                        else:
                            wait_end_time = task_time["start_execute"]
                        gantt_ax.broken_barh(
                            [(task_time["wait"], wait_end_time - task_time["wait"])],
                            [interval*c_idx+y_margin, height],
                            facecolor="black",
                            alpha=0.8,
                            edgecolor="k",
                            )
                        if "start_execute" not in task_time.keys():
                            continue
                        gantt_ax.broken_barh(
                            [(task_time["start_execute"], task_time["finish"] - task_time["start_execute"])],
                            [interval*c_idx+y_margin, height],
                            facecolor="limegreen",
                            alpha=0.8,
                            edgecolor="k",
                            )
                        if replan_idx < len(self.sharedInfo.res_replan_ts) - 1 and task_time["finish"] > self.sharedInfo.res_replan_ts[replan_idx + 1]:
                            last_used_idx.append(c_idx)
                            last_c_id_task_idx[c_id] = (task_id, c_idx)
                    else:
                        gantt_ax.broken_barh(
                            [(task_time["start_execute"], task_time["finish"] - task_time["start_execute"])],
                            [interval*c_idx+y_margin, height],
                            facecolor="limegreen",
                            alpha=0.8,
                            edgecolor="k",
                            )
                        if replan_idx < len(self.sharedInfo.res_replan_ts) - 1 and task_time["finish"] > self.sharedInfo.res_replan_ts[replan_idx + 1]:
                            last_used_idx.append(c_idx)
                            last_c_id_task_idx[c_id] = (task_id, c_idx)



        gantt_ax.set_ylim((0, interval*max_idx+y_margin+height+y_margin))
        gantt_ax.set_yticks([y_margin+1+interval*i for i in range(max_idx+1)])
        gantt_ax.set_yticklabels([f"$\\mathcal{{N}}_{{{i}}}$" for i in range(max_idx+1)], fontsize=10)
        gantt_ax.tick_params(axis='y', length=0)
        gantt_ax.tick_params(axis='x', length=0)

        self.save_fig(fig, f"{self.tag}_gantt.png")
```

**File:** scripts/data_process.py (L345-429)

```python
    def draw_task_real_time_gantt_fig(self):
        fig, gantt_ax = plt.subplots()
        gantt_ax:Axes = gantt_ax

        interval = 1.2
        height = 0.8
        y_margin = 1
        for task in self.sharedInfo.tasks.values():
            gantt_ax.broken_barh(
                [(task.r_release_time, task.r_start_travel_time - task.r_release_time)],
                [interval*task.task_id+y_margin, height],
                facecolor="grey",
                edgecolor="none",
                alpha=0.8,
                )
            gantt_ax.broken_barh(
                [(task.r_start_travel_time, task.r_ready - task.r_start_travel_time)],
                [interval*task.task_id+y_margin, height],
                facecolor="blue",
                edgecolor="none",
                alpha=0.8,
                )
            if task.r_wait != np.inf:
                gantt_ax.broken_barh(
                    [(task.r_ready, task.r_wait - task.r_ready)],
                    [interval*task.task_id+y_margin, height],
                    facecolor="orange",
                    edgecolor="none",
                    alpha=0.8,
                    )
                gantt_ax.broken_barh(
                    [(task.r_wait, task.r_start_execute_time - task.r_wait)],
                    [interval*task.task_id+y_margin, height],
                    facecolor="yellow",
                    edgecolor="none",
                    alpha=0.8,
                    )
            else:
                gantt_ax.broken_barh(
                    [(task.r_ready, task.r_start_execute_time - task.r_ready)],
                    [interval*task.task_id+y_margin, height],
                    facecolor="orange",
                    edgecolor="none",
                    alpha=0.8,
                    )
            gantt_ax.broken_barh(
                [(task.r_start_execute_time, task.r_finish_time - task.r_start_execute_time)],
                [interval*task.task_id+y_margin, height],
                facecolor="green",
                edgecolor="none",
                alpha=0.8,
            )

            total = len(task.target_dict)
            success = len(task.target_dict)
            for target in task.target_dict.values():
                if target.active:
                    success -= 1
            if success < total:
                gantt_ax.text(x=task.r_finish_time, y=interval*task.task_id+y_margin+height/2, s=f"{success}/{total}", fontsize=10, horizontalalignment='left', verticalalignment='center')
                gantt_ax.add_patch(plt.Rectangle((task.r_release_time, interval*task.task_id+y_margin), task.r_finish_time-task.r_release_time, height, edgecolor='purple', facecolor='none', zorder=100, linewidth=1.5, hatch='//'))

        gantt_ax.set_ylim((0, interval*len(self.sharedInfo.tasks)+y_margin+height+y_margin))
        gantt_ax.set_yticks([y_margin+1+interval*i for i in range(len(self.sharedInfo.tasks))])
        gantt_ax.set_yticklabels([f"$\\omega_{{{i+1}}}$" for i in range(len(self.sharedInfo.tasks))], fontsize=10)
        gantt_ax.tick_params(axis='y', length=0)
        gantt_ax.set_xlabel("Time[s]")

        c_num_ax = gantt_ax.twinx()
        time_list = np.arange(len(self.sharedInfo.res_cur_coalition_num)) * 0.1
        c_num_ax.plot(time_list, self.sharedInfo.res_cur_coalition_num, 'r')
        c_num_ax.set_ylabel("Number of Subteams")

        legend_elements = [
            plt.Line2D([0], [0], color='grey', lw=4, label='Release'),
            plt.Line2D([0], [0], color='blue', lw=4, label='Navigation'),
            plt.Line2D([0], [0], color='orange', lw=4, label='Synchronization'),
            plt.Line2D([0], [0], color='green', lw=4, label='Execution'),
            plt.Line2D([0], [0], color='red', lw=4, label='Number of Subteams'),
            plt.Line2D([0], [0], color='purple', lw=4, label='Unsuccessful Task'),
        ]
        gantt_ax.legend(handles=legend_elements, loc='lower right')


        self.save_fig(fig, f"{self.tag}_task_real_time_gantt.png")
```

**File:** scripts/data_process.py (L662-665)

```python
        fig.write_image(
            os.path.join(self.folder_path, self.fig_folder, f"{self.tag}_sankey.pdf"),
            scale=1,
            )
```

**File:** scripts/data_process.py (L667-680)

```python
    def draw_planning_time_fig(self):
        fig, ax = plt.subplots(figsize=(6, 1.5))
        ax:Axes = ax
        # data = [t*100 for t in self.sharedInfo.res_replan_time_cost]
        data = self.sharedInfo.res_replan_time_cost
        ax.stem(self.sharedInfo.res_replan_ts, data, linefmt='b-', markerfmt='bo', basefmt=' ')
        replan_mean = np.mean(data)
        ax.axhline(replan_mean, color='g', linestyle='--', label='Mean')
        ax.text(0, replan_mean, f"{replan_mean:.1f}", color='g', fontsize=10, verticalalignment='bottom', horizontalalignment='left')
        ax.axhline(1.4, color='r', linestyle='--', label='Ours Mean')
        ax.text(0, 1.4, f"1.4", color='r', fontsize=10, verticalalignment='bottom', horizontalalignment='left')
        ax.set_ylabel("Planning Time[s]")
        ax.legend(loc='upper right')
        self.save_fig(fig, f"{self.tag}_planning_time.png")
```

**File:** scripts/data_process.py (L694-738)

```python
    def draw_stack_fig_alpha(self):
        fig, ax = plt.subplots(figsize=(6, 1.8))
        ax:Axes = ax

        travelling = self.sharedInfo.res_travelling_agents_num
        ready = self.sharedInfo.res_ready_agents_num
        working = self.sharedInfo.res_working_agents_num

        colors = ['#1077a0', '#dd7f3e', '#5ca02c']
        time_list = np.arange(len(travelling)) * 0.1
        ax.stackplot(
            time_list,
            [travelling, ready, working],
            labels=['nav.', 'wait', 'exec.'],
            colors=colors,
            alpha=0.8,
            )

        ax.plot(time_list, self.sharedInfo.res_valid_agents_num, 'r', label='valid')

        ax2 = ax.twinx()
        # finish_rate = [(total-num)/total*100 for num, total in zip(self.sharedInfo.res_cur_unfinished_tasks_num, self.sharedInfo.res_cur_total_tasks_num)]
        finish_rate = []
        for num, total in zip(self.sharedInfo.res_cur_unfinished_tasks_num, self.sharedInfo.res_cur_total_tasks_num):
            finish = total - num
            if finish >= 60:
                finish -= 1
            if finish >= 61:
                finish -= 1
            # 60 -> 59
            # 61 -> 60 -> 59
            # 62 -> 61 -> 60
            # 63 -> 62 -> 61
            finish_rate.append(finish/total*100)

        ax2.plot(time_list, finish_rate, 'darkorchid', label='task finish rate')

        ax.set_xlabel("Time[s]")
        ax.set_ylabel("Number of Agents")
        ax2.set_ylabel("Task Finish Rate[%]")
        ax.legend(loc='upper left')
        ax2.legend(loc='upper right')
        ax2.set_ylim(0, 100)

        self.save_fig(fig, f"{self.tag}_stack_alpha.png")
```

**File:** src/render/resource/view/simulation_interface.py (L4-4)

```python
import pyqtgraph as pg
```

**File:** src/render/resource/view/simulation_interface.py (L5-6)

```python
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsPolygonItem
```

**File:** src/render/resource/view/simulation_interface.py (L10-16)

```python
from matplotlib import colormaps as cm, pyplot as plt
from matplotlib.patches import Circle
from matplotlib.widgets import Cursor
from matplotlib.collections import LineCollection
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.gridspec as gridspec
```

**File:** src/render/resource/view/simulation_interface.py (L417-419)

```python
        self.sprite_ax.scatter(agentA_pos[:,0], agentA_pos[:,1], edgecolors=agentA_edge_color, facecolor=agentA_color, s=100, marker="P", linewidths=1.5, zorder=21)   # 十字
        self.sprite_ax.scatter(agentB_pos[:,0], agentB_pos[:,1], edgecolors=agentB_edge_color, facecolor=agentB_color, s=100, marker="X", linewidths=1.5, zorder=21)   # X
        self.sprite_ax.scatter(agentC_pos[:,0], agentC_pos[:,1], edgecolors=agentC_edge_color, facecolor=agentC_color, s=100, marker="D", linewidths=1.5, zorder=21)   # 菱形
```

**File:** src/render/resource/view/simulation_interface.py (L450-458)

```python
            if task.area.area_type == "polygon":
                pts = np.array(task.area.polygon.exterior.coords[:-1])
                self.sprite_ax.fill(pts[:,0], pts[:,1], facecolor=face_color, edgecolor=edge_color, alpha=area_alpha, linewidth=2, zorder=10)
            elif task.area.area_type == "circle":
                center = task.area.center
                radius = task.area.radius
                circle = Circle(center, radius, facecolor=face_color, edgecolor=edge_color, alpha=area_alpha, linewidth=2)
                circle.set_zorder(10)
                self.sprite_ax.add_artist(circle)
```

**File:** src/render/resource/view/simulation_interface.py (L1011-1016)

```python
                    traj = agent.history_traj[-self.k_history_traj_length:]
                    colors = cm.get_cmap('Greys')(np.linspace(0.2, 0.9, len(traj)))
                    points = np.array([traj[:-1], traj[1:]]).transpose(1, 0, 2)
                    segments = LineCollection(points, colors=colors, linewidths=2.8, alpha=0.4)
                    segments.set_zorder(0)
                    self.sk_ax.add_collection(segments)
```

**File:** src/render/resource/view/simulation_interface.py (L1033-1037)

```python
                    alpha = 0.9
                    linewidth = 3.5

                    colors = self.rb[agent.cur_c_id%self.k_rb]
                    self.sk_ax.plot(traj[:,0], traj[:,1], color=colors, linewidth=linewidth, alpha=alpha, zorder=20)
```

**File:** src/render/resource/view/simulation_interface.py (L1313-1317)

```python
        self.graph_ax.axis('off')
        self.graph_ax.set_aspect('equal')
        self.graph_ax.autoscale_view()

        self.draw()
```

