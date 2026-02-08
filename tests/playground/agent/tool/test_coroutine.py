import asyncio
import threading
import time

# ---------------------- 定义协程函数 ----------------------
# 主线程要执行的协程任务
async def main_coroutine():
    """主线程的协程任务：每秒打印一次主线程协程状态"""
    for i in range(5):
        print(f"【主线程协程】运行中，计数: {i} | 当前线程: {threading.current_thread().name}")
        await asyncio.sleep(1)  # 协程休眠（非阻塞）
    print("【主线程协程】任务执行完毕")

# 子线程要执行的协程任务
async def sub_coroutine():
    """子线程的协程任务：每秒打印一次子线程协程状态"""
    for i in range(5):
        print(f"  【子线程协程】运行中，计数: {i} | 当前线程: {threading.current_thread().name}")
        await asyncio.sleep(1)  # 协程休眠（非阻塞）
    print("  【子线程协程】任务执行完毕")

# ---------------------- 子线程入口函数 ----------------------
def sub_thread_entry():
    """子线程的入口函数：初始化子线程的事件循环并运行协程"""
    # 关键：为子线程创建独立的事件循环
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)  # 将新循环设为当前线程的默认循环
    
    # # 在子线程中运行协程
    # loop.run_until_complete(sub_coroutine())
    # loop.close()  # 任务完成后关闭循环
    asyncio.run(sub_coroutine())

# ---------------------- 主线程执行逻辑 ----------------------
if __name__ == "__main__":
    print("程序启动，主线程名称:", threading.current_thread().name)
    
    # 1. 创建并启动子线程（子线程内部会运行协程）
    sub_thread = threading.Thread(target=sub_thread_entry, name="子线程-01")
    sub_thread.start()
    
    # 2. 主线程自身运行协程（主线程的事件循环）
    asyncio.run(main_coroutine())
    
    # 3. 等待子线程完成，保证程序完整退出
    sub_thread.join()
    
    print("所有线程协程任务均已完成，程序退出")