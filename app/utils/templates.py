from typing import Any

from fastapi import Depends, Request
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from app.models.user import User
from app.models.user_permissions import UserPermissions
from app.models.variables import Variables
from app.views.deps import get_current_user, get_db

templates = Jinja2Templates(directory="app/views/templates")


async def get_template_context(
    request: Request,
    session: Session,
    current_user: User | None = None,
) -> dict[str, Any]:
    """Get common template context data"""
    # Get variables
    variables = session.exec(select(Variables)).first()
    if not variables:
        variables = Variables()
        session.add(variables)
        session.commit()

    context = {"request": request, "variables": variables}

    if not current_user:
        return context

    # Get user permissions
    permissions = session.exec(
        select(UserPermissions).where(UserPermissions.user_id == current_user.id)
    ).first()

    if not permissions:
        permissions = UserPermissions(user_id=current_user.id)

    context.update({"user": current_user, "user_permissions": permissions})
    return context
