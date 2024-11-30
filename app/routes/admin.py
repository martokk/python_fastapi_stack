from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models.variables import Variables
from app.utils.security import (
    require_board_members,
    require_faq,
    require_partners,
    require_staff,
    require_stats,
    require_timeline,
    require_users,
    require_webpage_variables,
    require_wish_list,
)

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/variables")
async def get_variables(
    current_user=Depends(require_webpage_variables), session: Session = Depends(get_session)
):
    variables = session.exec(select(Variables)).first()
    return variables


@router.get("/wishlist")
async def get_wishlist(
    current_user=Depends(require_wish_list), session: Session = Depends(get_session)
):
    # Your wishlist logic here
    pass


@router.get("/staff")
async def get_staff(current_user=Depends(require_staff), session: Session = Depends(get_session)):
    # Your staff logic here
    pass


# Similarly for other routes...
