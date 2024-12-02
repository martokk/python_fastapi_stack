from typing import Any

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from sqlmodel import Session, select
from fastapi.encoders import jsonable_encoder
from fastapi import Body

from app import crud
from app.models.alerts import Alerts
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

    stats = await crud.stats.get_first(db=session)
    if not stats:
        stats = await crud.stats.create(db=session, obj_in=Stats())

    context["stats"] = stats
    context["alerts"] = Alerts().from_request(request=request)
    return templates.TemplateResponse("admin/stats.html", context)


@router.put("/stats", response_class=Response)
async def update_stats(
    request: Request,
    stats_data: dict = Body(...),
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> Response:
    """Update stats"""
    if not context["user_permissions"].stats:
        return Response(status_code=403)

    stats = await crud.stats.get_first(db=db)
    if not stats:
        stats = await crud.stats.create(db=db, obj_in=Stats())

    # Update stats with new values
    stats_update = Stats(**stats_data)
    stats = await crud.stats.update(db=db, db_obj=stats, obj_in=stats_update)

    alerts = Alerts()
    alerts.success.append("Statistics updated successfully")
    response = Response(status_code=200)
    response.set_cookie(
        key="alerts", value=alerts.model_dump_json(), max_age=5, httponly=True, samesite="lax"
    )
    return response
