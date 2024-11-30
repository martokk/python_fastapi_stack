from typing import Any

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select

from app.models.partners import Partner
from app.utils.templates import templates
from app.views.deps import get_db
from app.views.pages.admin.deps import get_admin_context

router = APIRouter()


@router.get("/partners", response_class=HTMLResponse)
async def admin_partners(
    request: Request,
    context: dict[str, Any] = Depends(get_admin_context),
    session: Session = Depends(get_db),
) -> HTMLResponse:
    """Admin partners page"""
    if not context["user_permissions"].partners:
        return templates.TemplateResponse("admin/403.html", context, status_code=403)

    partners = session.exec(select(Partner)).all()
    context["partners"] = partners
    return templates.TemplateResponse("admin/partners.html", context)
