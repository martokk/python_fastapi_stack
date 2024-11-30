from typing import Any

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select

from app.models.people import Staff
from app.utils.templates import templates
from app.views.deps import get_db
from app.views.pages.admin.deps import get_admin_context

router = APIRouter()


@router.get("/staff", response_class=HTMLResponse)
async def admin_staff(
    request: Request,
    context: dict[str, Any] = Depends(get_admin_context),
    session: Session = Depends(get_db),
) -> HTMLResponse:
    """Admin staff page"""
    if not context["user_permissions"].staff:
        return templates.TemplateResponse("admin/403.html", context, status_code=403)

    staff = session.exec(select(Staff)).all()
    context["staff"] = staff
    return templates.TemplateResponse("admin/staff.html", context)
