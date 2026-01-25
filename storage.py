"""
任务管理CLI工具 - 存储接口和实现
"""

import json
import os
from abc import ABC, abstractmethod
from typing import List, Dict
from constants import DEFAULT_FILENAME, BACKUP_SUFFIX


class TaskStorage(ABC):
    """任务存储接口"""

    @abstractmethod
    def load(self) -> List[Dict]:
        """加载任务数据"""
        pass

    @abstractmethod
    def save(self, tasks: List[Dict]) -> None:
        """保存任务数据"""
        pass

    @abstractmethod
    def exists(self) -> bool:
        """检查文件是否存在"""
        pass

    @abstractmethod
    def create_if_not_exists(self) -> None:
        """文件不存在时创建"""
        pass


class JSONTaskStorage(TaskStorage):
    """JSON文件存储实现"""

    def __init__(self, filepath: str = None):
        self.filepath = filepath or os.path.expanduser("~/" + DEFAULT_FILENAME)

    def load(self) -> List[Dict]:
        """从JSON文件加载任务"""
        if not self.exists():
            return []

        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 验证JSON格式（必须是数组）
            if not isinstance(data, list):
                raise ValueError("Invalid task file format. Expected array.")

            return data

        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}")

    def save(self, tasks: List[Dict]) -> None:
        """保存任务到JSON文件"""
        # 创建备份
        self._create_backup()

        # 保存数据
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, indent=2, ensure_ascii=False)

    def exists(self) -> bool:
        """检查文件是否存在"""
        return os.path.exists(self.filepath)

    def create_if_not_exists(self) -> None:
        """文件不存在时创建空数组"""
        if self.exists():
            return

        # 获取文件目录
        file_dir = os.path.dirname(self.filepath)
        if file_dir and not os.path.exists(file_dir):
            os.makedirs(file_dir, exist_ok=True)

        # 创建空JSON数组
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump([], f, indent=2, ensure_ascii=False)

    def _create_backup(self):
        """创建备份文件"""
        if not self.exists():
            return

        backup_path = self.filepath + BACKUP_SUFFIX
        try:
            with open(self.filepath, 'r', encoding='utf-8') as src:
                with open(backup_path, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
        except Exception:
            # 备份失败不影响主流程
            pass


class MockTaskStorage(TaskStorage):
    """Mock存储用于测试"""

    def __init__(self, data: List[Dict] = None):
        self.data = data if data is not None else []

    def load(self) -> List[Dict]:
        """从内存加载任务"""
        return self.data.copy()

    def save(self, tasks: List[Dict]) -> None:
        """保存任务到内存"""
        self.data = tasks.copy()

    def exists(self) -> bool:
        """Mock总是返回True"""
        return True

    def create_if_not_exists(self) -> None:
        """Mock无需创建"""
        pass
