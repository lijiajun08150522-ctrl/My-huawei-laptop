"""
任务管理CLI工具 - 常量定义
"""

# ==================== 任务状态常量 ====================

STATUS_PENDING = "pending"
STATUS_DONE = "done"
VALID_STATUSES = [STATUS_PENDING, STATUS_DONE]

# ==================== 任务字段常量 ====================

FIELD_ID = "id"
FIELD_DESCRIPTION = "description"
FIELD_STATUS = "status"
FIELD_CREATED_AT = "createdAt"
FIELD_COMPLETED_AT = "completedAt"

# ==================== 时间戳格式 ====================

TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

# ==================== 消息模板 ====================

MSG_ADDED = "Added: {description}"
MSG_TASK_NOT_FOUND = "Error: Task {task_id} not found"
MSG_TASK_ALREADY_DONE = "Task {task_id} is already done"
MSG_TASK_MARKED_DONE = "Task {task_id} marked as done"
MSG_TASK_DELETED = "Task {task_id} deleted"
MSG_CLEARED_ALL = "Cleared all completed tasks"
MSG_EMPTY_DESCRIPTION = "Error: Task description cannot be empty"
MSG_NO_TASKS = "No tasks found"
MSG_NO_COMMAND = "Error: No command specified"
MSG_HELP_HINT = "Use 'help' for usage information"
MSG_UNKNOWN_COMMAND = "Error: Unknown command '{command}'. Use 'help' for usage."

MSG_TASK_ID_REQUIRED = "Error: Task ID is required"
MSG_TASK_ID_USAGE = "Usage: task-cli done <id>"
MSG_TASK_ID_INVALID = "Error: Task ID must be a number"

MSG_DESC_REQUIRED = "Error: Task description is required"
MSG_DESC_USAGE = "Usage: task-cli add <description>"

# ==================== 文件相关常量 ====================

DEFAULT_FILENAME = ".tasks.json"
BACKUP_SUFFIX = ".backup"

# ==================== 错误消息 ====================

ERR_INVALID_JSON = "Invalid JSON format in task file: {error}"
ERR_INVALID_FORMAT = "Invalid task file format. Expected array."
ERR_MISSING_FIELD = "Missing required field: {field}"
ERR_INVALID_ID_TYPE = "Task ID must be an integer"
ERR_INVALID_DESC_TYPE = "Task description must be a string"
ERR_INVALID_STATUS = "Task status must be 'pending' or 'done'"
ERR_SKIP_INVALID_TASK = "Skipping invalid task: {error}"

ERR_PERMISSION_DENIED = "Error: Permission denied. Unable to write task file."
ERR_WRITE_FILE = "Error: Unable to write task file: {error}"
ERR_READ_FILE = "Error: Unable to read task file: {error}"

# ==================== 分析与报表常量 ====================

# 消息常量
MSG_TODAY_REPORT_HEADER = "今日简报"
MSG_STATS_TOTAL = "总任务数"
MSG_STATS_COMPLETED = "已完成"
MSG_STATS_PENDING = "待办"
MSG_STATS_COMPLETION_RATE = "完成率"
MSG_STATS_BY_CATEGORY = "分类统计"
MSG_STATS_PRIORITY = "优先级分布"

# 警告消息
MSG_TASK_OVERLOAD_WARNING = "注意：任务积压过多，请优先处理！"

# 导出相关
MSG_EXPORT_SUCCESS = "报表已导出: {filepath}"
MSG_EXPORT_FAILED = "导出失败: {error}"

# 配置常量
TASK_OVERLOAD_THRESHOLD = 5
DEFAULT_SUMMARY_FILE = "summary.txt"

# 任务分类和优先级（未来扩展）
DEFAULT_CATEGORY = "General"
CATEGORIES = ["Work", "Study", "Life", "General"]
PRIORITY_HIGH = "High"
PRIORITY_MEDIUM = "Medium"
PRIORITY_LOW = "Low"
PRIORITIES = [PRIORITY_HIGH, PRIORITY_MEDIUM, PRIORITY_LOW]
PRIORITY_WEIGHTS = {
    PRIORITY_HIGH: 3,
    PRIORITY_MEDIUM: 2,
    PRIORITY_LOW: 1
}
