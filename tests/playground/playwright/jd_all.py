# jd_auto.py
from playwright.async_api import async_playwright
import asyncio

async def main():
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir="jd_profile",  # 关键：保存登录态
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled"
            ]
        )

        page = await context.new_page()
        await page.goto("https://www.jd.com")

        print("👉 请手动登录京东（扫码/账号）")
        await page.wait_for_timeout(120_000)  # 给你 2 分钟登录

        print("✅ 登录完成，关闭浏览器")
        await context.close()
        
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir="jd_profile",  # 使用同一个目录
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )

        page = await context.new_page()
        await page.goto("https://search.jd.com/Search?keyword=RTX%204090")

        await page.wait_for_timeout(5000)
        await page.screenshot(path="jd_4090.png")

        print("截图完成")

        await context.close()

asyncio.run(main())
