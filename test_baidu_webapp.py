#!/usr/bin/env python3
"""
百度官网自动化测试
使用 Playwright 进行网页功能测试和验证
"""

from playwright.sync_api import sync_playwright
import time


def test_baidu_website():
    """测试百度官网功能"""

    with sync_playwright() as p:
        print("=" * 60)
        print("开始测试百度官网")
        print("=" * 60)

        # 启动浏览器
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # 捕获控制台日志
        console_messages = []

        def handle_console(msg):
            console_messages.append(msg)

        page.on("console", handle_console)

        # 1. 页面加载测试
        print("\n[1/7] 页面加载测试...")
        try:
            start_time = time.time()
            page.goto('https://www.baidu.com', timeout=30000)
            load_time = time.time() - start_time
            print(f"    ✓ 页面加载成功 (耗时: {load_time:.2f}秒)")

            # 等待页面完全加载
            page.wait_for_load_state('networkidle', timeout=10000)
            print(f"    ✓ 网络空闲状态已达到")
        except Exception as e:
            print(f"    ✗ 页面加载失败: {e}")
            browser.close()
            return False

        # 2. 页面标题验证
        print("\n[2/7] 页面标题验证...")
        try:
            title = page.title()
            print(f"    ✓ 页面标题: {title}")
        except Exception as e:
            print(f"    ✗ 获取标题失败: {e}")

        # 3. 搜索框功能测试
        print("\n[3/7] 搜索框功能测试...")
        try:
            # 查找搜索框
            search_input = page.locator('#kw')
            if search_input.count() > 0:
                print(f"    ✓ 搜索框元素存在")

                # 输入测试文本
                search_input.fill('Playwright测试')
                print(f"    ✓ 成功输入测试文本")

                # 查找搜索按钮
                search_button = page.locator('#su')
                if search_button.count() > 0:
                    print(f"    ✓ 搜索按钮存在")

                    # 点击搜索
                    with page.expect_navigation(timeout=10000):
                        search_button.click()
                    print(f"    ✓ 搜索触发成功")

                    # 等待搜索结果页加载
                    page.wait_for_load_state('networkidle', timeout=10000)
                    print(f"    ✓ 搜索结果页加载完成")
                else:
                    print(f"    ✗ 搜索按钮未找到")
            else:
                print(f"    ✗ 搜索框未找到")
        except Exception as e:
            print(f"    ✗ 搜索功能测试失败: {e}")

        # 4. 页面元素发现
        print("\n[4/7] 页面元素发现...")

        # 查找按钮
        try:
            buttons = page.locator('button').all()
            print(f"    ✓ 找到 {len(buttons)} 个按钮")
            for i, btn in enumerate(buttons[:3]):  # 显示前3个
                text = btn.inner_text() if btn.is_visible() else "[隐藏]"
                print(f"       [{i+1}] {text[:50]}")
        except Exception as e:
            print(f"    ✗ 按钮查找失败: {e}")

        # 查找链接
        try:
            links = page.locator('a[href]').all()
            print(f"    ✓ 找到 {len(links)} 个链接")
            for link in links[:5]:  # 显示前5个
                text = link.inner_text().strip()[:30]
                href = link.get_attribute('href')
                if href and text:
                    print(f"       - {text} -> {href[:50]}")
        except Exception as e:
            print(f"    ✗ 链接查找失败: {e}")

        # 5. 响应式布局测试
        print("\n[5/7] 响应式布局测试...")
        viewports = [
            {'width': 1920, 'height': 1080, 'name': '桌面'},
            {'width': 768, 'height': 1024, 'name': '平板'},
            {'width': 375, 'height': 667, 'name': '手机'}
        ]

        for vp in viewports:
            try:
                page.set_viewport_size({'width': vp['width'], 'height': vp['height']})
                page.wait_for_load_state('networkidle')
                print(f"    ✓ {vp['name']} ({vp['width']}x{vp['height']}) 布局正常")
            except Exception as e:
                print(f"    ✗ {vp['name']} 布局测试失败: {e}")

        # 6. 性能指标
        print("\n[6/7] 性能指标...")
        try:
            metrics = page.evaluate('''() => {
                const timing = performance.timing;
                return {
                    domContentLoaded: timing.domContentLoadedEventEnd - timing.navigationStart,
                    loadComplete: timing.loadEventEnd - timing.navigationStart,
                    domInteractive: timing.domInteractive - timing.navigationStart
                };
            }''')

            print(f"    ✓ DOM内容加载: {metrics['domContentLoaded']:.0f}ms")
            print(f"    ✓ DOM交互就绪: {metrics['domInteractive']:.0f}ms")
            print(f"    ✓ 页面完全加载: {metrics['loadComplete']:.0f}ms")
        except Exception as e:
            print(f"    ✗ 性能指标获取失败: {e}")

        # 7. 截图保存
        print("\n[7/7] 保存页面截图...")
        try:
            page.set_viewport_size({'width': 1920, 'height': 1080})
            page.screenshot(path='d:/SummerProject/baidu_screenshot.png', full_page=True)
            print(f"    ✓ 截图已保存到: baidu_screenshot.png")
        except Exception as e:
            print(f"    ✗ 截图保存失败: {e}")

        # 显示控制台日志摘要
        if console_messages:
            print(f"\n控制台日志: {len(console_messages)} 条")
            errors = [msg for msg in console_messages if msg.type == 'error']
            warnings = [msg for msg in console_messages if msg.type == 'warning']
            if errors:
                print(f"    错误: {len(errors)} 条")
            if warnings:
                print(f"    警告: {len(warnings)} 条")

        # 关闭浏览器
        browser.close()

        print("\n" + "=" * 60)
        print("测试完成!")
        print("=" * 60)

        return True


if __name__ == "__main__":
    success = test_baidu_website()
    exit(0 if success else 1)
