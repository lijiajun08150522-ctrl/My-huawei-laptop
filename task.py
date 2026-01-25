"""
任务管理CLI工具 - 实现文件（重构版）
"""

import sys
from datetime import datetime
from typing import List, Optional

from constants import (
    STATUS_PENDING, STATUS_DONE,
    FIELD_ID, FIELD_DESCRIPTION, FIELD_STATUS,
    FIELD_CREATED_AT, FIELD_COMPLETED_AT,
    MSG_ADDED, MSG_TASK_NOT_FOUND, MSG_TASK_ALREADY_DONE,
    MSG_TASK_MARKED_DONE, MSG_TASK_DELETED, MSG_CLEARED_ALL,
    MSG_EMPTY_DESCRIPTION, MSG_NO_TASKS,
    MSG_NO_COMMAND, MSG_HELP_HINT, MSG_UNKNOWN_COMMAND,
    MSG_TASK_ID_REQUIRED, MSG_TASK_ID_USAGE, MSG_TASK_ID_INVALID,
    MSG_DESC_REQUIRED, MSG_DESC_USAGE,
    ERR_INVALID_JSON, ERR_INVALID_FORMAT, ERR_SKIP_INVALID_TASK,
    ERR_PERMISSION_DENIED, ERR_WRITE_FILE, ERR_READ_FILE
)
from validators import TaskValidator
from storage import JSONTaskStorage


class Task:
    """任务数据结构"""

    def __init__(self, id: int, description: str):
        self.id = id
        self.description = description
        self.status = STATUS_PENDING
        self.createdAt = datetime.now().isoformat() + "Z"
        self.completedAt = None

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            FIELD_ID: self.id,
            FIELD_DESCRIPTION: self.description,
            FIELD_STATUS: self.status,
            FIELD_CREATED_AT: self.createdAt,
            FIELD_COMPLETED_AT: self.completedAt
        }

    @staticmethod
    def from_dict(data: dict) -> 'Task':
        """从字典创建任务（带验证）"""
        # 验证字段
        TaskValidator.validate_task_fields(data)

        # 创建任务对象
        task = Task(data[FIELD_ID], data[FIELD_DESCRIPTION])
        task.status = data[FIELD_STATUS]
        task.createdAt = data.get(FIELD_CREATED_AT)
        task.completedAt = data.get(FIELD_COMPLETED_AT)

        return task


class TaskManager:
    """任务管理器"""

    def __init__(self, filepath: str = None, storage=None):
        if storage:
            self.storage = storage
        else:
            self.storage = JSONTaskStorage(filepath)

        self.tasks: List[Task] = []
        self._load_tasks()

    # ==================== 文件操作 ====================

    def _load_tasks(self):
        """从存储加载任务"""
        self.storage.create_if_not_exists()

        try:
            data = self.storage.load()

            # 验证并加载每个任务
            self.tasks = []
            for item in data:
                if TaskValidator.validate_task_dict(item):
                    try:
                        self.tasks.append(Task.from_dict(item))
                    except ValueError as e:
                        # 跳过无效任务，继续加载其他任务
                        print(ERR_SKIP_INVALID_TASK.format(error=e))

        except ValueError as e:
            # 格式错误，重置为空数组
            print(str(e))
            self.tasks = []
        except Exception as e:
            # 其他错误
            print(ERR_READ_FILE.format(error=e))
            sys.exit(1)

    def _save_tasks(self):
        """保存任务到存储"""
        try:
            data = [task.to_dict() for task in self.tasks]
            self.storage.save(data)

        except PermissionError:
            print(ERR_PERMISSION_DENIED)
            sys.exit(1)
        except OSError as e:
            print(ERR_WRITE_FILE.format(error=e))
            sys.exit(1)
        except Exception as e:
            print(ERR_WRITE_FILE.format(error=e))
            sys.exit(1)

    # ==================== 命令实现 ====================

    def add(self, description: str) -> str:
        """添加任务"""
        if not description.strip():
            return MSG_EMPTY_DESCRIPTION

        new_id = max([task.id for task in self.tasks], default=0) + 1
        task = Task(new_id, description.strip())
        self.tasks.append(task)
        self._save_tasks()

        return MSG_ADDED.format(description=task.description)

    def list(self) -> List[str]:
        """列出所有任务"""
        if not self.tasks:
            return [MSG_NO_TASKS]

        result = []
        for task in self.tasks:
            status = STATUS_DONE if task.status == STATUS_DONE else STATUS_PENDING
            result.append(f"[{task.id}] {task.description} ({status})")
        return result

    def done(self, task_id: int) -> str:
        """标记任务完成"""
        task = self._find_task(task_id)
        if not task:
            return MSG_TASK_NOT_FOUND.format(task_id=task_id)

        if task.status == STATUS_DONE:
            return MSG_TASK_ALREADY_DONE.format(task_id=task_id)

        task.status = STATUS_DONE
        task.completedAt = datetime.now().isoformat() + "Z"
        self._save_tasks()

        return MSG_TASK_MARKED_DONE.format(task_id=task_id)

    def delete(self, task_id: int) -> str:
        """删除任务"""
        task = self._find_task(task_id)
        if not task:
            return MSG_TASK_NOT_FOUND.format(task_id=task_id)

        self.tasks.remove(task)
        self._save_tasks()

        return MSG_TASK_DELETED.format(task_id=task_id)

    def clear(self) -> str:
        """清除已完成的任务"""
        self.tasks = [t for t in self.tasks if t.status == STATUS_PENDING]
        self._save_tasks()

        return MSG_CLEARED_ALL

    # ==================== 辅助方法 ====================

    def _find_task(self, task_id: int) -> Optional[Task]:
        """查找任务"""
        return next((t for t in self.tasks if t.id == task_id), None)

    def help(self) -> str:
        """显示帮助信息"""
        return """Usage: task-cli <command> [arguments]

Commands:
  add <description>    Add a new task
  list                 List all tasks
  done <id>            Mark task as completed
  delete <id>          Delete a task
  clear                Clear all completed tasks
  help                 Show this help message"""


# ==================== 主程序入口 ====================

def main():
    """主入口函数"""
    if len(sys.argv) < 2:
        print(MSG_NO_COMMAND)
        print(MSG_HELP_HINT)
        sys.exit(1)

    command = sys.argv[1].lower()
    manager = TaskManager()

    if command == "add":
        if len(sys.argv) < 3:
            print(MSG_DESC_REQUIRED)
            print(MSG_DESC_USAGE)
            sys.exit(1)

        description = " ".join(sys.argv[2:])
        print(manager.add(description))

    elif command == "list":
        for line in manager.list():
            print(line)

    elif command == "done":
        if len(sys.argv) < 3:
            print(MSG_TASK_ID_REQUIRED)
            print(MSG_TASK_ID_USAGE)
            sys.exit(1)

        try:
            task_id = int(sys.argv[2])
            print(manager.done(task_id))
        except ValueError:
            print(MSG_TASK_ID_INVALID)
            sys.exit(1)

    elif command == "delete":
        if len(sys.argv) < 3:
            print(MSG_TASK_ID_REQUIRED)
            print(MSG_TASK_ID_USAGE)
            sys.exit(1)

        try:
            task_id = int(sys.argv[2])
            print(manager.delete(task_id))
        except ValueError:
            print(MSG_TASK_ID_INVALID)
            sys.exit(1)

    elif command == "clear":
        print(manager.clear())

    elif command == "help" or command == "--help" or command == "-h":
        print(manager.help())

    else:
        print(MSG_UNKNOWN_COMMAND.format(command=command))


if __name__ == "__main__":
    main()
