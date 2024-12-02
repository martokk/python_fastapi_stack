from typing import Any

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from sqlmodel import Session

from app import crud
from app.utils.model_utils import get_backup_fields
from app.utils.templates import templates
from app.views.deps import get_db
from app.views.pages.admin.deps import get_admin_context

router = APIRouter()


@router.get("/backup", response_class=HTMLResponse)
async def admin_backup(
    request: Request,
    context: dict[str, Any] = Depends(get_admin_context),
) -> HTMLResponse:
    """Admin backup page"""
    if not context["user_permissions"].backup:
        return templates.TemplateResponse("admin/403.html", context, status_code=403)

    context["backup_fields"] = get_backup_fields()
    return templates.TemplateResponse("admin/backup.html", context)


@router.get("/backup/download")
async def download_backup(
    request: Request,
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Download database backup"""
    if not context["user_permissions"].backup:
        return JSONResponse({"error": "Unauthorized"}, status_code=403)

    try:
        # Map field names to their crud methods
        crud_map = {
            "variables": crud.variables.get_all,
            "wishlist": crud.wishlist.get_all,
            "staff": crud.staff.get_all,
            "board": crud.board_member.get_all,
            "stats": crud.stats.get_all,
            "timeline": crud.timeline.get_all,
            "partners": crud.partners.get_all,
            "programs": crud.programs.get_all,
            "faq": crud.faq.get_all_ordered,
            "user": crud.user.get_all,
        }

        # Collect all data
        backup_data = {}
        for field in get_backup_fields():
            if field in crud_map:
                backup_data[field] = await crud_map[field](db=db)

        return JSONResponse(backup_data)
    except Exception as e:
        return JSONResponse({"error": f"Failed to generate backup: {str(e)}"}, status_code=500)
