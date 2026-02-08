arxiv_queries = [  
    ######################################### MPC 模型预测控制规划路径，死锁解决，分布式决策
    # 核心主题  
    'ti:"multi-agent path planning" AND ti:"deadlock resolution"',  
    'abs:"distributed multi-agent" AND abs:"deadlock breaking"',  
    'all:"homogeneous egalitarian" AND all:"deadlock"',  
    'ti:"large-scale" AND ti:"multi-agent" AND ti:"path planning"',  
    'abs:"100+ agents" AND abs:"distributed planning"',  
  
    # 死锁与冲突避免  
    'ti:"deadlock" AND ti:"multi-agent"',  
    'abs:"deadlock resolution" AND abs:"robotics"',  
    'all:"conflict-free" AND all:"trajectory" AND all:"multi-robot"',  
    'ti:"deadlock-breaking" AND ti:"algorithm"',  
    'abs:"deadlock" AND abs:"egalitarian"',  
  
    # 时序轨迹与多项式轨迹  
    'ti:"temporal trajectory" AND ti:"coordination"',  
    'abs:"piecewise polynomial" AND abs:"trajectory"',  
    'all:"5th-order" AND all:"polynomial" AND all:"trajectory"',  
    'ti:"7th-order" AND ti:"trajectory" AND ti:"planning"',  
    'abs:"trajectory generation" AND abs:"temporal coordination"',  
  
    # 分布式优化与凸规划  
    'ti:"convex program" AND ti:"multi-agent"',  
    'abs:"distributed optimization" AND abs:"path planning"',  
    'all:"convex" AND all:"constraints" AND all:"multi-robot"',  
    'ti:"distributed" AND ti:"convex" AND ti:"planning"',  
    'abs:"constraint" AND abs:"multi-agent" AND abs:"optimization"',  
  
    # ROS 与嵌入式实现  
    'ti:"ROS" AND ti:"multi-agent" AND ti:"planning"',  
    'abs:"Crazyflie" AND abs:"swarm"',  
    'all:"firmware" AND all:"trajectory execution"',  
    'ti:"embedded" AND ti:"trajectory" AND ti:"execution"',  
    'abs:"crazyflie_ros" AND abs:"planner"',  
  
    # 碰撞避免与安全  
    'ti:"collision avoidance" AND ti:"multi-agent"',  
    'abs:"local obstacle" AND abs:"avoidance"',  
    'all:"safety" AND all:"multi-robot" AND all:"planning"',  
    'ti:"decentralized" AND ti:"collision avoidance"',  
    'abs:"sensor-based" AND abs:"obstacle" AND abs:"avoidance"',  
  
    # 应用场景与规模  
    'ti:"drone swarm" AND ti:"path planning"',  
    'abs:"warehouse automation" AND abs:"multi-agent"',  
    'all:"UAV" AND all:"formation" AND all:"planning"',  
    'ti:"large-scale" AND ti:"drone" AND ti:"coordination"',  
    'abs:"autonomous" AND abs:"delivery" AND abs:"fleet"',  

    ######################################### heriarchical multi-UAV task allocation
    
    # 系统与架构  
    'ti:"hierarchical multi-UAV" AND ti:"task allocation"',  
    'all:"multi-agent planning" AND ti:"UAV swarm"',  
    'ti:"clustered UAV" AND ti:"mission coordination"',  
    'abs:"hierarchical multitasking" AND ti:"multi-agent systems"',  
    # 规划与分配算法  
    'ti:"Hungarian algorithm" AND ti:"task assignment" AND ti:"UAV"',  
    'all:"boustrophedon decomposition" AND ti:"area coverage"',  
    'ti:"iterative load balancing" AND ti:"path planning"',  
    'abs:"online replanning" AND ti:"dynamic task allocation"',  
    # 避障与路径规划  
    'ti:"Bug algorithm" AND ti:"obstacle avoidance" AND ti:"UAV"',  
    'all:"path planning" AND ti:"inflated obstacles"',  
    # 通信与仿真  
    'ti:"UDP/HTTP dual protocol" AND ti:"UAV communication"',  
    'abs:"simulation environment" AND ti:"WorldServer"',  
    # 领域综合  
    'ti:"cooperative search" AND ti:"multi-UAV"',  
    'all:"persistent surveillance" AND ti:"UAV team"',  
    'ti:"decentralized task allocation" AND ti:"drone swarm"',  
    'abs:"real-time replanning" AND ti:"multi-robot systems"'  

    ######################################### HULK
    
    # 核心问题域  
    'multi-agent task allocation UAV',  
    'coalition formation heterogeneous agents',  
    'dynamic task assignment multi-robot',  
    'hierarchical task planning UAV swarm',  
      
    # 算法相关  
    'MILP task allocation makespan minimization',  
    'tree search coalition formation',  
    'receding horizon planning multi-agent',  
    'MVRP multi-vehicle routing problem',  
    'K-means clustering task allocation',  
      
    # 约束和协调  
    'task dependency constraints precedence',  
    'skill-based agent task matching',  
    'temporal constraints task scheduling',  
    'Nash equilibrium multi-agent planning',  
      
    # 应用场景  
    'search and rescue UAV coordination',  
    'surveillance task allocation drones',  
    'target capture multi-robot',  
    'area coverage path planning',  
      
    # 方法论  
    'anytime algorithm task planning',  
    'event-triggered replanning',  
    'MTZ subtour elimination VRP',  
    'OR-Tools constraint programming',  
      
    # 组合查询  
    'ti:"multi-agent" AND ti:"task allocation"',  
    'ti:"coalition formation" AND ti:"UAV"',  
    'ti:"MILP" AND ti:"makespan"',  
    'abs:"heterogeneous agents" AND abs:"task allocation"',  
    'abs:"receding horizon" AND abs:"multi-robot"',  
    

    ######################################### llm、marl、运筹优化等算法方法
    
    # --- LLM & GenAI for Planning (大模型与生成式AI) ---
    'all:"Large Language Model" AND all:"multi-agent path planning"',
    'ti:"LLM" AND ti:"task allocation" AND ti:"robot"',
    'abs:"foundation model" AND abs:"UAV swarm" AND abs:"planning"',
    'all:"GPT" AND all:"robot navigation" AND all:"multi-agent"',
    'ti:"language-guided" AND ti:"multi-robot" AND ti:"coordination"',
    'abs:"prompt engineering" AND abs:"task assignment" AND abs:"robots"',
    'all:"LLM-based" AND all:"decentralized" AND all:"control"',
    'ti:"generative AI" AND ti:"trajectory generation" AND ti:"UAV"',
    'abs:"natural language" AND abs:"human-swarm interaction"',
    'all:"reasoning" AND all:"LLM" AND all:"multi-agent system"',

    # --- Reinforcement Learning (强化学习 & MARL) ---
    'ti:"multi-agent reinforcement learning" AND ti:"UAV"',
    'abs:"MARL" AND abs:"heterogeneous" AND abs:"task allocation"',
    'all:"Deep Q-Network" AND all:"path planning" AND all:"drones"',
    'ti:"proximal policy optimization" AND ti:"multi-robot"',
    'abs:"actor-critic" AND abs:"collision avoidance" AND abs:"swarm"',
    'all:"decentralized learning" AND all:"cooperative navigation"',
    'ti:"curriculum learning" AND ti:"multi-agent" AND ti:"planning"',
    'abs:"graph neural network" AND abs:"path finding" AND abs:"robots"',
    'all:"policy gradient" AND all:"UAV formation"',
    'ti:"hierarchical reinforcement learning" AND ti:"mission planning"',

    # --- Operations Research & Optimization (运筹优化) ---
    'ti:"column generation" AND ti:"vehicle routing" AND ti:"UAV"',
    'abs:"branch and price" AND abs:"multi-task" AND abs:"allocation"',
    'all:"mixed integer linear programming" AND all:"heterogeneous UAV"',
    'ti:"genetic algorithm" AND ti:"path planning" AND ti:"multi-uav"',
    'abs:"ant colony optimization" AND abs:"task scheduling"',
    'all:"particle swarm optimization" AND all:"trajectory planning"',
    'ti:"simulated annealing" AND ti:"task assignment" AND ti:"robot"',
    'abs:"combinatorial auction" AND abs:"multi-robot" AND abs:"coordination"',
    'all:"game theory" AND all:"mechanism design" AND all:"UAV"',
    'ti:"market-based" AND ti:"approach" AND ti:"task allocation"',

    # --- Heterogeneous Systems (异构系统特化) ---
    'ti:"heterogeneous" AND ti:"UAV-UGV" AND ti:"coordination"',
    'abs:"air-ground" AND abs:"cooperative" AND abs:"planning"',
    'all:"capabilities" AND all:"coalition" AND all:"multi-robot"',
    'ti:"cross-domain" AND ti:"multi-agent" AND ti:"collaboration"',
    'abs:"different kinematics" AND abs:"formation control"',
    'all:"heterogeneous swarm" AND all:"resilience"',
    'ti:"leader-follower" AND ti:"heterogeneous" AND ti:"tracking"',
    'abs:"resource constraint" AND abs:"heterogeneous agents"',
    
    # --- Advanced Algorithmic Intersections (算法交叉) ---
    'ti:"neuro-symbolic" AND ti:"planning" AND ti:"robotics"',
    'abs:"model predictive control" AND abs:"learning-based"',
    'all:"data-driven" AND all:"optimization" AND all:"trajectory"',
    'ti:"distributed" AND ti:"model predictive control" AND ti:"swarm"',
    'abs:"safe reinforcement learning" AND abs:"multi-agent"',
    'all:"transformer" AND all:"trajectory prediction" AND all:"agents"',
    'ti:"attention mechanism" AND ti:"multi-agent" AND ti:"communication"',
    'abs:"knowledge graph" AND abs:"robot" AND abs:"task planning"',
    'all:"evolutionary strategy" AND all:"neuroevolution" AND all:"swarm"',
    'ti:"hybrid" AND ti:"algorithm" AND ti:"path planning"',
    'abs:"meta-heuristic" AND abs:"large-scale" AND abs:"optimization"'
]