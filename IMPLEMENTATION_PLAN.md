# 实现计划：根据规约优化任务管理CLI工具

## 📋 规约与当前实现的对比分析

### ✅ 已符合规约的功能
- [x] 任务属性结构（id, description, status, createdAt, completedAt）
- [x] JSON格式存储
- [x] 文件位置：用户主目录 `.tasks.json`
- [x] 核心命令：add, list, done, delete, clear
- [x] ISO 8601时间戳格式

### ⚠️ 需要优化的功能
- [ ] 错误消息与规约不完全一致
- [ ] JSON存储逻辑需要增强（文件不存在处理、格式验证）
- [ ] 命令参数验证需要完善

---

## 🎯 实现计划

### 阶段1：JSON存储逻辑优化

#### 1.1 修改 `TaskManager.__init__()` 方法

**当前问题**：
- 文件不存在时只处理加载，不创建
- 没有验证JSON格式

**修改方案**：
```python
def __init__(self, filepath: str = None):
    self.filepath = filepath or os.path.expanduser("~/.tasks.json")
    self.tasks: List[Task] = []
    self._ensure_file_exists()  # 确保文件存在
    self.load_tasks()
```

#### 1.2 新增 `TaskManager._ensure_file_exists()` 方法

**功能**：
- 检查文件是否存在
- 不存在时创建空JSON数组
- 初始化目录

**实现方案**：
```python
def _ensure_file_exists(self):
    """确保任务文件存在，不存在则创建"""
    # 获取文件目录
    file_dir = os.path.dirname(self.filepath)
    if file_dir and not os.path.exists(file_dir):
        os.makedirs(file_dir, exist_ok=True)

    # 文件不存在时创建空数组
    if not os.path.exists(self.filepath):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump([], f, indent=2, ensure_ascii=False)
```

#### 1.3 增强 `TaskManager.load_tasks()` 方法

**当前问题**：
- 异常处理不完善
- 没有验证JSON结构

**修改方案**：
```python
def load_tasks(self):
    """从文件加载任务"""
    try:
        with open(self.filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

            # 验证JSON格式（必须是数组）
            if not isinstance(data, list):
                print("Error: Invalid task file format. Expected array.")
                self.tasks = []
                return

            # 验证每个任务的结构
            self.tasks = []
            for item in data:
                if isinstance(item, dict) and all(key in item for key in ['id', 'description', 'status']):
                    self.tasks.append(Task.from_dict(item))

    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in task file: {e}")
        self.tasks = []
    except FileNotFoundError:
        # 文件不存在（由_ensure_file_exists处理）
        pass
    except Exception as e:
        print(f"Error: Unable to read task file: {e}")
        sys.exit(1)
```

#### 1.4 增强 `TaskManager.save_tasks()` 方法

**当前问题**：
- 异常信息不够具体
- 没有备份机制

**修改方案**：
```python
def save_tasks(self):
    """保存任务到文件"""
    try:
        data = [task.to_dict() for task in self.tasks]

        # 创建备份（可选）
        if os.path.exists(self.filepath):
            backup_path = self.filepath + '.backup'
            with open(self.filepath, 'r', encoding='utf-8') as src:
                with open(backup_path, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())

        # 保存数据
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    except PermissionError:
        print("Error: Permission denied. Unable to write task file.")
        sys.exit(1)
    except OSError as e:
        print(f"Error: Unable to write task file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Unable to write task file: {e}")
        sys.exit(1)
```

---

### 阶段2：错误消息统一

#### 2.1 修改 `TaskManager.add()` 方法

**当前问题**：
- 错误消息与规约不完全一致

**修改方案**：
```python
def add(self, description: str) -> str:
    """添加任务"""
    if not description.strip():
        return "Error: Task description cannot be empty"

    new_id = max([task.id for task in self.tasks], default=0) + 1
    task = Task(new_id, description.strip())
    self.tasks.append(task)
    self.save_tasks()
    return f"Added: {task.description}"
```

#### 2.2 修改 `TaskManager.done()` 方法

**当前问题**：
- 返回消息与规约一致
- 但错误消息需要统一

**修改方案**：
```python
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
```

#### 2.3 修改 `TaskManager.delete()` 方法

**修改方案**：
```python
def delete(self, task_id: int) -> str:
    """删除任务"""
    task = self._find_task(task_id)
    if not task:
        return f"Error: Task {task_id} not found"

    self.tasks.remove(task)
    self.save_tasks()
    return f"Task {task_id} deleted"
```

#### 2.4 修改 `TaskManager.clear()` 方法

**当前问题**：
- 返回消息是 "Cleared X completed tasks"
- 规约要求是 "Cleared all completed tasks"

**修改方案**：
```python
def clear(self) -> str:
    """清除已完成的任务"""
    completed_count = len([t for t in self.tasks if t.status == "done"])
    self.tasks = [t for t in self.tasks if t.status == "pending"]
    self.save_tasks()
    return "Cleared all completed tasks"
```

---

### 阶段3：命令参数验证增强

#### 3.1 修改 `main()` 函数中的参数处理

**当前问题**：
- done和delete命令缺少参数时错误信息不够明确

**修改方案**：
```python
if command == "done":
    if len(sys.argv) < 3:
        print("Error: Task ID is required")
        print("Usage: task-cli done <id>")
        sys.exit(1)
    try:
        task_id = int(sys.argv[2])
        print(manager.done(task_id))
    except ValueError:
        print("Error: Task ID must be a number")
        sys.exit(1)

if command == "delete":
    if len(sys.argv) < 3:
        print("Error: Task ID is required")
        print("Usage: task-cli delete <id>")
        sys.exit(1)
    try:
        task_id = int(sys.argv[2])
        print(manager.delete(task_id))
    except ValueError:
        print("Error: Task ID must be a number")
        sys.exit(1)
```

#### 3.2 新增命令帮助功能

**修改方案**：
```python
if command == "help" or command == "--help" or command == "-h":
    print(manager.help())
```

---

### 阶段4：数据结构验证增强

#### 4.1 修改 `Task.from_dict()` 方法

**当前问题**：
- 缺少字段验证
- 可能出现KeyError

**修改方案**：
```python
@staticmethod
def from_dict(data: Dict) -> 'Task':
    """从字典创建任务（带验证）"""
    # 验证必需字段
    required_fields = ['id', 'description', 'status']
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")

    # 验证字段类型
    if not isinstance(data['id'], int):
        raise ValueError("Task ID must be an integer")
    if not isinstance(data['description'], str):
        raise ValueError("Task description must be a string")
    if data['status'] not in ['pending', 'done']:
        raise ValueError("Task status must be 'pending' or 'done'")

    # 创建任务对象
    task = Task(data["id"], data["description"])
    task.status = data["status"]
    task.createdAt = data.get("createdAt")
    task.completedAt = data.get("completedAt")

    return task
```

---

### 阶段5：测试用例更新

#### 5.1 更新 `test_task.py` 中的clear测试

**当前测试**：
```python
result = manager.clear()
tester.assert_equal(result, "Cleared 2 completed tasks", "应清除2个已完成任务")
```

**修改为**：
```python
result = manager.clear()
tester.assert_equal(result, "Cleared all completed tasks", "应清除已完成任务")
```

---

## 📊 修改清单

### 需要修改的函数/方法

| 序号 | 函数/方法 | 文件 | 修改类型 | 优先级 |
|------|-----------|------|----------|--------|
| 1 | `TaskManager.__init__()` | task.py | 增强 | 高 |
| 2 | `TaskManager._ensure_file_exists()` | task.py | 新增 | 高 |
| 3 | `TaskManager.load_tasks()` | task.py | 增强 | 高 |
| 4 | `TaskManager.save_tasks()` | task.py | 增强 | 中 |
| 5 | `TaskManager.clear()` | task.py | 修改 | 中 |
| 6 | `Task.from_dict()` | task.py | 增强 | 中 |
| 7 | `main()` | task.py | 增强 | 低 |
| 8 | `test_clear_completed()` | test_task.py | 修改 | 低 |

---

## 🔧 JSON存储逻辑处理方案

### 存储结构

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

### 存储逻辑流程

```
初始化
  ↓
检查文件是否存在
  ↓ 否
创建空JSON数组 []
  ↓
加载文件内容
  ↓
验证JSON格式（必须是数组）
  ↓
验证每个任务结构
  ↓
加载到内存
  ↓
操作（add/list/done/delete/clear）
  ↓
保存到文件（自动格式化）
```

### 异常处理策略

1. **文件不存在** → 自动创建
2. **JSON格式错误** → 重置为空数组
3. **字段缺失** → 跳过无效任务
4. **权限错误** → 显示错误并退出
5. **编码错误** → 使用UTF-8编码

---

## ✅ 验证计划

### 功能验证

- [ ] 文件不存在时自动创建
- [ ] JSON格式正确读写
- [ ] 错误消息与规约一致
- [ ] 参数验证完善
- [ ] 所有测试用例通过

### 性能验证

- [ ] 大量任务加载速度
- [ ] 文件IO性能
- [ ] 内存占用

### 安全性验证

- [ ] 异常任务数据处理
- [ ] 并发访问安全
- [ ] 文件权限处理

---

## 📅 实施顺序

1. **优先级高**: 阶段1（JSON存储逻辑优化）
2. **优先级中**: 阶段2（错误消息统一） + 阶段3（参数验证）
3. **优先级低**: 阶段4（数据结构验证） + 阶段5（测试更新）

---

## 🎯 预期成果

- 100% 符合规约要求
- 更健壮的错误处理
- 更好的数据完整性
- 更友好的用户提示
- 所有测试通过
