# 重构计划：任务管理CLI工具

## 📊 数据结构变化分析

### 对比：规约 vs 当前实现

| 规约要求 | 当前实现 | 状态 |
|---------|---------|------|
| 字段名: `createdAt` | 字段名: `createdAt` | ✅ 一致 |
| 字段名: `completedAt` | 字段名: `completedAt` | ✅ 一致 |
| ISO 8601格式 | ISO 8601格式 + "Z" | ✅ 符合 |
| 状态值: `pending` \| `done` | 状态值: `pending` \| `done` | ✅ 一致 |
| 基本命令 | 基本命令 | ✅ 一致 |
| 错误消息 | 错误消息 | ✅ 一致 |

### 结论

**当前实现已完全符合规约要求**，无需结构性重构。

但发现以下可优化点：

1. **代码质量优化** - 提取常量、改进命名
2. **可维护性提升** - 分离关注点、减少重复
3. **扩展性增强** - 为未来功能预留空间

---

## 🎯 重构计划（优化型重构）

### 阶段1：常量提取

#### 1.1 新增常量定义

**目标**：将魔法字符串和数字提取为命名常量

**新增模块**：`constants.py`
```python
# 任务状态常量
STATUS_PENDING = "pending"
STATUS_DONE = "done"
VALID_STATUSES = [STATUS_PENDING, STATUS_DONE]

# 任务字段常量
FIELD_ID = "id"
FIELD_DESCRIPTION = "description"
FIELD_STATUS = "status"
FIELD_CREATED_AT = "createdAt"
FIELD_COMPLETED_AT = "completedAt"

# 时间戳格式
TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

# 消息模板
MSG_ADDED = "Added: {description}"
MSG_TASK_NOT_FOUND = "Error: Task {task_id} not found"
MSG_TASK_ALREADY_DONE = "Task {task_id} is already done"
MSG_TASK_MARKED_DONE = "Task {task_id} marked as done"
MSG_TASK_DELETED = "Task {task_id} deleted"
MSG_CLEARED_ALL = "Cleared all completed tasks"
MSG_EMPTY_DESCRIPTION = "Error: Task description cannot be empty"
MSG_NO_TASKS = "No tasks found"

# 文件相关
DEFAULT_FILENAME = ".tasks.json"
BACKUP_SUFFIX = ".backup"
```

**修改函数**：
- `task.py` 中所有硬编码字符串和数字
- `test_task.py` 中的测试断言

---

### 阶段2：数据验证器分离

#### 2.1 新增验证器类

**目标**：将验证逻辑从数据类中分离

**新增类**：`TaskValidator`
```python
class TaskValidator:
    """任务数据验证器"""

    @staticmethod
    def validate_task_dict(data: Dict) -> bool:
        """验证任务字典结构"""
        required_fields = [FIELD_ID, FIELD_DESCRIPTION, FIELD_STATUS]
        return all(field in data for field in required_fields)

    @staticmethod
    def validate_id(task_id: int) -> bool:
        """验证任务ID"""
        return isinstance(task_id, int) and task_id > 0

    @staticmethod
    def validate_description(description: str) -> bool:
        """验证任务描述"""
        return isinstance(description, str) and len(description.strip()) > 0

    @staticmethod
    def validate_status(status: str) -> bool:
        """验证任务状态"""
        return status in VALID_STATUSES
```

**修改函数**：
- `Task.from_dict()` - 使用验证器
- `TaskManager.add()` - 使用验证器
- `main()` - 使用验证器

---

### 阶段3：命令处理器模式

#### 3.1 新增命令处理器基类

**目标**：使用命令模式重构命令处理逻辑

**新增类**：`CommandHandler`
```python
from abc import ABC, abstractmethod

class CommandHandler(ABC):
    """命令处理器基类"""

    def __init__(self, manager: TaskManager):
        self.manager = manager

    @abstractmethod
    def execute(self, args: List[str]) -> str:
        """执行命令"""
        pass

    @abstractmethod
    def get_help(self) -> str:
        """获取帮助信息"""
        pass
```

#### 3.2 实现具体命令处理器

**新增类**：
```python
class AddCommandHandler(CommandHandler):
    def execute(self, args: List[str]) -> str:
        description = " ".join(args)
        return self.manager.add(description)

    def get_help(self) -> str:
        return "add <description> - Add a new task"

class ListCommandHandler(CommandHandler):
    def execute(self, args: List[str]) -> str:
        return "\n".join(self.manager.list())

    def get_help(self) -> str:
        return "list - List all tasks"

class DoneCommandHandler(CommandHandler):
    def execute(self, args: List[str]) -> str:
        task_id = int(args[0])
        return self.manager.done(task_id)

    def get_help(self) -> str:
        return "done <id> - Mark task as completed"

class DeleteCommandHandler(CommandHandler):
    def execute(self, args: List[str]) -> str:
        task_id = int(args[0])
        return self.manager.delete(task_id)

    def get_help(self) -> str:
        return "delete <id> - Delete a task"

class ClearCommandHandler(CommandHandler):
    def execute(self, args: List[str]) -> str:
        return self.manager.clear()

    def get_help(self) -> str:
        return "clear - Clear all completed tasks"
```

#### 3.3 新增命令注册器

**新增类**：`CommandRegistry`
```python
class CommandRegistry:
    """命令注册器"""

    def __init__(self, manager: TaskManager):
        self.manager = manager
        self.handlers = {}
        self._register_default_handlers()

    def _register_default_handlers(self):
        """注册默认命令处理器"""
        self.register("add", AddCommandHandler(self.manager))
        self.register("list", ListCommandHandler(self.manager))
        self.register("done", DoneCommandHandler(self.manager))
        self.register("delete", DeleteCommandHandler(self.manager))
        self.register("clear", ClearCommandHandler(self.manager))

    def register(self, name: str, handler: CommandHandler):
        """注册命令处理器"""
        self.handlers[name.lower()] = handler

    def execute(self, command: str, args: List[str]) -> str:
        """执行命令"""
        handler = self.handlers.get(command.lower())
        if handler:
            return handler.execute(args)
        raise ValueError(f"Unknown command: {command}")

    def get_help(self) -> str:
        """获取帮助信息"""
        lines = ["Usage: task-cli <command> [arguments]", "", "Commands:"]
        for name, handler in self.handlers.items():
            lines.append(f"  {handler.get_help()}")
        lines.append("  help - Show this help message")
        return "\n".join(lines)
```

**修改函数**：
- `main()` - 使用命令注册器
- 移除 `TaskManager.help()` - 由命令注册器提供

---

### 阶段4：文件操作抽象

#### 4.1 新增文件存储接口

**目标**：抽象文件操作，便于测试和扩展

**新增接口**：`TaskStorage`
```python
from abc import ABC, abstractmethod

class TaskStorage(ABC):
    """任务存储接口"""

    @abstractmethod
    def load(self) -> List[Dict]:
        """加载任务"""
        pass

    @abstractmethod
    def save(self, tasks: List[Dict]) -> None:
        """保存任务"""
        pass

    @abstractmethod
    def exists(self) -> bool:
        """检查文件是否存在"""
        pass
```

#### 4.2 实现JSON文件存储

**新增类**：`JSONTaskStorage`
```python
class JSONTaskStorage(TaskStorage):
    """JSON文件存储实现"""

    def __init__(self, filepath: str):
        self.filepath = filepath

    def load(self) -> List[Dict]:
        """从JSON文件加载任务"""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if not isinstance(data, list):
                raise ValueError("Invalid task file format. Expected array.")

            return data

        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}")

    def save(self, tasks: List[Dict]) -> None:
        """保存任务到JSON文件"""
        self._create_backup()

        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, indent=2, ensure_ascii=False)

    def exists(self) -> bool:
        """检查文件是否存在"""
        return os.path.exists(self.filepath)

    def _create_backup(self):
        """创建备份文件"""
        if self.exists():
            backup_path = self.filepath + BACKUP_SUFFIX
            with open(self.filepath, 'r', encoding='utf-8') as src:
                with open(backup_path, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())

    def create_if_not_exists(self):
        """文件不存在时创建"""
        if not self.exists():
            file_dir = os.path.dirname(self.filepath)
            if file_dir:
                os.makedirs(file_dir, exist_ok=True)
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump([], f)
```

**修改函数**：
- `TaskManager.__init__()` - 使用存储接口
- `TaskManager.load_tasks()` - 委托给存储对象
- `TaskManager.save_tasks()` - 委托给存储对象
- 移除 `TaskManager._ensure_file_exists()` - 由存储对象处理

---

### 阶段5：测试重构

#### 5.1 新增Mock存储

**新增类**：`MockTaskStorage`
```python
class MockTaskStorage(TaskStorage):
    """Mock存储用于测试"""

    def __init__(self, data: List[Dict] = None):
        self.data = data if data is not None else []

    def load(self) -> List[Dict]:
        return self.data.copy()

    def save(self, tasks: List[Dict]) -> None:
        self.data = tasks.copy()

    def exists(self) -> bool:
        return True
```

#### 5.2 更新测试用例

**修改函数**：
- 所有测试用例 - 使用Mock存储
- 新增存储接口测试
- 新增命令处理器测试

---

## 📋 重构清单

### 新增文件

| 文件名 | 类型 | 优先级 |
|--------|------|--------|
| `constants.py` | 常量定义 | 高 |
| `validators.py` | 验证器类 | 中 |
| `storage.py` | 存储接口和实现 | 中 |
| `commands.py` | 命令处理器 | 低 |

### 修改文件

| 文件名 | 修改类型 | 优先级 |
|--------|----------|--------|
| `task.py` | 重构 | 高 |
| `test_task.py` | 更新 | 中 |

---

## 🔧 重构步骤

### 第1步：常量提取（高优先级）
1. 创建 `constants.py`
2. 更新 `task.py` 使用常量
3. 更新 `test_task.py` 使用常量
4. 运行测试验证

### 第2步：文件操作抽象（中优先级）
1. 创建 `storage.py`
2. 更新 `TaskManager` 使用存储接口
3. 更新测试使用Mock存储
4. 运行测试验证

### 第3步：验证器分离（中优先级）
1. 创建 `validators.py`
2. 更新 `Task` 和 `TaskManager` 使用验证器
3. 运行测试验证

### 第4步：命令处理器模式（低优先级）
1. 创建 `commands.py`
2. 更新 `main()` 使用命令注册器
3. 运行测试验证

---

## ✅ 重构收益

### 代码质量
- ✅ 消除魔法字符串和数字
- ✅ 提高代码可读性
- ✅ 减少重复代码

### 可维护性
- ✅ 职责分离清晰
- ✅ 便于单元测试
- ✅ 降低耦合度

### 扩展性
- ✅ 易于添加新命令
- ✅ 易于更换存储方式
- ✅ 易于添加新功能

---

## ⚠️ 风险评估

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 功能回归 | 中 | 运行完整测试套件 |
| 性能下降 | 低 | 重构后进行性能测试 |
| 测试失败 | 中 | 逐步重构，每步验证 |

---

## 📅 实施建议

### 推荐实施顺序

1. **先实施阶段1**（常量提取）- 影响最小，收益最大
2. **再实施阶段2**（文件操作抽象）- 提高可测试性
3. **可选实施阶段3**（验证器分离）- 改进代码结构
4. **最后实施阶段4**（命令处理器）- 最大重构，可选

### 验证方式

每个阶段完成后：
1. 运行 `python test_task.py` 确保所有测试通过
2. 运行 `python task.py <command>` 确保功能正常
3. 对比重构前后行为一致性

---

## 🎯 总结

### 当前状态
- ✅ 功能完全符合规约
- ✅ 所有测试通过（25/25）
- ✅ 代码结构良好

### 重构目标
- 🎯 提高代码质量
- 🎯 提升可维护性
- 🎯 增强扩展性
- 🎯 为未来功能做准备

### 建议
由于当前实现已完全符合规约且测试通过，建议：
1. **优先实施阶段1**（常量提取）- 立即可行
2. **根据需求实施其他阶段** - 按需重构
3. **保持测试覆盖** - 确保重构安全
