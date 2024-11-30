from typing import Any

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from sqlmodel import Session, select

from app import crud, models
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
    """Admin board members page"""
    if not context["user_permissions"].board_members:
        return templates.TemplateResponse("admin/403.html", context, status_code=403)

    board_members = session.exec(select(models.BoardMember)).all()
    context["board_members"] = board_members
    return templates.TemplateResponse("admin/board.html", context)


@router.post("/board-members")
async def create_board_member(
    board_member: models.BoardMemberCreate,
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Create new board member"""
    if not context["user_permissions"].board_members:
        return JSONResponse({"error": "Unauthorized"}, status_code=403)

    created_member = await crud.board_member.create(db=db, obj_in=board_member)
    return JSONResponse({"id": created_member.id})


@router.get("/board-members/{board_member_id}")
async def get_board_member(
    board_member_id: int,
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Get board member by ID"""
    if not context["user_permissions"].board_members:
        return JSONResponse({"error": "Unauthorized"}, status_code=403)

    board_member = await crud.board_member.get(db=db, id=board_member_id)
    if not board_member:
        return JSONResponse({"error": "Board member not found"}, status_code=404)

    return JSONResponse(
        {
            "id": board_member.id,
            "name": board_member.name,
            "position": board_member.position,
            "description": board_member.description,
        }
    )


@router.put("/board-members/{board_member_id}")
async def update_board_member(
    board_member_id: int,
    board_member_update: models.BoardMemberUpdate,
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Update board member"""
    if not context["user_permissions"].board_members:
        return JSONResponse({"error": "Unauthorized"}, status_code=403)

    board_member = await crud.board_member.get(db=db, id=board_member_id)
    if not board_member:
        return JSONResponse({"error": "Board member not found"}, status_code=404)

    board_member = await crud.board_member.update(
        db=db, db_obj=board_member, obj_in=board_member_update
    )
    return JSONResponse({"id": board_member.id})


@router.delete("/board-members/{board_member_id}")
async def delete_board_member(
    board_member_id: int,
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Delete board member"""
    if not context["user_permissions"].board_members:
        return JSONResponse({"error": "Unauthorized"}, status_code=403)

    board_member = await crud.board_member.get(db=db, id=board_member_id)
    if not board_member:
        return JSONResponse({"error": "Board member not found"}, status_code=404)

    await crud.board_member.remove(db=db, id=board_member_id)
    return JSONResponse({"status": "success"})
