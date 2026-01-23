"""
任务管理CLI工具 - 实现文件
"""

import json
import os
import sys
from datetime import datetime
from typing import List, Dict, Optional


# ==================== 数据结构定义 ====================

class Task:
    """任务数据结构"""

    def __init__(self, id: int, description: str):
        self.id = id
        self.description = description
        self.status = "pending"
        self.createdAt = datetime.now().isoformat() + "Z"
        self.completedAt = None

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "createdAt": self.createdAt,
            "completedAt": self.completedAt
        }

    @staticmethod
    def from_dict(data: Dict) -> 'Task':
        """从字典创建任务"""
        task = Task(data["id"], data["description"])
        task.status = data["status"]
        task.createdAt = data["createdAt"]
        task.completedAt = data.get("completedAt")
        return task


class TaskManager:
    """任务管理器"""

    def __init__(self, filepath: str = None):
        self.filepath = filepath or os.path.expanduser("~/.tasks.json")
        self.tasks: List[Task] = []
        self.load_tasks()

    # ==================== 文件操作 ====================

    def load_tasks(self):
        """从文件加载任务"""
        try:
            if os.path.exists(self.filepath):
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = [Task.from_dict(item) for item in data]
        except Exception as e:
            print(f"Error: Unable to read task file: {e}")
            sys.exit(1)

    def save_tasks(self):
        """保存任务到文件"""
        try:
            data = [task.to_dict() for task in self.tasks]
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error: Unable to write task file: {e}")
            sys.exit(1)

    # ==================== 命令实现 ====================

    def add(self, description: str) -> str:
        """添加任务"""
        if not description.strip():
            return "Error: Task description cannot be empty"

        new_id = max([task.id for task in self.tasks], default=0) + 1
        task = Task(new_id, description.strip())
        self.tasks.append(task)
        self.save_tasks()
        return f"Added: {task.description}"

    def list(self) -> List[str]:
        """列出所有任务"""
        if not self.tasks:
            return ["No tasks found"]

        result = []
        for task in self.tasks:
            status = "done" if task.status == "done" else "pending"
            result.append(f"[{task.id}] {task.description} ({status})")
        return result

    def done(self, task_id: int) -> str:
        """标记任务完成"""
        task = self._find_task(task_id)
        if not task:
            return f"Error: Task {task_id} not found"

        if task.status == "done":
            return f"Task {task_id} is already done"

        task.status = "done"
        task.completedAt = datetime.now().isoformat() + "Z"
        self.save_tasks()
        return f"Task {task_id} marked as done"

    def delete(self, task_id: int) -> str:
        """删除任务"""
        task = self._find_task(task_id)
        if not task:
            return f"Error: Task {task_id} not found"

        self.tasks.remove(task)
        self.save_tasks()
        return f"Task {task_id} deleted"

    def clear(self) -> str:
        """清除已完成的任务"""
        completed_count = len([t for t in self.tasks if t.status == "done"])
        self.tasks = [t for t in self.tasks if t.status == "pending"]
        self.save_tasks()
        return f"Cleared {completed_count} completed tasks"

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
        print("Error: No command specified")
        print("Use 'help' for usage information")
        sys.exit(1)

    command = sys.argv[1].lower()
    manager = TaskManager()

    if command == "add":
        description = " ".join(sys.argv[2:])
        print(manager.add(description))
    elif command == "list":
        for line in manager.list():
            print(line)
    elif command == "done":
        try:
            task_id = int(sys.argv[2])
            print(manager.done(task_id))
        except (IndexError, ValueError):
            print("Error: Invalid task ID")
    elif command == "delete":
        try:
            task_id = int(sys.argv[2])
            print(manager.delete(task_id))
        except (IndexError, ValueError):
            print("Error: Invalid task ID")
    elif command == "clear":
        print(manager.clear())
    elif command == "help":
        print(manager.help())
    else:
        print(f"Error: Unknown command '{command}'. Use 'help' for usage.")


if __name__ == "__main__":
    main()
