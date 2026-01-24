"""
任务管理CLI工具 - 测试文件
"""

import os
import json
import sys
from task import Task, TaskManager


# ==================== 测试工具函数 ====================

class TaskTester:
    """测试框架"""

    def __init__(self):
        self.test_file = "test_tasks.json"
        self.passed = 0
        self.failed = 0

    def setup(self):
        """测试前准备"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def teardown(self):
        """测试后清理"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def assert_equal(self, actual, expected, message=""):
        """断言相等"""
        if actual == expected:
            self.passed += 1
            print(f"[PASS] {message}")
        else:
            self.failed += 1
            print(f"[FAIL] {message}")
            print(f"  Expected: {expected}")
            print(f"  Actual: {actual}")

    def assert_true(self, condition, message=""):
        """断言为真"""
        if condition:
            self.passed += 1
            print(f"[PASS] {message}")
        else:
            self.failed += 1
            print(f"[FAIL] {message}")

    def print_summary(self):
        """打印测试结果"""
        total = self.passed + self.failed
        print(f"\n{'='*50}")
        print(f"测试结果: {self.passed}/{total} 通过")
        if self.failed > 0:
            print(f"失败: {self.failed}")
        print(f"{'='*50}")
        return self.failed == 0


# ==================== 测试用例 ====================

def test_add_tasks(tester: TaskTester):
    """测试1: 添加3个任务"""
    print("\n测试1: 添加任务")
    manager = TaskManager(tester.test_file)

    result1 = manager.add("学习Python")
    tester.assert_equal(result1, "Added: 学习Python", "添加第一个任务")

    result2 = manager.add("完成作业")
    tester.assert_equal(result2, "Added: 完成作业", "添加第二个任务")

    result3 = manager.add("阅读文档")
    tester.assert_equal(result3, "Added: 阅读文档", "添加第三个任务")

    # 验证任务数量
    tester.assert_equal(len(manager.tasks), 3, "任务数量应为3")


def test_list_tasks(tester: TaskTester):
    """测试2: 列出任务"""
    print("\n测试2: 列出任务")
    manager = TaskManager(tester.test_file)

    manager.add("任务A")
    manager.add("任务B")

    tasks = manager.list()
    tester.assert_equal(len(tasks), 2, "应返回2个任务")
    tester.assert_true("[1]" in tasks[0], "第一个任务ID应为1")
    tester.assert_true("任务A" in tasks[0], "第一个任务描述正确")
    tester.assert_true("pending" in tasks[0], "任务状态应为pending")


def test_complete_task(tester: TaskTester):
    """测试3: 完成任务"""
    print("\n测试3: 完成任务")
    manager = TaskManager(tester.test_file)

    manager.add("待完成任务")
    result = manager.done(1)
    tester.assert_equal(result, "Task 1 marked as done", "任务应标记为完成")

    tasks = manager.list()
    tester.assert_true("done" in tasks[0], "任务状态应为done")


def test_delete_task(tester: TaskTester):
    """测试4: 删除任务"""
    print("\n测试4: 删除任务")
    manager = TaskManager(tester.test_file)

    manager.add("任务1")
    manager.add("任务2")
    manager.add("任务3")

    result = manager.delete(2)
    tester.assert_equal(result, "Task 2 deleted", "应成功删除任务2")
    tester.assert_equal(len(manager.tasks), 2, "剩余任务应为2个")


def test_clear_completed(tester: TaskTester):
    """测试5: 清除已完成任务"""
    print("\n测试5: 清除已完成任务")
    manager = TaskManager(tester.test_file)

    manager.add("任务1")
    manager.add("任务2")
    manager.add("任务3")
    manager.done(1)
    manager.done(3)

    result = manager.clear()
    tester.assert_equal(result, "Cleared all completed tasks", "应清除已完成任务")
    tester.assert_equal(len(manager.tasks), 1, "应剩余1个未完成任务")


def test_error_handling(tester: TaskTester):
    """测试6: 错误处理"""
    print("\n测试6: 错误处理")
    manager = TaskManager(tester.test_file)

    # 测试删除不存在的任务
    result = manager.delete(999)
    tester.assert_equal(result, "Error: Task 999 not found", "应报告任务未找到")

    # 测试完成不存在的任务
    result = manager.done(999)
    tester.assert_equal(result, "Error: Task 999 not found", "应报告任务未找到")

    # 测试添加空描述
    result = manager.add("")
    tester.assert_equal(result, "Error: Task description cannot be empty", "应报告描述为空")

    # 测试空列表
    empty_manager = TaskManager(tester.test_file)
    tasks = empty_manager.list()
    tester.assert_equal(tasks[0], "No tasks found", "空任务列表应提示无任务")


def test_persistence(tester: TaskTester):
    """测试7: 数据持久化"""
    print("\n测试7: 数据持久化")
    manager1 = TaskManager(tester.test_file)
    manager1.add("持久化测试")
    manager1.done(1)

    # 创建新的管理器实例
    manager2 = TaskManager(tester.test_file)
    tester.assert_equal(len(manager2.tasks), 1, "应加载持久化的数据")
    tester.assert_equal(manager2.tasks[0].status, "done", "应加载任务状态")


def test_json_validation(tester: TaskTester):
    """测试8: JSON验证"""
    print("\n测试8: JSON验证")
    test_file = tester.test_file

    # 测试1: 文件不存在时自动创建
    if os.path.exists(test_file):
        os.remove(test_file)
    manager = TaskManager(test_file)
    tester.assert_true(os.path.exists(test_file), "文件不存在时应自动创建")

    # 测试2: 验证空数组文件
    with open(test_file, 'r') as f:
        data = json.load(f)
    tester.assert_equal(data, [], "应创建空数组")

    # 测试3: 无效JSON格式（非数组）
    with open(test_file, 'w') as f:
        json.dump({"not_array": True}, f)
    manager = TaskManager(test_file)
    tester.assert_equal(len(manager.tasks), 0, "无效JSON格式应重置为空数组")

    # 测试4: 跳过无效任务
    with open(test_file, 'w') as f:
        json.dump([
            {"id": 1, "description": "有效任务", "status": "pending"},
            {"id": "invalid", "description": "无效ID", "status": "pending"},
            {"id": 2, "description": "另一个有效任务", "status": "pending"}
        ], f)
    manager = TaskManager(test_file)
    tester.assert_equal(len(manager.tasks), 2, "应跳过无效任务")


def test_backup_creation(tester: TaskTester):
    """测试9: 备份文件创建"""
    print("\n测试9: 备份文件创建")
    manager = TaskManager(tester.test_file)

    manager.add("测试任务")
    backup_file = tester.test_file + '.backup'

    # 验证备份文件被创建
    tester.assert_true(os.path.exists(backup_file), "保存时应创建备份文件")


# ==================== 运行测试 ====================

def run_all_tests():
    """运行所有测试"""
    print("="*50)
    print("开始运行测试套件")
    print("="*50)

    tester = TaskTester()
    tester.setup()

    try:
        test_add_tasks(tester)
        tester.setup()

        test_list_tasks(tester)
        tester.setup()

        test_complete_task(tester)
        tester.setup()

        test_delete_task(tester)
        tester.setup()

        test_clear_completed(tester)
        tester.setup()

        test_error_handling(tester)
        tester.setup()

        test_persistence(tester)
        tester.setup()

        test_json_validation(tester)
        tester.setup()

        test_backup_creation(tester)
        tester.teardown()

    finally:
        tester.teardown()

    return tester.print_summary()


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
