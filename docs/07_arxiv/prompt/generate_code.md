其中不要只搜索一个
        # 1. 搜索论文
        search = arxiv.Search(
            query=f'ti:"{title}"',
            max_results=num_results,
            sort_by=arxiv.SortCriterion.Relevance
        )
        result = next(client.results(search))
其中告诉我Search除了sort_by=arxiv.SortCriterion.Relevance，还有哪些可以选择的参数？详细讲解？
这个能不能改一下，一个query和search需要返回多个结果？一般每一次搜索一个问题，类似如下这些，需要把max_results多少，给我一个范围，然后填入这个参数max_results?
arxiv_queries = [  
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
]  
arxiv_queries = [  
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
]

search_queries = [  
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
]
同时除了上述三个个，再给我补充 用 multi ai agent、llm、RL、各种运筹优化等等来解决相关多种异构uav多任务任务分配和路径规划问题的查询语句，要求覆盖不同的算法方法和应用场景，给我一个范围，至少40条，最多100条。

然后再继续完成上述的下载，pdf、 bib、latex，命名必须用论文标题，最后用streamlit展示这些查询语句，用户可以选择一个查询语句，点击搜索后展示arXiv上相关的论文标题、摘要和链接。


下载完之后，再给我写另外一个代码，要求根据上述下载的内容，用streamlit展示这些查询语句，用户可以选择一个查询语句，点击搜索后展示arXiv上相关的论文标题、摘要和链接。还能讲这些论文分类选择展示（包括学科分类、时间等等等），类似于各种条件过滤，然后配出来个各种统计图表，展示这些论文的分布情况（比如按时间、按学科分类、按作者等等）。