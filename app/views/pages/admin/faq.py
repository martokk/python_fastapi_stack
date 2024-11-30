from typing import Any, Optional

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select

from app.models.programs import FAQ, Program
from app.utils.templates import templates
from app.views.deps import get_db
from app.views.pages.admin.deps import get_admin_context

router = APIRouter()


@router.get("/faq", response_class=HTMLResponse)
async def admin_faq(
    request: Request,
    program_id: Optional[int] = None,
    context: dict[str, Any] = Depends(get_admin_context),
    session: Session = Depends(get_db),
) -> HTMLResponse:
    """Admin FAQ page"""
    if not context["user_permissions"].faq:
        return templates.TemplateResponse("admin/403.html", context, status_code=403)

    # Get all programs for the dropdown
    programs = session.exec(select(Program)).all()
    context["programs"] = programs

    # Get FAQs, filtered by program if specified
    query = select(FAQ).order_by(FAQ.order)
    if program_id:
        query = query.where(FAQ.program_id == program_id)
    faqs = session.exec(query).all()

    context["faqs"] = faqs
    context["selected_program"] = program_id
    return templates.TemplateResponse("admin/faq.html", context)
