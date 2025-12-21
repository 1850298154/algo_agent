from playwright.async_api import async_playwright
import asyncio

async def wait_for_user_confirm(page):
    # 注入一个按钮
    await page.evaluate("""
        () => {
            if (document.getElementById('__agent_confirm')) return;

            const btn = document.createElement('button');
            btn.id = '__agent_confirm';
            btn.innerText = '✅ 我已登录，继续';
            btn.style = `
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 99999;
                padding: 12px 16px;
                font-size: 14px;
                background: #e1251b;
                color: white;
                border: none;
                border-radius: 6px;
                cursor: pointer;
            `;
            btn.onclick = () => {
                window.__LOGIN_CONFIRMED__ = true;
            };
            document.body.appendChild(btn);
        }
    """)

    print("👉 请手动登录，然后点击右上角「我已登录，继续」")

    # 无限等待，直到用户点按钮
    await page.wait_for_function("window.__LOGIN_CONFIRMED__ === true")

async def main():
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            "jd_profile",
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )

        page = await context.new_page()
        await page.goto("https://www.jd.com")

        await wait_for_user_confirm(page)

        print("✅ 用户确认登录完成，进入后续流程")

        await page.goto("https://search.jd.com/Search?keyword=RTX%204090")
        await page.wait_for_timeout(3000)
        await page.screenshot(path="jd_4090.png")

        await context.close()

asyncio.run(main())
