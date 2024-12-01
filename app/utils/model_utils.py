from typing import List

from app import models


def get_permission_fields() -> List[str]:
    """
    Get a list of permission field names from the UserPermissions model,
    excluding 'id' and 'user_id'.

    Returns:
        List[str]: List of permission field names
    """
    return [
        field
        for field in models.UserPermissions.model_fields.keys()
        if field not in ("id", "user_id")
    ]


def get_backup_fields() -> List[str]:
    """
    Get a list of all database models that can be backed up.

    Returns:
        List[str]: List of model names that can be backed up
    """
    backup_fields = get_permission_fields()
    backup_fields.remove("backup")
    return backup_fields
