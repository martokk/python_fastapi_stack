from typing import Any

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select

from app.models.timeline import Timeline
from app.utils.templates import templates
from app.views.deps import get_db
from app.views.pages.admin.deps import get_admin_context

router = APIRouter()


@router.get("/timeline", response_class=HTMLResponse)
async def admin_timeline(
    request: Request,
    context: dict[str, Any] = Depends(get_admin_context),
    session: Session = Depends(get_db),
) -> HTMLResponse:
    """Admin timeline page"""
    if not context["user_permissions"].timeline:
        return templates.TemplateResponse("admin/403.html", context, status_code=403)

    timeline = session.exec(select(Timeline).order_by(Timeline.date)).all()
    context["timeline"] = timeline
    return templates.TemplateResponse("admin/timeline.html", context)
