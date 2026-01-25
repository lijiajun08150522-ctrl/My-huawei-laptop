"""
智能分析与报表模块
"""

import os
from typing import List, Dict, Optional
from datetime import datetime
from constants import (
    STATUS_PENDING, STATUS_DONE,
    FIELD_ID, FIELD_DESCRIPTION, FIELD_STATUS,
    FIELD_CREATED_AT, FIELD_COMPLETED_AT
)


# ==================== 统计计算器 ====================

class TaskStatistics:
    """任务统计计算器 - 纯计算逻辑"""

    def __init__(self, tasks):
        """
        初始化统计计算器

        Args:
            tasks: 任务列表
        """
        self.tasks = tasks

    def calculate_total(self) -> int:
        """计算总任务数"""
        return len(self.tasks)

    def calculate_completed(self) -> int:
        """计算已完成任务数"""
        return len([t for t in self.tasks if t.status == STATUS_DONE])

    def calculate_pending(self) -> int:
        """计算待办任务数"""
        return len([t for t in self.tasks if t.status == STATUS_PENDING])

    def get_completion_rate(self) -> float:
        """
        计算完成率

        Returns:
            完成率（百分比，0-100）
        """
        total = self.calculate_total()
        if total == 0:
            return 0.0
        completed = self.calculate_completed()
        return (completed / total) * 100

    def get_stats_by_category(self) -> Dict[str, int]:
        """
        按分类统计任务数量

        Returns:
            分类统计字典 {分类名: 任务数}
        """
        stats = {}
        for task in self.tasks:
            category = getattr(task, 'category', 'General')
            stats[category] = stats.get(category, 0) + 1
        return stats

    def get_priority_distribution(self) -> Dict[str, int]:
        """
        获取优先级分布

        Returns:
            优先级统计字典 {优先级: 任务数}
        """
        stats = {}
        for task in self.tasks:
            priority = getattr(task, 'priority', 'Medium')
            stats[priority] = stats.get(priority, 0) + 1
        return stats


# ==================== 智能分析器 ====================

class TaskAnalyzer:
    """智能分析器 - 基于统计的业务逻辑"""

    def __init__(self, statistics: TaskStatistics):
        """
        初始化分析器

        Args:
            statistics: 统计计算器实例
        """
        self.statistics = statistics

    def check_task_overload(self, threshold: int = 5) -> bool:
        """
        检查任务积压是否超限

        Args:
            threshold: 待办任务阈值，默认5

        Returns:
            True表示积压超限，False表示正常
        """
        pending_count = self.statistics.calculate_pending()
        return pending_count > threshold

    def get_overload_warning(self, threshold: int = 5) -> Optional[str]:
        """
        获取积压警告信息

        Args:
            threshold: 待办任务阈值，默认5

        Returns:
            警告信息字符串，如果没有积压则返回None
        """
        if self.check_task_overload(threshold):
            return "注意：任务积压过多，请优先处理！"
        return None

    def get_priority_distribution(self) -> Dict[str, int]:
        """获取优先级分布统计"""
        return self.statistics.get_priority_distribution()

    def get_completion_rate(self) -> float:
        """获取完成率"""
        return self.statistics.get_completion_rate()


# ==================== 报表生成器 ====================

class ReportGenerator:
    """报表生成器 - 生成格式化的报表"""

    def __init__(self, tasks, analyzer: TaskAnalyzer):
        """
        初始化报表生成器

        Args:
            tasks: 任务列表
            analyzer: 分析器实例
        """
        self.tasks = tasks
        self.analyzer = analyzer

    def format_task(self, task) -> str:
        """
        格式化单个任务

        Args:
            task: 任务对象

        Returns:
            格式化的任务字符串
        """
        status_str = "done" if task.status == STATUS_DONE else "pending"
        priority = getattr(task, 'priority', 'Medium')
        category = getattr(task, 'category', 'General')
        return f"[{task.id}] {task.description} ({priority}, {category}, {status_str})"

    def format_statistics(self) -> str:
        """
        格式化统计信息

        Returns:
            格式化的统计信息字符串
        """
        total = self.analyzer.statistics.calculate_total()
        completed = self.analyzer.statistics.calculate_completed()
        pending = self.analyzer.statistics.calculate_pending()
        rate = self.analyzer.statistics.get_completion_rate()

        lines = [
            f"总任务数: {total}",
            f"已完成: {completed}",
            f"待办: {pending}",
            f"完成率: {rate:.2f}%"
        ]
        return "\n".join(lines)

    def format_category_stats(self) -> str:
        """
        格式化分类统计

        Returns:
            格式化的分类统计字符串
        """
        category_stats = self.analyzer.statistics.get_stats_by_category()

        lines = ["分类统计:"]
        for category, count in sorted(category_stats.items()):
            lines.append(f"- {category}: {count}")

        return "\n".join(lines)

    def format_priority_stats(self) -> str:
        """
        格式化优先级统计

        Returns:
            格式化的优先级统计字符串
        """
        priority_stats = self.analyzer.statistics.get_priority_distribution()

        lines = ["优先级分布:"]
        for priority, count in sorted(priority_stats.items()):
            lines.append(f"- {priority}: {count}")

        return "\n".join(lines)

    def format_task_list(self) -> str:
        """
        格式化任务列表

        Returns:
            格式化的任务列表字符串
        """
        if not self.tasks:
            return "无任务"

        lines = ["任务列表:"]
        for task in self.tasks:
            lines.append(self.format_task(task))

        return "\n".join(lines)

    def generate_summary(self) -> str:
        """
        生成今日简报

        Returns:
            格式化的今日简报字符串
        """
        separator = "=" * 50

        lines = [
            separator,
            "今日简报",
            separator,
            self.format_statistics(),
            "",
            self.format_category_stats(),
            separator
        ]

        return "\n".join(lines)

    def generate_full_report(self) -> str:
        """
        生成完整报表

        Returns:
            格式化的完整报表字符串
        """
        separator = "=" * 50

        lines = [
            separator,
            "任务管理器 - 任务报表",
            separator,
            f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            separator,
            "统计信息",
            separator,
            self.format_statistics(),
            "",
            separator,
            "分类统计",
            separator,
            self.format_category_stats(),
            "",
            separator,
            self.format_task_list(),
            "",
            separator,
            self.format_priority_stats(),
            separator
        ]

        return "\n".join(lines)

    def export_to_txt(self, filepath: str = "summary.txt") -> str:
        """
        导出报表为文本文件

        Args:
            filepath: 导出文件路径（支持相对路径和绝对路径）

        Returns:
            导出成功消息
        """
        content = self.generate_full_report()

        # 转换为绝对路径
        if not os.path.isabs(filepath):
            # 使用当前工作目录
            filepath = os.path.abspath(filepath)

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"报表已导出: {filepath}"
        except Exception as e:
            return f"导出失败: {e}"


# ==================== 分析服务 ====================

class TaskAnalyzerService:
    """任务分析服务 - 整合所有分析功能的统一入口"""

    def __init__(self, task_manager):
        """
        初始化分析服务

        Args:
            task_manager: 任务管理器实例
        """
        self.task_manager = task_manager
        self._init_components()

    def _init_components(self):
        """初始化所有组件"""
        self.statistics = TaskStatistics(self.task_manager.tasks)
        self.analyzer = TaskAnalyzer(self.statistics)
        self.report_generator = ReportGenerator(
            self.task_manager.tasks,
            self.analyzer
        )

    def _refresh_components(self):
        """刷新组件（当任务列表更新时调用）"""
        self._init_components()

    def get_today_report(self) -> str:
        """
        获取今日简报

        Returns:
            今日简报字符串
        """
        self._refresh_components()
        return self.report_generator.generate_summary()

    def export_summary(self, filepath: str = "summary.txt") -> str:
        """
        导出报表

        Args:
            filepath: 导出文件路径

        Returns:
            导出结果消息
        """
        self._refresh_components()
        return self.report_generator.export_to_txt(filepath)

    def get_statistics(self) -> Dict:
        """
        获取完整统计数据

        Returns:
            包含所有统计信息的字典
        """
        self._refresh_components()
        return {
            'total': self.statistics.calculate_total(),
            'completed': self.statistics.calculate_completed(),
            'pending': self.statistics.calculate_pending(),
            'completion_rate': self.statistics.get_completion_rate(),
            'by_category': self.statistics.get_stats_by_category(),
            'by_priority': self.statistics.get_priority_distribution()
        }

    def check_overload_warning(self, threshold: int = 5) -> Optional[str]:
        """
        检查并返回积压警告

        Args:
            threshold: 待办任务阈值

        Returns:
            警告信息，如果没有积压则返回None
        """
        self._refresh_components()
        return self.analyzer.get_overload_warning(threshold)
