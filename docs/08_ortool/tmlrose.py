import mlrose
# 测试基础功能（生成TSP问题并求解）
from mlrose import TSPOpt, random_discrete_opt

# 生成随机TSP问题
coords = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10)]
tsp_problem = TSPOpt(length=5, coords=coords, maximize=False)
# 用遗传算法求解
best_state, best_fitness = tsp_problem.solve(algorithm='genetic_alg', pop_size=200, mutation_prob=0.1)
print("mlrose安装成功！TSP最优路径：", best_state)
print("最优路径长度：", best_fitness)