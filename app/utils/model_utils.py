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
