from typing import Any

from fastapi import Depends, Request
from sqlmodel import Session, select

from app.models.user import User
from app.models.user_permissions import UserPermissions
from app.utils.templates import get_template_context
from app.views.deps import get_current_user_or_raise, get_db


async def get_admin_context(
    request: Request,
    current_user: User = Depends(get_current_user_or_raise),
    session: Session = Depends(get_db),
) -> dict[str, Any]:
    """Get admin template context with user permissions"""
    context = await get_template_context(
        request=request, current_user=current_user, session=session
    )

    # Get user permissions
    permissions = session.exec(
        select(UserPermissions).where(UserPermissions.user_id == current_user.id)
    ).first()

    if not permissions:
        permissions = UserPermissions(user_id=current_user.id)
        session.add(permissions)
        session.commit()

    context["user_permissions"] = permissions
    return context
