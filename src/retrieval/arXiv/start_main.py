import asyncio
import os
import sys
# print(sys.path)
# sys.path.append(
#     os.path.abspath(
#     os.path.join(
#     os.path.dirname(__file__), '../../..')))
import json
import pprint
from unittest.mock import Base
from pydantic import BaseModel, Field
from src.retrieval.arXiv.config import (
    MAX_REQUESTS_PER_SECOND, 
    DOWNLOAD_DIR, 
    DOWNLOAD_CONCURRENCY, 
    PAPERS_RESULT_PATH,
    )
from src.retrieval.arXiv.core.rate_limiter import TokenBucketLimiter
from src.retrieval.arXiv.core.network import RateLimitedClient
from src.retrieval.arXiv.services.search_service import SearchService
from src.retrieval.arXiv.services.download_service import DownloadService
from src.retrieval.arXiv.utils.logger import logger
from src.retrieval.arXiv import arxiv_pydantic
# input("Press Enter to continue...")


class AllPapers(BaseModel):
    papers: list[arxiv_pydantic.Result] = Field(..., description="List of all unique papers found.")

async def main(queries: list[str], max_results_per_query: int = 10):
    # 1. 初始化基础设施
    logger.info("🛠️  Initializing system...")
    
    # 核心：全局限流器 (1s 2个令牌)
    global_limiter = TokenBucketLimiter(rate_per_second=MAX_REQUESTS_PER_SECOND)
    
    # 网络客户端 (注入限流器)
    network_client = RateLimitedClient(global_limiter)
    await network_client.start()
    
    # 业务服务
    search_service = SearchService(global_limiter) # 搜索也共享同一个限流器
    download_service = DownloadService(network_client, DOWNLOAD_DIR)

    try:
        # 2. 执行搜索阶段
        search_tasks = [search_service.search(q, max_results=max_results_per_query) 
                        for q in queries]
        logger.info("🔍 Starting search phase...")
        results_list: list[list[arxiv_pydantic.Result]] = await asyncio.gather(*search_tasks)
        
        # 去重
        all_papers = AllPapers(papers=[])
        seen_ids = set()
        for res in results_list:
            for paper in res:
                if paper.get_short_id() not in seen_ids:
                    all_papers.papers.append(paper)
                    seen_ids.add(paper.get_short_id())
        logger.info(f"📊 Total unique papers to process: {len(all_papers.papers)}")
        with open(PAPERS_RESULT_PATH, "w", encoding="utf-8") as f:
            all_papers_json_str = all_papers.model_dump_json(indent=4)
            # f.write(pprint.pformat(all_papers_json_str))
            f.write(all_papers_json_str)

        # 3. 执行下载阶段
        # 使用Semaphore控制最大并发任务数（虽然有令牌桶兜底，但Semaphore可以防止创建过多Task对象占用内存）
        sem = asyncio.Semaphore(DOWNLOAD_CONCURRENCY)
        async def bounded_process(paper: arxiv_pydantic.Result):
            async with sem:
                await download_service.process_paper(paper)

        download_tasks = [bounded_process(p) for p in all_papers.papers]
        if download_tasks:
            logger.info("🔥 Starting download phase...")
            await asyncio.gather(*download_tasks)
        else:
            logger.warning("⚠️  No papers found.")

    finally:
        await network_client.close()
        logger.info("✨ Mission Complete.")




arxiv_queries = [  
    ######################################### MPC 模型预测控制规划路径，死锁解决，分布式决策
    # 核心主题 (ti→abs，放宽数量限定)
    'abs:"multi-agent path planning" OR abs:"deadlock resolution"',  
    'abs:"distributed multi-agent" OR abs:"deadlock breaking"',  
    'all:"homogeneous egalitarian" OR all:"deadlock"',  
    'abs:"large-scale" AND abs:"multi-agent path planning"',  
    'abs:"multi-agent" AND abs:"distributed planning" AND (abs:"100 agents" OR abs:"large-scale")',  

    # 死锁与冲突避免 (ti→abs，补充同义词)
    'abs:"deadlock" AND abs:"multi-agent" OR abs:"multi-robot"',  
    'abs:"deadlock resolution" OR abs:"deadlock breaking" AND abs:"robotics"',  
    'all:"conflict-free" OR all:"collision-free" AND all:"trajectory" AND all:"multi-robot"',  
    'abs:"deadlock-breaking" OR abs:"deadlock avoidance" AND abs:"algorithm"',  
    'abs:"deadlock" AND (abs:"egalitarian" OR abs:"fairness")',  

    # 时序轨迹与多项式轨迹 (ti→abs，放宽阶数限定)
    'abs:"temporal trajectory" AND abs:"coordination"',  
    'abs:"piecewise polynomial" OR abs:"polynomial trajectory"',  
    'all:"polynomial trajectory" AND (all:"5th-order" OR all:"7th-order" OR all:"6th-order")',  
    'abs:"7th-order" OR abs:"5th-order" AND abs:"trajectory planning"',  
    'abs:"trajectory generation" AND abs:"temporal coordination"',  

    # 分布式优化与凸规划 (ti→abs，核心保留AND)
    'abs:"convex program" AND abs:"multi-agent"',  
    'abs:"distributed optimization" AND abs:"path planning"',  
    'all:"convex constraints" AND all:"multi-robot"',  
    'abs:"distributed" AND abs:"convex planning"',  
    'abs:"constraint" AND abs:"multi-agent optimization"',  

    # ROS 与嵌入式实现 (ti→abs，补充变体)
    'abs:"ROS" AND abs:"multi-agent planning"',  
    'abs:"Crazyflie" OR abs:"drone swarm"',  
    'all:"firmware" AND all:"trajectory execution"',  
    'abs:"embedded" AND abs:"trajectory execution"',  
    'abs:"crazyflie_ros" OR abs:"drone planner"',  

    # 碰撞避免与安全 (ti→abs，补充decentralized/distributed)
    'abs:"collision avoidance" AND abs:"multi-agent"',  
    'abs:"local obstacle" AND abs:"avoidance"',  
    'all:"safety" AND all:"multi-robot planning"',  
    'abs:"decentralized" OR abs:"distributed" AND abs:"collision avoidance"',  
    'abs:"sensor-based" AND abs:"obstacle avoidance"',  

    # 应用场景与规模 (ti→abs，补充同义词)
    'abs:"drone swarm" OR abs:"UAV swarm" AND abs:"path planning"',  
    'abs:"warehouse automation" AND abs:"multi-agent"',  
    'all:"UAV" OR all:"drone" AND all:"formation planning"',  
    'abs:"large-scale" AND abs:"drone coordination"',  
    'abs:"autonomous delivery" AND abs:"fleet"',  

    ######################################### heriarchical multi-UAV task allocation
    # 系统与架构 (ti→abs，补充变体)
    'abs:"hierarchical multi-UAV" OR abs:"hierarchical multi-drone" AND abs:"task allocation"',  
    'all:"multi-agent planning" OR all:"multi-robot planning" AND abs:"UAV swarm"',  
    'abs:"clustered UAV" AND abs:"mission coordination"',  
    'abs:"hierarchical multitasking" AND abs:"multi-agent systems"',  

    # 规划与分配算法 (ti→abs，放宽组合)
    'abs:"Hungarian algorithm" AND abs:"task assignment" AND (abs:"UAV" OR abs:"drone")',  
    'all:"boustrophedon decomposition" AND all:"area coverage"',  
    'abs:"iterative load balancing" AND abs:"path planning"',  
    'abs:"online replanning" OR abs:"dynamic task allocation"',  

    # 避障与路径规划 (ti→abs，补充变体)
    'abs:"Bug algorithm" AND abs:"obstacle avoidance" AND (abs:"UAV" OR abs:"drone")',  
    'all:"path planning" AND all:"inflated obstacles" OR all:"obstacle inflation"',  

    # 通信与仿真 (ti→abs，放宽协议限定)
    'abs:"UAV communication" AND (abs:"UDP" OR abs:"HTTP" OR abs:"TCP")',  
    'abs:"simulation environment" AND abs:"multi-UAV" OR abs:"WorldServer"',  

    # 领域综合 (ti→abs，补充同义词)
    'abs:"cooperative search" AND abs:"multi-UAV" OR abs:"multi-drone"',  
    'all:"persistent surveillance" AND all:"UAV team" OR all:"drone team"',  
    'abs:"decentralized task allocation" AND abs:"drone swarm"',  
    'abs:"real-time replanning" AND abs:"multi-robot systems"',  

    ######################################### HULK
    # 核心问题域 (补充变体，放宽组合)
    'multi-agent task allocation UAV OR drone',  
    'coalition formation heterogeneous agents OR robots',  
    'dynamic task assignment multi-robot OR multi-agent',  
    'hierarchical task planning UAV swarm OR drone swarm',  

    # 算法相关 (保留核心，放宽场景)
    'MILP task allocation makespan minimization',  
    'tree search coalition formation',  
    'receding horizon planning multi-agent',  
    'MVRP multi-vehicle routing problem UAV OR robot',  
    'K-means clustering task allocation',  

    # 约束和协调 (补充同义词)
    'task dependency constraints precedence OR order',  
    'skill-based agent task matching',  
    'temporal constraints task scheduling',  
    'Nash equilibrium multi-agent planning',  

    # 应用场景 (补充变体)
    'search and rescue UAV coordination OR drone coordination',  
    'surveillance task allocation drones OR UAVs',  
    'target capture multi-robot OR multi-agent',  
    'area coverage path planning UAV OR drone',  

    # 方法论 (保留核心，放宽组合)
    'anytime algorithm task planning',  
    'event-triggered replanning',  
    'MTZ subtour elimination VRP',  
    'OR-Tools constraint programming',  

    # 组合查询 (ti→abs，扩大范围)
    'abs:"multi-agent" AND abs:"task allocation"',  
    'abs:"coalition formation" AND (abs:"UAV" OR abs:"drone")',  
    'abs:"MILP" AND abs:"makespan"',  
    'abs:"heterogeneous agents" AND abs:"task allocation"',  
    'abs:"receding horizon" AND abs:"multi-robot"',  

    ######################################### llm、marl、运筹优化等算法方法
    # --- LLM & GenAI for Planning (大模型与生成式AI) ---
    'all:"Large Language Model" OR all:"LLM" AND all:"multi-agent path planning"',
    'abs:"LLM" AND abs:"task allocation" AND abs:"robot" OR abs:"UAV"',
    'abs:"foundation model" AND abs:"UAV swarm" OR abs:"drone swarm" AND abs:"planning"',
    'all:"GPT" OR all:"LLM" AND all:"robot navigation" AND all:"multi-agent"',
    'abs:"language-guided" AND abs:"multi-robot" AND abs:"coordination"',
    'abs:"prompt engineering" AND abs:"task assignment" AND abs:"robots"',
    'all:"LLM-based" AND all:"decentralized control" OR all:"distributed control"',
    'abs:"generative AI" AND abs:"trajectory generation" AND abs:"UAV"',
    'abs:"natural language" AND abs:"human-swarm interaction"',
    'all:"reasoning" AND all:"LLM" AND all:"multi-agent system"',

    # --- Reinforcement Learning (强化学习 & MARL) ---
    'abs:"multi-agent reinforcement learning" OR abs:"MARL" AND abs:"UAV"',
    'abs:"MARL" AND abs:"heterogeneous" AND abs:"task allocation"',
    'all:"Deep Q-Network" OR all:"DQN" AND all:"path planning" AND all:"drones"',
    'abs:"proximal policy optimization" OR abs:"PPO" AND abs:"multi-robot"',
    'abs:"actor-critic" AND abs:"collision avoidance" AND abs:"swarm"',
    'all:"decentralized learning" AND all:"cooperative navigation"',
    'abs:"curriculum learning" AND abs:"multi-agent planning"',
    'abs:"graph neural network" OR abs:"GNN" AND abs:"path finding"',
    'all:"policy gradient" AND all:"UAV formation"',
    'abs:"hierarchical reinforcement learning" AND abs:"mission planning"',

    # --- Operations Research & Optimization (运筹优化) ---
    'abs:"column generation" AND abs:"vehicle routing" AND abs:"UAV"',
    'abs:"branch and price" AND abs:"multi-task allocation"',
    'all:"mixed integer linear programming" OR all:"MILP" AND all:"heterogeneous UAV"',
    'abs:"genetic algorithm" AND abs:"path planning" AND abs:"multi-uav"',
    'abs:"ant colony optimization" AND abs:"task scheduling"',
    'all:"particle swarm optimization" OR all:"PSO" AND all:"trajectory planning"',
    'abs:"simulated annealing" AND abs:"task assignment" AND abs:"robot"',
    'abs:"combinatorial auction" AND abs:"multi-robot coordination"',
    'all:"game theory" AND all:"mechanism design" AND all:"UAV"',
    'abs:"market-based approach" AND abs:"task allocation"',

    # --- Heterogeneous Systems (异构系统特化) ---
    'abs:"heterogeneous" AND abs:"UAV-UGV" AND abs:"coordination"',
    'abs:"air-ground cooperative" AND abs:"planning"',
    'all:"capabilities" AND all:"coalition" AND all:"multi-robot"',
    'abs:"cross-domain" AND abs:"multi-agent collaboration"',
    'abs:"different kinematics" AND abs:"formation control"',
    'all:"heterogeneous swarm" AND all:"resilience"',
    'abs:"leader-follower" AND abs:"heterogeneous tracking"',
    'abs:"resource constraint" AND abs:"heterogeneous agents"',
    
    # --- Advanced Algorithmic Intersections (算法交叉) ---
    'abs:"neuro-symbolic" AND abs:"planning robotics"',
    'abs:"model predictive control" OR abs:"MPC" AND abs:"learning-based"',
    'all:"data-driven optimization" AND all:"trajectory"',
    'abs:"distributed model predictive control" AND abs:"swarm"',
    'abs:"safe reinforcement learning" AND abs:"multi-agent"',
    'all:"transformer" AND all:"trajectory prediction agents"',
    'abs:"attention mechanism" AND abs:"multi-agent communication"',
    'abs:"knowledge graph" AND abs:"robot task planning"',
    'all:"evolutionary strategy" OR all:"neuroevolution" AND all:"swarm"',
    'abs:"hybrid algorithm" AND abs:"path planning"',
    'abs:"meta-heuristic" AND abs:"large-scale optimization"'
]
# arxiv_queries = [
#     "tl:multi-agent path planning",
# ]


if __name__ == "__main__":
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    try:
        asyncio.run(main(arxiv_queries, max_results_per_query=10))
    except KeyboardInterrupt:
        logger.info("🛑 Stopped by user.")