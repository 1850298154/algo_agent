# jd_auto.py
from playwright.async_api import async_playwright
import asyncio

async def main():
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
