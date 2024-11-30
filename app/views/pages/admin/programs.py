from typing import Any

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select

from app.models.programs import Program
from app.utils.templates import templates
from app.views.deps import get_db
from app.views.pages.admin.deps import get_admin_context

router = APIRouter()


@router.get("/programs", response_class=HTMLResponse)
async def admin_programs(
    request: Request,
    context: dict[str, Any] = Depends(get_admin_context),
    session: Session = Depends(get_db),
) -> HTMLResponse:
    """Admin programs page"""
    if not context["user_permissions"].faq:
        return templates.TemplateResponse("admin/403.html", context, status_code=403)

    programs = session.exec(select(Program)).all()
    context["programs"] = programs
    return templates.TemplateResponse("admin/programs.html", context)
