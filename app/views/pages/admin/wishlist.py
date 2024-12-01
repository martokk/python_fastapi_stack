from typing import Any

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from sqlmodel import Session

from app import crud
from app.models.alerts import Alerts
from app.models.wishlist import WishlistCreate, WishlistUpdate
from app.utils.templates import templates
from app.views.deps import get_db
from app.views.pages.admin.deps import get_admin_context

router = APIRouter()


@router.get("/wishlist", response_class=HTMLResponse)
async def admin_wishlist(
    request: Request,
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> HTMLResponse:
    """Admin wishlist page"""
    if not context["user_permissions"].wishlist:
        return templates.TemplateResponse("admin/403.html", context, status_code=403)

    wishlist = await crud.wishlist.get_first(db=db)
    if not wishlist:
        wishlist = await crud.wishlist.create(db=db, obj_in=WishlistCreate(content=""))

    context["wishlist"] = wishlist
    context["alerts"] = Alerts().from_request(request=request)
    return templates.TemplateResponse("admin/wishlist.html", context)


@router.post("/wishlist", response_class=Response)
async def update_wishlist(
    request: Request,
    content: str = Form(...),
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> Response:
    """Update wishlist content"""
    if not context["user_permissions"].wishlist:
        return templates.TemplateResponse("admin/403.html", context, status_code=403)

    wishlist = await crud.wishlist.get_first(db=db)
    if not wishlist:
        wishlist = await crud.wishlist.create(db=db, obj_in=WishlistCreate(content=content))
    else:
        wishlist = await crud.wishlist.update(
            db=db, db_obj=wishlist, obj_in=WishlistUpdate(content=content)
        )

    alerts = Alerts()
    alerts.success.append("Wishlist updated successfully")
    response = RedirectResponse(url="/admin/wishlist", status_code=302)
    response.set_cookie(
        key="alerts", value=alerts.model_dump_json(), max_age=5, httponly=True, samesite="lax"
    )
    return response
