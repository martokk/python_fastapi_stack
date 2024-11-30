from typing import Any

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select

from app.models.wishlist import Wishlist
from app.utils.templates import templates
from app.views.deps import get_db
from app.views.pages.admin.deps import get_admin_context

router = APIRouter()


@router.get("/wishlist", response_class=HTMLResponse)
async def admin_wishlist(
    request: Request,
    context: dict[str, Any] = Depends(get_admin_context),
    session: Session = Depends(get_db),
) -> HTMLResponse:
    """Admin wishlist page"""
    if not context["user_permissions"].wish_list:
        return templates.TemplateResponse("admin/403.html", context, status_code=403)

    wishlist = session.exec(select(Wishlist)).first()
    if not wishlist:
        wishlist = Wishlist()
        session.add(wishlist)
        session.commit()

    context["wishlist"] = wishlist
    return templates.TemplateResponse("admin/wishlist.html", context)
