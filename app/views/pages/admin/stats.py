from typing import Any

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select

from app.models.stats import Stats
from app.utils.templates import templates
from app.views.deps import get_db
from app.views.pages.admin.deps import get_admin_context

router = APIRouter()


@router.get("/stats", response_class=HTMLResponse)
async def admin_stats(
    request: Request,
    context: dict[str, Any] = Depends(get_admin_context),
    session: Session = Depends(get_db),
) -> HTMLResponse:
    """Admin stats page"""
    if not context["user_permissions"].stats:
        return templates.TemplateResponse("admin/403.html", context, status_code=403)

    stats = session.exec(select(Stats)).first()
    if not stats:
        stats = Stats()
        session.add(stats)
        session.commit()

    context["stats"] = stats
    return templates.TemplateResponse("admin/stats.html", context)
