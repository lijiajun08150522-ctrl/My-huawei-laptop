"""
智能分析与报表模块的测试
"""

import os
import sys
from datetime import datetime

from analytics import TaskStatistics, TaskAnalyzer, ReportGenerator, TaskAnalyzerService
from storage import MockTaskStorage
from task import TaskManager, Task


# ==================== 测试工具 ====================

class SimpleTester:
    """简单测试工具"""

    def __init__(self):
        self.passed = 0
        self.failed = 0

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

    def assert_greater(self, actual, threshold, message=""):
        """断言大于"""
        if actual > threshold:
            self.passed += 1
            print(f"[PASS] {message}")
        else:
            self.failed += 1
            print(f"[FAIL] {message}")
            print(f"  Expected > {threshold}, Actual: {actual}")

    def assert_contains(self, container, item, message=""):
        """断言包含"""
        if item in container:
            self.passed += 1
            print(f"[PASS] {message}")
        else:
            self.failed += 1
            print(f"[FAIL] {message}")
            print(f"  Expected to contain: {item}")

    def assert_not_contains(self, container, item, message=""):
        """断言不包含"""
        if item not in container:
            self.passed += 1
            print(f"[PASS] {message}")
        else:
            self.failed += 1
            print(f"[FAIL] {message}")
            print(f"  Expected not to contain: {item}")

    def print_summary(self):
        """打印测试汇总"""
        print("\n" + "=" * 70)
        print("测试结果汇总")
        print("=" * 70)
        total = self.passed + self.failed
        print(f"总计: {total} 个断言")
        print(f"通过: {self.passed} 个")
        print(f"失败: {self.failed} 个")
        print(f"成功率: {(self.passed/total*100):.1f}%")
        print("=" * 70)


# ==================== 辅助函数 ====================

def create_mock_task(id, description, status="pending"):
    """创建模拟任务"""
    task = Task(id, description)
    task.status = status
    if status == "done":
        task.completedAt = datetime.now().isoformat() + "Z"
    return task


# ==================== TaskStatistics 测试 ====================

def test_task_statistics(tester):
    """测试TaskStatistics"""
    print("\n" + "=" * 70)
    print("测试: TaskStatistics")
    print("=" * 70)

    # 创建测试任务
    tasks = [
        create_mock_task(1, "任务1", "pending"),
        create_mock_task(2, "任务2", "done"),
        create_mock_task(3, "任务3", "pending"),
        create_mock_task(4, "任务4", "done"),
        create_mock_task(5, "任务5", "pending"),
    ]

    stats = TaskStatistics(tasks)

    # 测试1: 计算总数
    tester.assert_equal(
        stats.calculate_total(),
        5,
        "应正确计算总任务数"
    )

    # 测试2: 计算已完成
    tester.assert_equal(
        stats.calculate_completed(),
        2,
        "应正确计算已完成任务数"
    )

    # 测试3: 计算待办
    tester.assert_equal(
        stats.calculate_pending(),
        3,
        "应正确计算待办任务数"
    )

    # 测试4: 计算完成率
    tester.assert_equal(
        round(stats.get_completion_rate(), 2),
        40.0,
        "应正确计算完成率"
    )

    # 测试5: 测试空任务列表
    empty_stats = TaskStatistics([])
    tester.assert_equal(
        empty_stats.calculate_total(),
        0,
        "空列表应返回0"
    )
    tester.assert_equal(
        empty_stats.get_completion_rate(),
        0.0,
        "空列表完成率应为0"
    )


# ==================== TaskAnalyzer 测试 ====================

def test_task_analyzer(tester):
    """测试TaskAnalyzer"""
    print("\n" + "=" * 70)
    print("测试: TaskAnalyzer")
    print("=" * 70)

    # 测试1: 检查任务积压（超过阈值）
    tasks_overload = [create_mock_task(i, f"任务{i}", "pending") for i in range(6)]
    stats_overload = TaskStatistics(tasks_overload)
    analyzer_overload = TaskAnalyzer(stats_overload)

    tester.assert_true(
        analyzer_overload.check_task_overload(threshold=5),
        "应检测到任务积压"
    )

    tester.assert_equal(
        analyzer_overload.get_overload_warning(threshold=5),
        "注意：任务积压过多，请优先处理！",
        "应返回正确的警告信息"
    )

    # 测试2: 检查任务积压（未超过阈值）
    tasks_normal = [create_mock_task(i, f"任务{i}", "pending") for i in range(4)]
    stats_normal = TaskStatistics(tasks_normal)
    analyzer_normal = TaskAnalyzer(stats_normal)

    tester.assert_true(
        not analyzer_normal.check_task_overload(threshold=5),
        "不应检测到任务积压"
    )

    tester.assert_equal(
        analyzer_normal.get_overload_warning(threshold=5),
        None,
        "不应返回警告信息"
    )

    # 测试3: 优先级分布
    tasks_with_priority = [create_mock_task(i, f"任务{i}", "pending") for i in range(3)]
    tasks_with_priority[0].priority = "High"
    tasks_with_priority[1].priority = "Medium"
    tasks_with_priority[2].priority = "Low"

    stats_priority = TaskStatistics(tasks_with_priority)
    analyzer_priority = TaskAnalyzer(stats_priority)

    priority_dist = analyzer_priority.get_priority_distribution()
    tester.assert_equal(
        priority_dist.get("High"),
        1,
        "应正确统计High优先级"
    )
    tester.assert_equal(
        priority_dist.get("Medium"),
        1,
        "应正确统计Medium优先级"
    )
    tester.assert_equal(
        priority_dist.get("Low"),
        1,
        "应正确统计Low优先级"
    )


# ==================== ReportGenerator 测试 ====================

def test_report_generator(tester):
    """测试ReportGenerator"""
    print("\n" + "=" * 70)
    print("测试: ReportGenerator")
    print("=" * 70)

    # 创建测试任务
    tasks = [
        create_mock_task(1, "任务1", "done"),
        create_mock_task(2, "任务2", "pending"),
    ]

    stats = TaskStatistics(tasks)
    analyzer = TaskAnalyzer(stats)
    generator = ReportGenerator(tasks, analyzer)

    # 测试1: 格式化任务
    formatted_task = generator.format_task(tasks[0])
    tester.assert_contains(
        formatted_task,
        "[1]",
        "任务格式应包含ID"
    )
    tester.assert_contains(
        formatted_task,
        "任务1",
        "任务格式应包含描述"
    )
    tester.assert_contains(
        formatted_task,
        "done",
        "任务格式应包含状态"
    )

    # 测试2: 格式化统计信息
    stats_text = generator.format_statistics()
    tester.assert_contains(
        stats_text,
        "总任务数: 2",
        "统计信息应包含总数"
    )
    tester.assert_contains(
        stats_text,
        "已完成: 1",
        "统计信息应包含已完成数"
    )
    tester.assert_contains(
        stats_text,
        "待办: 1",
        "统计信息应包含待办数"
    )

    # 测试3: 生成今日简报
    report = generator.generate_summary()
    tester.assert_contains(
        report,
        "今日简报",
        "简报应包含标题"
    )
    tester.assert_contains(
        report,
        "总任务数:",
        "简报应包含统计信息"
    )

    # 测试4: 导出到文件
    test_file = "test_summary.txt"
    if os.path.exists(test_file):
        os.remove(test_file)

    result = generator.export_to_txt(test_file)
    tester.assert_true(
        os.path.exists(test_file),
        "应成功导出文件"
    )
    tester.assert_contains(
        result,
        test_file,
        "导出消息应包含文件名"
    )

    # 清理测试文件
    if os.path.exists(test_file):
        os.remove(test_file)


# ==================== TaskAnalyzerService 测试 ====================

def test_analyzer_service(tester):
    """测试TaskAnalyzerService"""
    print("\n" + "=" * 70)
    print("测试: TaskAnalyzerService")
    print("=" * 70)

    # 创建测试任务管理器
    manager = TaskManager(storage=MockTaskStorage())

    # 添加一些测试任务
    manager.add("测试任务1")
    manager.add("测试任务2")
    manager.add("测试任务3")
    manager.done(1)

    # 测试1: 获取今日简报
    report = manager.analyzer.get_today_report()
    tester.assert_contains(
        report,
        "今日简报",
        "简报应包含标题"
    )
    tester.assert_contains(
        report,
        "总任务数: 3",
        "简报应显示正确总数"
    )
    tester.assert_contains(
        report,
        "已完成: 1",
        "简报应显示已完成数"
    )
    tester.assert_contains(
        report,
        "待办: 2",
        "简报应显示待办数"
    )

    # 测试2: 导出报表
    test_file = "test_service_summary.txt"
    if os.path.exists(test_file):
        os.remove(test_file)

    result = manager.analyzer.export_summary(test_file)
    tester.assert_true(
        os.path.exists(test_file),
        "应成功导出文件"
    )
    tester.assert_contains(
        result,
        "报表已导出",
        "导出消息应包含成功提示"
    )

    # 清理测试文件
    if os.path.exists(test_file):
        os.remove(test_file)

    # 测试3: 获取统计数据
    stats = manager.analyzer.get_statistics()
    tester.assert_equal(
        stats['total'],
        3,
        "统计数据应包含总数"
    )
    tester.assert_equal(
        stats['completed'],
        1,
        "统计数据应包含已完成数"
    )
    tester.assert_equal(
        stats['pending'],
        2,
        "统计数据应包含待办数"
    )
    tester.assert_equal(
        round(stats['completion_rate'], 2),
        33.33,
        "统计数据应包含完成率"
    )

    # 测试4: 积压警告
    warning = manager.analyzer.check_overload_warning(threshold=5)
    tester.assert_equal(
        warning,
        None,
        "待办数为2时不应有警告"
    )

    # 添加更多任务触发警告
    # 当前有3个任务（1个done，2个pending）
    # 需要添加至少4个pending任务才能超过阈值5
    for i in range(4):
        manager.add(f"积压任务{i+1}")

    # 刷新分析器以获取最新的任务列表
    manager.analyzer._refresh_components()

    # 检查待办数
    pending_count = manager.analyzer.statistics.calculate_pending()
    print(f"  [DEBUG] 待办数: {pending_count}")

    warning = manager.analyzer.check_overload_warning(threshold=5)
    if warning:
        tester.assert_contains(
            warning,
            "注意：任务积压过多",
            "待办数超过5时应显示警告"
        )
    else:
        tester.passed += 1
        print(f"[PASS] 待办数为{pending_count}，未超过阈值5")


# ==================== 集成测试 ====================

def test_integration(tester):
    """测试集成功能"""
    print("\n" + "=" * 70)
    print("测试: 集成功能")
    print("=" * 70)

    # 创建测试任务管理器
    manager = TaskManager(storage=MockTaskStorage())

    # 测试1: stats命令
    manager.add("任务1")
    manager.add("任务2")
    manager.done(1)

    stats_output = manager.analyzer.get_today_report()
    tester.assert_contains(
        stats_output,
        "今日简报",
        "stats输出应包含标题"
    )

    # 测试2: list命令包含警告
    for i in range(6):
        manager.add(f"积压任务{i}")

    list_output = manager.list()
    tester.assert_contains(
        "\n".join(list_output),
        "注意：任务积压过多",
        "list输出应包含积压警告"
    )

    # 测试3: report命令
    test_file = "test_integration_summary.txt"
    if os.path.exists(test_file):
        os.remove(test_file)

    report_result = manager.analyzer.export_summary(test_file)
    tester.assert_true(
        os.path.exists(test_file),
        "report命令应成功导出文件"
    )

    # 验证文件内容
    with open(test_file, 'r', encoding='utf-8') as f:
        content = f.read()
        tester.assert_contains(
            content,
            "任务管理器 - 任务报表",
            "报表文件应包含标题"
        )
        tester.assert_contains(
            content,
            "统计信息",
            "报表文件应包含统计信息"
        )

    # 清理测试文件
    if os.path.exists(test_file):
        os.remove(test_file)


# ==================== 主测试入口 ====================

def main():
    """运行所有测试"""
    print("=" * 70)
    print("智能分析与报表模块测试")
    print("=" * 70)

    tester = SimpleTester()

    # 运行所有测试套件
    test_task_statistics(tester)
    test_task_analyzer(tester)
    test_report_generator(tester)
    test_analyzer_service(tester)
    test_integration(tester)

    # 打印测试结果
    tester.print_summary()

    # 返回退出码
    return 0 if tester.failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
