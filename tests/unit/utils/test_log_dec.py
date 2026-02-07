from src.utils.l import global_logger, traceable
from typing import Any, Dict

if __name__ == "__main__":
    import asyncio

    # 测试同步函数
    @traceable
    def test_sync_function(a: int, b: str, c: Dict[str, Any]) -> Dict[str, Any]:
        """普通同步测试函数"""
        return {"result": a + int(b) + c["key"]}

    # 测试协程函数（新增）
    @traceable
    async def test_async_function(a: int, b: str, c: Dict[str, Any]) -> Dict[str, Any]:
        """协程测试函数"""
        await asyncio.sleep(0.1)  # 模拟异步操作
        return {"async_result": a + int(b) + c["key"]}
    # 测试协程函数（新增）
    @traceable
    async def test_async_function2(a: int, b: str, c: Dict[str, Any]) -> Dict[str, Any]:
        """协程测试函数"""
        await asyncio.sleep(0.1)  # 模拟异步操作
        1/0
        return {"async_result": a + int(b) + c["key"]}

    # 执行同步测试
    ret_sync = test_sync_function(1, "2", {"key": 3})
    global_logger.debug(f"同步函数结果：{ret_sync}")

    # 执行异步测试
    async def main():
        try:
            ret_async = await test_async_function(1, "2", {"key": 3})
            global_logger.debug(f"协程函数结果：{ret_async}")
            ret_async = await test_async_function2(1, "2", {"key": 3})
            global_logger.debug(f"协程函数结果：{ret_async}")
        except Exception as e:
            pass
    asyncio.run(main())