"""
任务管理CLI工具 - 测试文件（重构版）
"""

import sys
from task import Task, TaskManager
from storage import MockTaskStorage
from constants import (
    MSG_ADDED, MSG_TASK_NOT_FOUND, MSG_TASK_MARKED_DONE,
    MSG_TASK_DELETED, MSG_CLEARED_ALL, MSG_EMPTY_DESCRIPTION,
    MSG_NO_TASKS, STATUS_PENDING, STATUS_DONE
)


# ==================== 测试工具函数 ====================

class TaskTester:
    """测试框架"""

    def __init__(self):
        self.passed = 0
        self.failed = 0

    def setup(self):
        """测试前准备（Mock存储自动清理）"""
        pass

    def teardown(self):
        """测试后清理（Mock存储自动清理）"""
        pass

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
    storage = MockTaskStorage()
    manager = TaskManager(storage=storage)

    result1 = manager.add("学习Python")
    tester.assert_equal(result1, MSG_ADDED.format(description="学习Python"), "添加第一个任务")

    result2 = manager.add("完成作业")
    tester.assert_equal(result2, MSG_ADDED.format(description="完成作业"), "添加第二个任务")

    result3 = manager.add("阅读文档")
    tester.assert_equal(result3, MSG_ADDED.format(description="阅读文档"), "添加第三个任务")

    # 验证任务数量
    tester.assert_equal(len(manager.tasks), 3, "任务数量应为3")


def test_list_tasks(tester: TaskTester):
    """测试2: 列出任务"""
    print("\n测试2: 列出任务")
    storage = MockTaskStorage()
    manager = TaskManager(storage=storage)

    manager.add("任务A")
    manager.add("任务B")

    tasks = manager.list()
    tester.assert_equal(len(tasks), 2, "应返回2个任务")
    tester.assert_true("[1]" in tasks[0], "第一个任务ID应为1")
    tester.assert_true("任务A" in tasks[0], "第一个任务描述正确")
    tester.assert_true(STATUS_PENDING in tasks[0], f"任务状态应为{STATUS_PENDING}")


def test_complete_task(tester: TaskTester):
    """测试3: 完成任务"""
    print("\n测试3: 完成任务")
    storage = MockTaskStorage()
    manager = TaskManager(storage=storage)

    manager.add("待完成任务")
    result = manager.done(1)
    tester.assert_equal(result, MSG_TASK_MARKED_DONE.format(task_id=1), "任务应标记为完成")

    tasks = manager.list()
    tester.assert_true(STATUS_DONE in tasks[0], f"任务状态应为{STATUS_DONE}")


def test_delete_task(tester: TaskTester):
    """测试4: 删除任务"""
    print("\n测试4: 删除任务")
    storage = MockTaskStorage()
    manager = TaskManager(storage=storage)

    manager.add("任务1")
    manager.add("任务2")
    manager.add("任务3")

    result = manager.delete(2)
    tester.assert_equal(result, MSG_TASK_DELETED.format(task_id=2), "应成功删除任务2")
    tester.assert_equal(len(manager.tasks), 2, "剩余任务应为2个")


def test_clear_completed(tester: TaskTester):
    """测试5: 清除已完成任务"""
    print("\n测试5: 清除已完成任务")
    storage = MockTaskStorage()
    manager = TaskManager(storage=storage)

    manager.add("任务1")
    manager.add("任务2")
    manager.add("任务3")
    manager.done(1)
    manager.done(3)

    result = manager.clear()
    tester.assert_equal(result, MSG_CLEARED_ALL, "应清除已完成任务")
    tester.assert_equal(len(manager.tasks), 1, "应剩余1个未完成任务")


def test_error_handling(tester: TaskTester):
    """测试6: 错误处理"""
    print("\n测试6: 错误处理")
    storage = MockTaskStorage()
    manager = TaskManager(storage=storage)

    # 测试删除不存在的任务
    result = manager.delete(999)
    tester.assert_equal(result, MSG_TASK_NOT_FOUND.format(task_id=999), "应报告任务未找到")

    # 测试完成不存在的任务
    result = manager.done(999)
    tester.assert_equal(result, MSG_TASK_NOT_FOUND.format(task_id=999), "应报告任务未找到")

    # 测试添加空描述
    result = manager.add("")
    tester.assert_equal(result, MSG_EMPTY_DESCRIPTION, "应报告描述为空")

    # 测试空列表
    empty_storage = MockTaskStorage()
    empty_manager = TaskManager(storage=empty_storage)
    tasks = empty_manager.list()
    tester.assert_equal(tasks[0], MSG_NO_TASKS, "空任务列表应提示无任务")


def test_persistence(tester: TaskTester):
    """测试7: 数据持久化"""
    print("\n测试7: 数据持久化")
    storage = MockTaskStorage()
    manager1 = TaskManager(storage=storage)

    manager1.add("持久化测试")
    manager1.done(1)

    # 创建新的管理器实例（使用同一存储）
    manager2 = TaskManager(storage=storage)
    tester.assert_equal(len(manager2.tasks), 1, "应加载持久化的数据")
    tester.assert_equal(manager2.tasks[0].status, STATUS_DONE, f"应加载任务状态为{STATUS_DONE}")


def test_json_validation(tester: TaskTester):
    """测试8: JSON验证"""
    print("\n测试8: 数据验证")

    # 测试1: 有效任务
    valid_data = [
        {"id": 1, "description": "有效任务", "status": "pending"},
        {"id": 2, "description": "另一个有效任务", "status": "pending"}
    ]
    storage = MockTaskStorage(valid_data)
    manager = TaskManager(storage=storage)
    tester.assert_equal(len(manager.tasks), 2, "应加载所有有效任务")

    # 测试2: 无效ID类型
    invalid_id_data = [
        {"id": "invalid", "description": "无效ID", "status": "pending"}
    ]
    storage = MockTaskStorage(invalid_id_data)
    manager = TaskManager(storage=storage)
    tester.assert_equal(len(manager.tasks), 0, "应跳过ID类型无效的任务")

    # 测试3: 缺少必需字段
    missing_field_data = [
        {"id": 1, "description": "缺少状态"}
    ]
    storage = MockTaskStorage(missing_field_data)
    manager = TaskManager(storage=storage)
    tester.assert_equal(len(manager.tasks), 0, "应跳过缺少字段的任务")


def test_task_object(tester: TaskTester):
    """测试9: 任务对象"""
    print("\n测试9: 任务对象")
    task = Task(1, "测试任务")

    tester.assert_equal(task.id, 1, "任务ID应为1")
    tester.assert_equal(task.description, "测试任务", "任务描述应正确")
    tester.assert_equal(task.status, STATUS_PENDING, f"初始状态应为{STATUS_PENDING}")
    tester.assert_true(task.completedAt is None, "完成时间应为None")

    # 测试转换为字典
    task_dict = task.to_dict()
    tester.assert_equal(task_dict["id"], 1, "字典ID应正确")
    tester.assert_equal(task_dict["description"], "测试任务", "字典描述应正确")

    # 测试从字典创建
    task2 = Task.from_dict(task_dict)
    tester.assert_equal(task2.id, 1, "从字典创建的任务ID应正确")
    tester.assert_equal(task2.description, "测试任务", "从字典创建的描述应正确")


def test_storage_operations(tester: TaskTester):
    """测试10: 存储操作"""
    print("\n测试10: 存储操作")
    storage = MockTaskStorage()

    # 测试初始状态
    tester.assert_equal(len(storage.load()), 0, "初始存储应为空")
    tester.assert_true(storage.exists(), "Mock存储应始终存在")

    # 测试保存
    test_data = [{"id": 1, "description": "测试", "status": "pending"}]
    storage.save(test_data)

    # 测试加载
    loaded_data = storage.load()
    tester.assert_equal(len(loaded_data), 1, "应加载保存的数据")
    tester.assert_equal(loaded_data[0]["description"], "测试", "数据内容应正确")


def test_mark_already_done(tester: TaskTester):
    """测试11: 标记已完成的任务"""
    print("\n测试11: 标记已完成的任务")
    storage = MockTaskStorage()
    manager = TaskManager(storage=storage)

    manager.add("测试任务")
    manager.done(1)

    # 再次标记已完成的任务
    result = manager.done(1)
    expected_msg = "Task 1 is already done"
    tester.assert_equal(result, expected_msg, "应提示任务已完成")


def test_id_auto_increment(tester: TaskTester):
    """测试12: ID自增"""
    print("\n测试12: ID自增")
    storage = MockTaskStorage()
    manager = TaskManager(storage=storage)

    manager.add("任务1")
    manager.add("任务2")
    manager.add("任务3")

    tester.assert_equal(manager.tasks[0].id, 1, "第一个任务ID应为1")
    tester.assert_equal(manager.tasks[1].id, 2, "第二个任务ID应为2")
    tester.assert_equal(manager.tasks[2].id, 3, "第三个任务ID应为3")


# ==================== 运行测试 ====================

def run_all_tests():
    """运行所有测试"""
    print("="*50)
    print("开始运行测试套件（重构版）")
    print("="*50)

    tester = TaskTester()

    try:
        test_add_tasks(tester)
        test_list_tasks(tester)
        test_complete_task(tester)
        test_delete_task(tester)
        test_clear_completed(tester)
        test_error_handling(tester)
        test_persistence(tester)
        test_json_validation(tester)
        test_task_object(tester)
        test_storage_operations(tester)
        test_mark_already_done(tester)
        test_id_auto_increment(tester)

    finally:
        pass  # Mock存储自动清理

    return tester.print_summary()


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
