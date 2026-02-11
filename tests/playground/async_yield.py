import asyncio
async def async_generator():
    yield 1
    await asyncio.sleep(2)
    yield 2
async def main():
    async for num in async_generator():
        print(num)
asyncio.run(main())