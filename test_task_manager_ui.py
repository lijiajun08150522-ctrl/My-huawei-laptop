#!/usr/bin/env python3
"""
任务管理器 Web UI 自动化测试
模拟真实用户在浏览器中的操作流程
"""

from playwright.sync_api import sync_playwright
import os
import time


class TaskManagerUITest:
    """任务管理器UI测试类"""

    def __init__(self):
        self.test_results = []
        self.passed = 0
        self.failed = 0

    def log(self, message, status="info"):
        """记录测试日志"""
        icon = {
            "pass": "[PASS]",
            "fail": "[FAIL]",
            "info": "[INFO]"
        }.get(status, "[LOG]")
        print(f"{icon} {message}")

    def assert_true(self, condition, message):
        """断言条件为真"""
        if condition:
            self.passed += 1
            self.log(message, "pass")
            return True
        else:
            self.failed += 1
            self.log(message, "fail")
            return False

    def assert_equal(self, actual, expected, message):
        """断言相等"""
        if actual == expected:
            self.passed += 1
            self.log(message, "pass")
            return True
        else:
            self.failed += 1
            self.log(f"{message} (期望: {expected}, 实际: {actual})", "fail")
            return False

    def run_tests(self):
        """运行所有UI测试"""
        print("=" * 70)
        print("任务管理器 Web UI 自动化测试")
        print("=" * 70)

        html_path = os.path.abspath("task_manager.html")

        with sync_playwright() as p:
            # 启动浏览器（非headless模式以便观察）
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(viewport={'width': 1200, 'height': 800})
            page = context.new_page()

            # 打开本地HTML文件
            file_url = f"file:///{html_path}"
            page.goto(file_url)
            self.log("打开任务管理器页面", "info")

            # 测试1: 页面初始状态
            print("\n" + "=" * 70)
            print("测试1: 页面初始状态检查")
            print("=" * 70)

            page.wait_for_load_state('networkidle')

            # 检查标题
            title = page.title()
            self.assert_equal(title, "任务管理器", "页面标题正确")

            # 检查空状态提示
            empty_state = page.locator('#emptyState')
            self.assert_true(empty_state.is_visible(), "空状态提示可见")
            self.assert_equal(empty_state.inner_text(), "暂无任务，添加一个吧！", "空状态提示文本正确")

            # 检查任务列表为空
            task_list = page.locator('#taskList .task-item')
            self.assert_equal(task_list.count(), 0, "初始任务列表为空")

            # 测试2: 添加单个任务
            print("\n" + "=" * 70)
            print("测试2: 添加单个任务")
            print("=" * 70)

            task_input = page.locator('#taskInput')
            add_button = page.locator('#addButton')

            # 用户输入任务描述
            self.log("用户在输入框输入: '完成项目文档'", "info")
            task_input.fill("完成项目文档")
            self.assert_equal(task_input.input_value(), "完成项目文档", "输入框内容正确")

            # 用户点击添加按钮
            self.log("用户点击添加按钮", "info")
            add_button.click()

            # 等待任务添加
            page.wait_for_timeout(500)

            # 验证任务已添加
            task_list = page.locator('#taskList .task-item')
            self.assert_equal(task_list.count(), 1, "任务已添加到列表")

            # 验证任务内容
            first_task = task_list.first
            task_text = first_task.locator('.task-text')
            self.assert_equal(task_text.inner_text(), "完成项目文档", "任务描述正确")

            task_status = first_task.locator('.task-status')
            self.assert_equal(task_status.inner_text(), "待完成", "任务初始状态为待完成")
            self.assert_true(task_status.get_attribute('class').endswith('pending'), "任务状态样式正确")

            # 验证输入框已清空
            self.assert_equal(task_input.input_value(), "", "添加后输入框已清空")

            # 验证空状态已隐藏
            empty_state = page.locator('#emptyState')
            self.assert_true(not empty_state.is_visible(), "空状态提示已隐藏")

            # 测试3: 添加多个任务
            print("\n" + "=" * 70)
            print("测试3: 添加多个任务")
            print("=" * 70)

            # 使用回车键添加任务
            self.log("用户使用回车键添加任务", "info")
            task_input.fill("编写测试用例")
            task_input.press('Enter')
            page.wait_for_timeout(500)
            self.assert_equal(task_list.count(), 2, "第二个任务已添加")

            # 继续添加任务
            task_input.fill("代码审查")
            add_button.click()
            page.wait_for_timeout(500)
            self.assert_equal(task_list.count(), 3, "第三个任务已添加")

            task_input.fill("部署到生产环境")
            task_input.press('Enter')
            page.wait_for_timeout(500)
            self.assert_equal(task_list.count(), 4, "第四个任务已添加")

            # 验证所有任务
            all_task_texts = page.locator('#taskList .task-text').all_text_contents()
            self.assert_equal(len(all_task_texts), 4, "共有4个任务")
            self.assert_true("完成项目文档" in all_task_texts, "第一个任务存在")
            self.assert_true("编写测试用例" in all_task_texts, "第二个任务存在")
            self.assert_true("代码审查" in all_task_texts, "第三个任务存在")
            self.assert_true("部署到生产环境" in all_task_texts, "第四个任务存在")

            # 测试4: 标记任务完成
            print("\n" + "=" * 70)
            print("测试4: 标记任务完成")
            print("=" * 70)

            # 获取第一个任务的复选框
            first_task_checkbox = page.locator('#taskList .task-item:first-child .task-checkbox')
            self.assert_true(not first_task_checkbox.is_checked(), "第一个任务初始未选中")

            # 用户点击复选框
            self.log("用户点击第一个任务的复选框", "info")
            first_task_checkbox.click()
            page.wait_for_timeout(500)

            # 验证任务已标记为完成
            self.assert_true(first_task_checkbox.is_checked(), "复选框已选中")

            first_task_item = page.locator('#taskList .task-item:first-child')
            task_status = first_task_item.locator('.task-status')
            self.assert_equal(task_status.inner_text(), "已完成", "任务状态已更新为已完成")
            self.assert_true(task_status.get_attribute('class').endswith('done'), "任务状态样式已更新")

            # 验证任务样式变化
            self.assert_true(first_task_item.get_attribute('class').endswith('completed'), "任务项样式已更新")

            # 验证删除线效果
            task_text = first_task_item.locator('.task-text')
            computed_style = task_text.evaluate("el => window.getComputedStyle(el).textDecoration")
            self.assert_true("line-through" in computed_style, "任务文本有删除线效果")

            # 测试5: 取消任务完成状态
            print("\n" + "=" * 70)
            print("测试5: 取消任务完成状态")
            print("=" * 70)

            self.log("用户再次点击复选框", "info")
            first_task_checkbox.click()
            page.wait_for_timeout(500)

            self.assert_true(not first_task_checkbox.is_checked(), "复选框已取消选中")

            first_task_item = page.locator('#taskList .task-item:first-child')
            task_status = first_task_item.locator('.task-status')
            self.assert_equal(task_status.inner_text(), "待完成", "任务状态已恢复为待完成")

            # 测试6: 删除任务
            print("\n" + "=" * 70)
            print("测试6: 删除任务")
            print("=" * 70)

            task_count_before = page.locator('#taskList .task-item').count()
            self.log(f"删除前任务数: {task_count_before}", "info")

            # 用户点击删除按钮
            self.log("用户点击第二个任务的删除按钮", "info")
            second_task_delete = page.locator('#taskList .task-item:nth-child(2) .delete-button')
            second_task_delete.click()
            page.wait_for_timeout(500)

            # 验证任务已删除
            task_count_after = page.locator('#taskList .task-item').count()
            self.assert_equal(task_count_after, task_count_before - 1, "任务已删除")

            # 验证剩余任务
            remaining_tasks = page.locator('#taskList .task-text').all_text_contents()
            self.assert_true("编写测试用例" not in remaining_tasks, "已删除的任务不在列表中")

            # 测试7: 清除已完成任务
            print("\n" + "=" * 70)
            print("测试7: 清除已完成任务")
            print("=" * 70)

            # 先标记几个任务为完成
            self.log("标记第一个和第三个任务为完成", "info")
            page.locator('#taskList .task-item:nth-child(1) .task-checkbox').click()
            page.wait_for_timeout(300)
            page.locator('#taskList .task-item:nth-child(3) .task-checkbox').click()
            page.wait_for_timeout(300)

            task_count_before_clear = page.locator('#taskList .task-item').count()
            completed_count_before = page.locator('#taskList .task-item.completed').count()
            self.log(f"清除前任务数: {task_count_before_clear}, 已完成: {completed_count_before}", "info")

            # 用户点击清除已完成任务按钮
            self.log("用户点击'清除已完成任务'按钮", "info")
            clear_button = page.locator('#clearButton')
            clear_button.click()

            # 处理弹窗
            page.on("dialog", lambda dialog: dialog.accept())
            page.wait_for_timeout(1000)

            # 验证已完成的任务已被清除
            task_count_after_clear = page.locator('#taskList .task-item').count()
            completed_count_after = page.locator('#taskList .task-item.completed').count()

            self.assert_equal(completed_count_after, 0, "已完成任务已全部清除")
            self.assert_equal(task_count_after_clear, task_count_before_clear - completed_count_before, "剩余任务数正确")

            # 测试8: 输入验证
            print("\n" + "=" * 70)
            print("测试8: 输入验证")
            print("=" * 70)

            task_count_before = page.locator('#taskList .task-item').count()

            # 尝试添加空任务
            self.log("用户尝试添加空任务", "info")
            task_input.fill("")
            add_button.click()

            # 验证弹窗提示
            page.on("dialog", lambda dialog: dialog.accept())
            page.wait_for_timeout(500)

            # 验证任务未添加
            task_count_after = page.locator('#taskList .task-item').count()
            self.assert_equal(task_count_after, task_count_before, "空任务未添加")

            # 尝试添加纯空格任务
            self.log("用户尝试添加纯空格任务", "info")
            task_input.fill("   ")
            add_button.click()
            page.on("dialog", lambda dialog: dialog.accept())
            page.wait_for_timeout(500)

            task_count_after = page.locator('#taskList .task-item').count()
            self.assert_equal(task_count_after, task_count_before, "纯空格任务未添加")

            # 测试9: 响应式布局
            print("\n" + "=" * 70)
            print("测试9: 响应式布局测试")
            print("=" * 70)

            viewports = [
                {'width': 1920, 'height': 1080, 'name': '桌面'},
                {'width': 768, 'height': 1024, 'name': '平板'},
                {'width': 375, 'height': 667, 'name': '手机'}
            ]

            for vp in viewports:
                self.log(f"切换到{vp['name']}视图 ({vp['width']}x{vp['height']})", "info")
                page.set_viewport_size({'width': vp['width'], 'height': vp['height']})
                page.wait_for_timeout(300)

                # 验证页面元素仍然可见
                self.assert_true(page.locator('#taskInput').is_visible(), f"{vp['name']}视图输入框可见")
                self.assert_true(page.locator('#addButton').is_visible(), f"{vp['name']}视图添加按钮可见")

            # 恢复桌面视图
            page.set_viewport_size({'width': 1200, 'height': 800})

            # 测试10: 截图
            print("\n" + "=" * 70)
            print("测试10: 页面截图")
            print("=" * 70)

            screenshot_path = os.path.join(os.path.dirname(__file__), "task_manager_screenshot.png")
            page.screenshot(path=screenshot_path, full_page=True)
            self.log(f"截图已保存到: {screenshot_path}", "pass")

            # 等待用户观察
            self.log("\n等待5秒以便观察测试结果...", "info")
            time.sleep(5)

            # 关闭浏览器
            browser.close()

        # 输出测试结果
        print("\n" + "=" * 70)
        print("测试结果汇总")
        print("=" * 70)
        total = self.passed + self.failed
        print(f"总计: {total} 个断言")
        print(f"通过: {self.passed} 个")
        print(f"失败: {self.failed} 个")
        print(f"成功率: {(self.passed/total*100):.1f}%")
        print("=" * 70)

        return self.failed == 0


if __name__ == "__main__":
    tester = TaskManagerUITest()
    success = tester.run_tests()
    exit(0 if success else 1)
