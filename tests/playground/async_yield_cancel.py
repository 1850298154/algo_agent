
import asyncio

async def gen():
    yield 1
    await asyncio.sleep(10)
    yield 2

async def main():
    g = gen()
    await anext(g)
    print('async main over')
async def main():
    g = gen()
    try:
        async for x in g:
            return x
    finally:
        await g.aclose()
    # await anext(g)     # StopAsyncIteration
    print('async main over')

x = asyncio.run(main())
print('py over', x)
