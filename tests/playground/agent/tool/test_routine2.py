import asyncio

# 1. 定义一个最简单的异步函数（模拟耗时操作，比如网络请求/IO）
async def simple_async_task(name: str, delay: float) -> str:
    """异步任务：等待指定时间后返回结果"""
    print(f"任务[{name}]开始执行（需要等待{delay}秒）")
    # await 是异步的核心：挂起当前任务，让事件循环去执行其他任务
    await asyncio.sleep(delay)  # 模拟耗时操作（比如等待接口响应）
    return f"任务[{name}]执行完成"

# 2. 定义并发执行的主函数
async def main():
    # 步骤1：创建多个异步任务（不会立即执行，只是加入事件循环）
    task1 = asyncio.create_task(simple_async_task("A", 3))  # 耗时3秒
    task2 = asyncio.create_task(simple_async_task("B", 1))  # 耗时1秒
    task3 = asyncio.create_task(simple_async_task("C", 2))  # 耗时2秒

    # 步骤2：并发等待所有任务完成，并收集结果（核心！）
    # await asyncio.gather(...) 会等待所有任务执行完毕，返回结果列表
    results = await asyncio.gather(task1, task2, task3)

    # 步骤3：打印结果（顺序和创建任务的顺序一致）
    print("\n所有任务执行完毕，结果列表：")
    for result in results:
        print(f"- {result}")

# 3. 运行异步主函数（Python 3.7+ 推荐用法）
if __name__ == "__main__":
    asyncio.run(main())