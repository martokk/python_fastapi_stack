from typing import Any

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from app.utils.templates import templates
from app.views.pages.admin.deps import get_admin_context

router = APIRouter()


@router.get("/backup", response_class=HTMLResponse)
async def admin_backup(
    request: Request,
    context: dict[str, Any] = Depends(get_admin_context),
) -> HTMLResponse:
    """Admin backup page"""
    if not context["user_permissions"].users:  # Using users permission for backup
        return templates.TemplateResponse("admin/403.html", context, status_code=403)

    return templates.TemplateResponse("admin/backup.html", context)
