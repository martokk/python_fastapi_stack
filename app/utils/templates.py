from typing import Any, Optional

import os

from fastapi import Depends, Request
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from app.models.admin import UserPermissions
from app.models.user import User
from app.views.deps import get_current_user, get_db

templates = Jinja2Templates(directory=os.path.join("app", "views", "templates"))


async def get_template_context(
    request: Request,
    current_user: User | None = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> dict[str, Any]:
    """Get common template context data"""
    if not current_user:
        return {"request": request}

    # Get user permissions
    permissions = session.exec(
        select(UserPermissions).where(UserPermissions.user_id == current_user.id)
    ).first()

    if not permissions:
        permissions = UserPermissions(user_id=current_user.id)

    return {"request": request, "user": current_user, "user_permissions": permissions}
