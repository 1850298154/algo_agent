# import asyncio
# from aiolimiter import AsyncLimiter

# # 1. 初始化限流器：每秒最多执行1次操作
# limiter = AsyncLimiter(max_rate=1, time_period=1)

# async def limited_task(task_id):
#     """被限流的异步任务"""
#     # 2. 关键：用async with获取令牌，没有可用令牌时会等待
#     async with limiter:
#         print(f"执行任务 {task_id} - {asyncio.get_event_loop().time():.2f}")
#         # 模拟任务执行（比如API请求）
#         # await asyncio.sleep(0.1)

# async def main():
#     # 批量创建10个任务，测试限流效果
#     tasks = [limited_task(i) for i in range(10)]
#     await asyncio.gather(*tasks)

# if __name__ == "__main__":
#     asyncio.run(main())


import asyncio
from random import random
# Task coroutine
async def task(semaphore, number):
   async with semaphore:
    #    value = random()
       value = 3
       print(f'Task {number} got {value}')
       await asyncio.sleep(value)
# Main coroutine
async def main():
   semaphore = asyncio.Semaphore(2)
   tasks = [asyncio.create_task(task(semaphore, i)) for i in range(10)]
   await asyncio.gather(*tasks)
# Start the asyncio program
asyncio.run(main())

