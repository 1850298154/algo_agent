import asyncio
from playwright.async_api import async_playwright, TimeoutError

JD_URL = "https://www.jd.com"


async def wait_for_login(page):
    """
    等待用户完成登录（人来操作）
    """
    print("🧑 请在打开的浏览器中完成【手动登录】京东（扫码/短信均可）")
    print("⏳ 程序将自动检测登录完成状态...")

    try:
        # 登录后才会出现的元素
        await page.wait_for_selector("input#key", timeout=5 * 60 * 1000)
        print("✅ 检测到登录完成（搜索框已出现）")
    except TimeoutError:
        raise RuntimeError("❌ 等待登录超时，请重试")


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,  # 必须 false
            slow_mo=50
        )

        context = await browser.new_context()
        page = await context.new_page()

        print("🌐 打开京东首页")
        await page.goto(JD_URL)

        # ====== 人工登录阶段 ======
        await wait_for_login(page)

        # ====== 登录完成 ======
        await page.screenshot(path="jd_logged_in.png")
        print("📸 已截图 jd_logged_in.png")

        # ====== 搜索商品 ======
        search_input = page.locator("input#key")
        await search_input.fill("RTX 4090")
        await search_input.press("Enter")

        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(3000)

        await page.screenshot(path="jd_search_4090.png")
        print("📸 已截图 jd_search_4090.png")

        print("✅ 全流程完成")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
