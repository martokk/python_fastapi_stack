from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models.admin import UserPermissions
from app.utils.auth import get_current_user

router = APIRouter(tags=["auth"])


@router.get("/user/permissions")
async def get_user_permissions(
    current_user=Depends(get_current_user), session: Session = Depends(get_session)
):
    """Get permissions for the current user - used by frontend to build navbar"""
    stmt = select(UserPermissions).where(UserPermissions.user_id == current_user.id)
    permissions = session.exec(stmt).first()

    if not permissions:
        return {
            "webpage_variables": False,
            "wish_list": False,
            "staff": False,
            "board_members": False,
            "stats": False,
            "timeline": False,
            "partners": False,
            "users": False,
            "faq": False,
        }

    return {
        "webpage_variables": permissions.webpage_variables,
        "wish_list": permissions.wish_list,
        "staff": permissions.staff,
        "board_members": permissions.board_members,
        "stats": permissions.stats,
        "timeline": permissions.timeline,
        "partners": permissions.partners,
        "users": permissions.users,
        "faq": permissions.faq,
    }
