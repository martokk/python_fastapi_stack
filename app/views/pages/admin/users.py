from typing import Any

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select

from app.models.user import User
from app.utils.templates import templates
from app.views.deps import get_db
from app.views.pages.admin.deps import get_admin_context

router = APIRouter()


@router.get("/users", response_class=HTMLResponse)
async def admin_users(
    request: Request,
    context: dict[str, Any] = Depends(get_admin_context),
    session: Session = Depends(get_db),
) -> HTMLResponse:
    """Admin users page"""
    if not context["user_permissions"].users:
        return templates.TemplateResponse("admin/403.html", context, status_code=403)

    users = session.exec(select(User)).all()
    context["users"] = users
    return templates.TemplateResponse("admin/users.html", context)
