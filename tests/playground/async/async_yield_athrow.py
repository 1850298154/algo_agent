import asyncio
async def async_gen_with_throw():
    try:
        yield 1
        yield 2
        yield 3
    except ValueError as e:
        print(f"捕获注入的异常：{e}")
        yield "异常后的值"

async def main():
    gen = async_gen_with_throw()
    val = await anext(gen)  # 获取值1
    print(f"初始值：{val}")
    val = await gen.athrow(ValueError, "手动注入异常")  # 向暂停点注入异常
    print(f"注入异常后的值：{val}")
    val = await anext(gen)#StopAsyncIteration   # 异常处理后继续执行，获取"异常后的值" 
    print(f"最终值：{val}")

asyncio.run(main())