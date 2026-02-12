# import asyncio
# async def async_generator():
#     for i in range(2):
#         yield i
#         await asyncio.sleep(2)
#     # yield 3
#     # raise StopIteration()
#     # raise StopAsyncIteration()
    
# async def main():
#     async for num in async_generator():
#         print(num)
#     # result = await async_generator()
#     # print(result) #TypeError: object async_generator can't be used in 'await' expression
# asyncio.run(main())



# import asyncio

# async def async_generator():
#     for i in range(5):
#         yield i
#         await asyncio.sleep(1)
#         if i == 2:  # 假设i为2时提前结束
#             yield StopAsyncIteration() # 什么都不做，多输出空格
#             """
# 0
# 1
# 2

# 3
# 4            
#             """
#             # raise StopAsyncIteration() 拦不住，只能到    except Exception as e:


# async def main():
#     try:
#         async for num in async_generator():
#             print(num)
#     except StopAsyncIteration as e:
#         print(f"StopAsyncIteration as e: An error occurred: {e}")
#     except Exception as e:
#         print(f"Exception as e: An error occurred: {e}")

# asyncio.run(main())





# ####### 推荐

# import asyncio

# async def async_generator():
#     for i in range(5):
#         yield i
#         await asyncio.sleep(1)
#         if i == 2:  # 提前终止循环，让生成器自然结束
#             break  # 替换 raise StopAsyncIteration()

# async def main():
#     try:
#         gen=async_generator()
#         print('gen', gen)
#         a=await anext(gen)
#         print('next ', a)
        
#         async for num in async_generator():
#             print(num)
#     except StopAsyncIteration as e:
#         print(f"StopAsyncIteration as e: An error occurred: {e}")
#     except Exception as e:
#         print(f"Exception as e: An error occurred: {e}")

# asyncio.run(main())



import asyncio

async def inner_async_generator(i):
    for j in range(2):
        yield i*10+j
async def async_generator():
    for i in range(5):
        # async for v in inner_async_func(i):  # 使用 async for 来委托异步生成器
        #     yield v
        yield inner_async_generator(i)
        await asyncio.sleep(1)
        if i == 2:  # 提前终止循环，让生成器自然结束
            break  # 替换 raise StopAsyncIteration()

async def main():
    try:
        gen=async_generator()
        print('gen', gen)
        a=await anext(gen)
        print('next ', a)
        """
        gen   <async_generator object async_generator at 0x000001C3BB1735E0>
        next  <async_generator object inner_async_generator at 0x000001C3BD1F9A40>
        """
        async for num in async_generator():
            print(num)
    except StopAsyncIteration as e:
        print(f"StopAsyncIteration as e: An error occurred: {e}")
    except Exception as e:
        print(f"Exception as e: An error occurred: {e}")

# asyncio.run(main())
# ✅ 方案 1（推荐）：直接 await

# Streamlit 现在支持 async 函数：

# import streamlit as st


# async def main():
#     async for x in async_generator():
#         st.write(x)


# st.run(main())  # 或在 async context 直接 await
# # ✅ 方案 2：复用已有 loop
# loop = asyncio.get_event_loop()
# loop.create_task(main())

# # 不要 run

# # ✅ 方案 3（最稳）：转同步包装
# def run_async(coro):
#     return asyncio.get_event_loop().run_until_complete(coro)


# run_async(main())

# try:
#     loop = asyncio.get_running_loop()
#     loop.create_task(main())

# except RuntimeError:
#     # 没有 running loop（普通 python 启动）
#     asyncio.run(main())
# https://chatgpt.com/c/698cd36f-bdd0-8320-bb26-b28fac55a457

import asyncio

async def inner_async_generator(i):
    for j in range(2):
        yield i * 10 + j    
async def async_generator():
    for i in range(5):
        # yield inner_async_generator(i)  # yield 返回的是生成器
        # yield from inner_async_generator(i)  # 使用 yield from 来委托生成器， 不支持在异步中
        async for v in inner_async_generator(i):  # 使用 async for 来委托异步生成器
            yield v        
        await asyncio.sleep(1)
        if i == 3:  # 提前终止循环，让生成器自然结束
            break  # 替换 raise StopAsyncIteration()

async def main():
    try:
        gen=async_generator()
        print('gen', gen)
        a=await anext(gen)
        print('next ', a)
        """
        gen   <async_generator object async_generator at 0x000001C3BD2B57D0>
        next  <async_generator object inner_async_generator at 0x000001C3BD2B5D80>        
        """
        
        async for num in async_generator():
            print(num)
    except StopAsyncIteration as e:
        print(f"StopAsyncIteration as e: An error occurred: {e}")
    except Exception as e:
        print(f"Exception as e: An error occurred: {e}")
    print("after async yield , ok")

# asyncio.run(main())

try:
    loop = asyncio.get_running_loop()
    loop.create_task(main())

except RuntimeError:
    # 没有 running loop（普通 python 启动）
    asyncio.run(main())
print("over main")
"""
gen <async_generator object async_generator at 0x000001BFB6FF35E0>
next  <async_generator object inner_async_generator at 0x000001BFB90A5B10>
<async_generator object inner_async_generator at 0x000001BFB90A60C0>
<async_generator object inner_async_generator at 0x000001BFB91658A0>
<async_generator object inner_async_generator at 0x000001BFB90A60C0>
gen <async_generator object async_generator at 0x000001BFB9198BA0>
next  0
0
1
10
11
20
21
"""