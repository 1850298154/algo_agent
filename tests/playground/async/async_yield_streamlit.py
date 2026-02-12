import streamlit as st
import asyncio

# 1. 定义异步生成器（复用之前的示例）
async def async_generator(n: int):
    for i in range(n):
        await asyncio.sleep(1)  # 模拟异步IO
        yield f"异步产出值 {i}"

# 2. Streamlit中调用异步逻辑（原生支持async，无需asyncio.run()）
async def main():
    st.title("Streamlit + 异步生成器示例")
    
    # Streamlit交互组件（不要放asyncio.run里！）
    n = st.slider("生成数量", 1, 5, 3)
    if st.button("开始生成"):
        st.write("开始异步生成...")
        # 遍历异步生成器
        async for val in async_generator(n):
            st.write(val)

# 3. 关键：Streamlit运行异步主函数（无需手动管理循环）
if __name__ == "__main__":
    # 错误写法（会报错）：asyncio.run(main())
    # 正确写法：Streamlit原生支持，直接调用async函数
    asyncio.run(main())  # 仅在脚本入口调用一次！（不推荐，更推荐下面的写法）
    
    # 🌟 更推荐的写法（Streamlit 1.18+）：无需asyncio.run()
    # await main()  # 直接在顶层await，Streamlit会自动处理