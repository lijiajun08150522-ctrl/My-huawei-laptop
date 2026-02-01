"""
自动截图脚本 - 为实训证明生成页面截图
"""
import asyncio
from playwright.async_api import async_playwright
import time
from datetime import datetime


async def capture_screenshots():
    """自动访问三个页面并截图"""

    print("=" * 60)
    print("开始自动截图...")
    print("=" * 60)

    async with async_playwright() as p:
        # 启动浏览器（有头模式）
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # 设置视口大小（桌面分辨率）
        await page.set_viewport_size({"width": 1920, "height": 1080})

        # 页面列表
        pages = [
            {
                "name": "首页",
                "url": "http://localhost:5000/",
                "filename": "screenshot-homepage.png"
            },
            {
                "name": "游戏页",
                "url": "http://localhost:5000/game",
                "filename": "screenshot-game.png"
            },
            {
                "name": "任务页",
                "url": "http://localhost:5000/tasks",
                "filename": "screenshot-tasks.png"
            }
        ]

        screenshots = []

        for i, page_info in enumerate(pages, 1):
            print(f"\n[{i}/{len(pages)}] 正在访问 {page_info['name']}...")
            print(f"    URL: {page_info['url']}")

            try:
                # 访问页面
                await page.goto(page_info['url'], wait_until="networkidle")

                # 等待页面加载完成
                await asyncio.sleep(2)

                # 截图
                await page.screenshot(
                    path=page_info['filename'],
                    full_page=False
                )

                screenshots.append(page_info['filename'])
                print(f"    ✅ 截图成功: {page_info['filename']}")

            except Exception as e:
                print(f"    ❌ 截图失败: {e}")

        await browser.close()

        print("\n" + "=" * 60)
        print("截图完成！")
        print("=" * 60)
        print(f"\n生成的截图文件:")
        for filename in screenshots:
            print(f"  - {filename}")
        print(f"\n保存位置: d:\\SummerProject\\")
        print("=" * 60)


if __name__ == "__main__":
    print("\n使用前请确保:")
    print("1. Flask服务已启动 (python app.py)")
    print("2. 服务运行在 http://localhost:5000")
    print("3. 已安装 playwright: pip install playwright")
    print("4. 已安装浏览器: playwright install chromium")
    print("\n")

    # 确认启动
    input("按回车键开始截图...")

    # 运行截图
    asyncio.run(capture_screenshots())
