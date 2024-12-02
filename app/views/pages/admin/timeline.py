from typing import Any

from datetime import datetime

from fastapi import APIRouter, Body, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse, Response
from sqlmodel import Session, col, select

from app import crud
from app.models.alerts import Alerts
from app.models.timeline import Timeline
from app.utils.templates import templates
from app.views.deps import get_db
from app.views.pages.admin.deps import get_admin_context

router = APIRouter()


@router.get("/timeline", response_class=HTMLResponse)
async def admin_timeline(
    request: Request,
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> HTMLResponse:
    """Admin timeline page"""
    if not context["user_permissions"].timeline:
        return templates.TemplateResponse("admin/403.html", context, status_code=403)

    # Get timeline entries ordered by date (oldest first)
    timeline = db.exec(select(Timeline).order_by(col(Timeline.date))).all()
    context["timeline"] = timeline
    context["alerts"] = Alerts().from_request(request=request)
    return templates.TemplateResponse("admin/timeline.html", context)


@router.post("/timeline", response_class=Response)
async def create_timeline_entry(
    request: Request,
    timeline_data: dict[str, Any] = Body(...),
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> Response:
    """Create new timeline entry"""
    if not context["user_permissions"].timeline:
        return Response(status_code=403)

    # Convert date string to date object
    timeline_data["date"] = datetime.strptime(timeline_data["date"], "%Y-%m-%d").date()
    timeline_entry = Timeline(**timeline_data)
    await crud.timeline.create(db=db, obj_in=timeline_entry)

    alerts = Alerts()
    alerts.success.append("Timeline entry created successfully")
    response = Response(status_code=200)
    response.set_cookie(
        key="alerts", value=alerts.model_dump_json(), max_age=5, httponly=True, samesite="lax"
    )
    return response


@router.get("/timeline/{entry_id}", response_class=JSONResponse)
async def get_timeline_entry(
    entry_id: int,
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Get timeline entry by ID"""
    if not context["user_permissions"].timeline:
        return JSONResponse({"error": "Unauthorized"}, status_code=403)

    entry = await crud.timeline.get(db=db, id=entry_id)
    if not entry:
        return JSONResponse({"error": "Entry not found"}, status_code=404)

    return JSONResponse(
        {
            "id": entry.id,
            "date": str(entry.date),
            "title": entry.title,
            "description": entry.description,
        }
    )


@router.put("/timeline/{entry_id}", response_class=Response)
async def update_timeline_entry(
    entry_id: int,
    timeline_data: dict[str, Any] = Body(...),
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> Response:
    """Update timeline entry"""
    if not context["user_permissions"].timeline:
        return Response(status_code=403)

    entry = await crud.timeline.get(db=db, id=entry_id)
    if not entry:
        return Response(status_code=404)

    # Convert date string to date object
    timeline_data["date"] = datetime.strptime(timeline_data["date"], "%Y-%m-%d").date()
    timeline_update = Timeline(**timeline_data)
    await crud.timeline.update(db=db, db_obj=entry, obj_in=timeline_update)

    alerts = Alerts()
    alerts.success.append("Timeline entry updated successfully")
    response = Response(status_code=200)
    response.set_cookie(
        key="alerts", value=alerts.model_dump_json(), max_age=5, httponly=True, samesite="lax"
    )
    return response


@router.delete("/timeline/{entry_id}", response_class=Response)
async def delete_timeline_entry(
    entry_id: int,
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> Response:
    """Delete timeline entry"""
    if not context["user_permissions"].timeline:
        return Response(status_code=403)

    entry = await crud.timeline.get(db=db, id=entry_id)
    if not entry:
        return Response(status_code=404)

    await crud.timeline.remove(db=db, id=entry_id)
    return Response(status_code=200)
