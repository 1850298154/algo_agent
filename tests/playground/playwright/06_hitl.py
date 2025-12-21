from playwright.async_api import async_playwright, Page
import asyncio
import tkinter as tk
from tkinter import messagebox


class LoginConfirmDialog:
    """
    一个独立桌面窗口（不注入网页），用户点“我已登录”才放行。
    - 跨平台：Windows / macOS / Linux（Python 自带 tkinter）
    - 不会因网页刷新而丢失
    """
    def __init__(self, title: str = "Agent Human-in-the-Loop"):
        self._title = title
        self._confirmed = False

    def show(self, tip: str = "请在浏览器中完成登录（含验证码等），完成后点击“我已登录，继续”。") -> bool:
        root = tk.Tk()
        root.title(self._title)
        root.geometry("520x180")
        root.resizable(False, False)

        # 置顶（尽量）
        try:
            root.attributes("-topmost", True)
        except Exception:
            pass

        frame = tk.Frame(root, padx=16, pady=16)
        frame.pack(fill="both", expand=True)

        lbl = tk.Label(frame, text=tip, justify="left", wraplength=480)
        lbl.pack(anchor="w")

        btn_row = tk.Frame(frame, pady=18)
        btn_row.pack(fill="x")

        def on_confirm():
            self._confirmed = True
            root.destroy()

        def on_cancel():
            self._confirmed = False
            root.destroy()

        confirm_btn = tk.Button(btn_row, text="我已登录，继续", width=18, command=on_confirm)
        confirm_btn.pack(side="left")

        cancel_btn = tk.Button(btn_row, text="取消/退出", width=12, command=on_cancel)
        cancel_btn.pack(side="left", padx=10)

        root.protocol("WM_DELETE_WINDOW", on_cancel)
        root.mainloop()
        return self._confirmed


async def wait_for_user_confirm_desktop() -> bool:
    # tkinter 是阻塞的，用线程跑，避免卡住 asyncio
    dialog = LoginConfirmDialog()
    return await asyncio.to_thread(dialog.show)


async def ensure_login(page: Page) -> None:
    print("👉 请在浏览器中完成登录；将弹出桌面窗口等待你确认。")
    ok = await wait_for_user_confirm_desktop()
    if not ok:
        raise RuntimeError("User cancelled login confirmation")

    # 可选：确认后给一点缓冲
    await page.wait_for_timeout(800)


async def main():
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            "jd_profile",
            headless=False,
            args=["--disable-blink-features=AutomationControlled"],
        )

        page = await context.new_page()
        await page.goto("https://www.jd.com", wait_until="domcontentloaded")

        # 1) 登录（人机协作确认，不注入网页）
        await ensure_login(page)
        print("✅ 用户确认登录完成，进入后续流程")

        # 2) 后续操作（示例：搜索并截图）
        await page.goto("https://search.jd.com/Search?keyword=RTX%204090", wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        await page.screenshot(path="jd_4090.png", full_page=True)

        await context.close()


if __name__ == "__main__":
    asyncio.run(main())