"""
任务管理CLI工具 - 数据验证器
"""

from typing import Dict, List
from constants import (
    FIELD_ID, FIELD_DESCRIPTION, FIELD_STATUS,
    VALID_STATUSES, ERR_MISSING_FIELD, ERR_INVALID_ID_TYPE,
    ERR_INVALID_DESC_TYPE, ERR_INVALID_STATUS
)


class TaskValidator:
    """任务数据验证器"""

    @staticmethod
    def validate_task_dict(data: Dict) -> bool:
        """验证任务字典结构是否完整"""
        required_fields = [FIELD_ID, FIELD_DESCRIPTION, FIELD_STATUS]
        return all(field in data for field in required_fields)

    @staticmethod
    def validate_id(task_id: int) -> bool:
        """验证任务ID是否有效"""
        return isinstance(task_id, int) and task_id > 0

    @staticmethod
    def validate_description(description: str) -> bool:
        """验证任务描述是否有效"""
        return isinstance(description, str) and len(description.strip()) > 0

    @staticmethod
    def validate_status(status: str) -> bool:
        """验证任务状态是否有效"""
        return status in VALID_STATUSES

    @staticmethod
    def validate_task_fields(data: Dict):
        """验证任务字段并抛出异常"""
        # 验证必需字段
        required_fields = [FIELD_ID, FIELD_DESCRIPTION, FIELD_STATUS]
        for field in required_fields:
            if field not in data:
                raise ValueError(ERR_MISSING_FIELD.format(field=field))

        # 验证ID类型
        if not isinstance(data[FIELD_ID], int):
            raise ValueError(ERR_INVALID_ID_TYPE)

        # 验证描述类型
        if not isinstance(data[FIELD_DESCRIPTION], str):
            raise ValueError(ERR_INVALID_DESC_TYPE)

        # 验证状态值
        if data[FIELD_STATUS] not in VALID_STATUSES:
            raise ValueError(ERR_INVALID_STATUS)

    @staticmethod
    def validate_create_params(task_id: int, description: str):
        """验证创建任务参数"""
        if not TaskValidator.validate_id(task_id):
            raise ValueError(ERR_INVALID_ID_TYPE)

        if not TaskValidator.validate_description(description):
            raise ValueError(ERR_INVALID_DESC_TYPE)
