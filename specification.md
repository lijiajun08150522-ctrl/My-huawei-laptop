# 项目规约：任务管理CLI工具 (Task Manager CLI)

## 1. 项目概述
开发一个基于命令行的任务管理工具，支持任务的增删改查和状态管理。

## 2. 功能需求

### 2.1 核心功能
- **添加任务**：`add <任务描述>` - 添加新任务
- **列出任务**：`list` - 显示所有任务
- **完成任务**：`done <任务ID>` - 标记任务为完成
- **删除任务**：`delete <任务ID>` - 删除指定任务
- **清除完成**：`clear` - 清除所有已完成的任务

### 2.2 任务属性
- ID: 唯一标识符（自增整数）
- 描述: 任务文本内容
- 状态: pending | done
- 创建时间: ISO 8601格式时间戳
- 完成时间: ISO 8601格式时间戳（完成时设置）

## 3. 数据存储
- 文件名: `tasks.json`
- 存储位置: 用户主目录 `.tasks.json`
- 格式: JSON数组

```json
[
  {
    "id": 1,
    "description": "示例任务",
    "status": "pending",
    "createdAt": "2026-01-23T10:00:00Z",
    "completedAt": null
  }
]
```

## 4. 输入输出规约

### 4.1 命令格式
```
task-cli <command> [arguments]
```

### 4.2 命令定义
- `add <description>` - 成功返回 "Added: <description>"
- `list` - 列出所有任务，格式: "[<id>] <description> (<status>)"
- `done <id>` - 成功返回 "Task <id> marked as done"
- `delete <id>` - 成功返回 "Task <id> deleted"
- `clear` - 成功返回 "Cleared all completed tasks"

### 4.3 错误处理
- 无效命令: "Error: Unknown command. Use 'help' for usage."
- 无效ID: "Error: Task <id> not found"
- 文件读写错误: "Error: Unable to read/write task file"

## 5. 约束条件
- 语言: Python 3.8+
- 无外部依赖（仅使用标准库）
- 文件不存在时自动创建
- ID自增，从1开始

## 6. 测试用例
1. 添加3个任务，列出所有任务
2. 完成第2个任务，再次列出
3. 删除第1个任务，列出剩余
4. 清除已完成的任务
5. 添加空描述应报错
