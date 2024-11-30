from typing import Any

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select

from app.models.people import BoardMember
from app.utils.templates import templates
from app.views.deps import get_db
from app.views.pages.admin.deps import get_admin_context

router = APIRouter()


@router.get("/board", response_class=HTMLResponse)
async def admin_board(
    request: Request,
    context: dict[str, Any] = Depends(get_admin_context),
    session: Session = Depends(get_db),
) -> HTMLResponse:
    """Admin board page"""
    if not context["user_permissions"].board_members:
        return templates.TemplateResponse("admin/403.html", context, status_code=403)

    board_members = session.exec(select(BoardMember)).all()
    context["board_members"] = board_members
    return templates.TemplateResponse("admin/board.html", context)
