from typing import Any

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from app.utils.templates import templates
from app.views.deps import get_current_user_or_raise
from app.views.pages.admin import (
    backup,
    board,
    faq,
    partners,
    programs,
    staff,
    stats,
    timeline,
    users,
    variables,
    wishlist,
)
from app.views.pages.admin.deps import get_admin_context

router = APIRouter(
    dependencies=[Depends(get_current_user_or_raise)],
)

# Include all admin sub-routers
router.include_router(variables.router, tags=["admin"])
router.include_router(wishlist.router, tags=["admin"])
router.include_router(stats.router, tags=["admin"])
router.include_router(timeline.router, tags=["admin"])
router.include_router(programs.router, tags=["admin"])
router.include_router(faq.router, tags=["admin"])
router.include_router(staff.router, tags=["admin"])
router.include_router(board.router, tags=["admin"])
router.include_router(partners.router, tags=["admin"])
router.include_router(users.router, tags=["admin"])
router.include_router(backup.router, tags=["admin"])


@router.get("/", response_class=HTMLResponse)
async def admin_home(
    request: Request,
    context: dict[str, Any] = Depends(get_admin_context),
) -> HTMLResponse:
    """Admin index page"""
    if not any(
        [
            context["user_permissions"].variables,
            context["user_permissions"].wishlist,
            context["user_permissions"].staff,
            context["user_permissions"].board_member,
            context["user_permissions"].stats,
            context["user_permissions"].timeline,
            context["user_permissions"].partners,
            context["user_permissions"].user,
            context["user_permissions"].faq,
            context["user_permissions"].programs,
            context["user_permissions"].backup,
        ]
    ):
        return templates.TemplateResponse("admin/403.html", context, status_code=403)

    return templates.TemplateResponse("admin/home.html", context)
