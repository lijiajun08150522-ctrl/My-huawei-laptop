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
