from typing import Any

from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from sqlmodel import Session, col, select

from app import crud, models
from app.paths import UPLOAD_PATH
from app.utils.templates import templates
from app.views.deps import get_db
from app.views.pages.admin.deps import get_admin_context


class OrderUpdate(BaseModel):
    id: int
    order: int


class OrderUpdateRequest(BaseModel):
    updates: list[OrderUpdate]


router = APIRouter()


@router.get("/staff", response_class=HTMLResponse)
async def admin_staff(
    request: Request,
    context: dict[str, Any] = Depends(get_admin_context),
    session: Session = Depends(get_db),
) -> HTMLResponse:
    """Admin staff members page"""
    if not context["user_permissions"].staff:
        return templates.TemplateResponse("admin/403.html", context, status_code=403)

    staff_members = session.exec(select(models.Staff).order_by(col(models.Staff.order))).all()
    context["staff_members"] = staff_members
    return templates.TemplateResponse("admin/staff.html", context)


@router.post("/staff")
async def create_staff_member(
    name: str = Form(...),
    position: str = Form(...),
    photo: UploadFile | None = File(None),
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Create new staff member"""
    if not context["user_permissions"].staff:
        return JSONResponse({"error": "Unauthorized"}, status_code=403)

    # Get max order and add 1
    result = db.exec(select(models.Staff).order_by(col(models.Staff.order).desc())).first()
    next_order = (result.order + 1) if result else 0

    # Handle photo upload
    photo_url = None
    if photo:
        photo_url = await crud.staff.save_photo(photo, name)

    staff_member = models.StaffCreate(
        name=name,
        position=position,
        photo_url=photo_url,
        order=next_order,
    )
    created_member = await crud.staff.create(db=db, obj_in=staff_member)
    return JSONResponse({"id": created_member.id})


@router.get("/staff/{staff_id}")
async def get_staff_member(
    staff_id: int,
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Get staff member by ID"""
    if not context["user_permissions"].staff:
        return JSONResponse({"error": "Unauthorized"}, status_code=403)

    staff_member = await crud.staff.get(db=db, id=staff_id)
    if not staff_member:
        return JSONResponse({"error": "Staff member not found"}, status_code=404)

    return JSONResponse(
        {
            "id": staff_member.id,
            "name": staff_member.name,
            "position": staff_member.position,
            "photo_url": staff_member.photo_url,
        }
    )


@router.put("/staff/{staff_id}")
async def update_staff_member(
    staff_id: int,
    name: str = Form(...),
    position: str = Form(...),
    photo: UploadFile | None = File(None),
    remove_photo: bool = Form(False),
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Update staff member"""
    if not context["user_permissions"].staff:
        return JSONResponse({"error": "Unauthorized"}, status_code=403)

    staff_member = await crud.staff.get(db=db, id=staff_id)
    if not staff_member:
        return JSONResponse({"error": "Staff member not found"}, status_code=404)

    # Handle photo update
    photo_url = staff_member.photo_url
    if remove_photo:
        photo_url = None
        if staff_member.photo_url:
            await crud.staff.delete_photo(staff_member.photo_url)
    elif photo:
        if staff_member.photo_url:
            await crud.staff.delete_photo(staff_member.photo_url)
        photo_url = await crud.staff.save_photo(photo, name)

    staff_update = models.StaffUpdate(
        name=name,
        position=position,
        photo_url=photo_url,
    )
    staff_member = await crud.staff.update(db=db, db_obj=staff_member, obj_in=staff_update)
    return JSONResponse({"id": staff_member.id})


@router.put("/staff-order")
async def update_staff_members_order(
    order_update: OrderUpdateRequest,
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Update staff members order"""
    if not context["user_permissions"].staff:
        return JSONResponse({"error": "Unauthorized"}, status_code=403)

    try:
        for update in order_update.updates:
            staff_member = await crud.staff.get(db=db, id=update.id)
            if staff_member:
                await crud.staff.update(
                    db=db,
                    db_obj=staff_member,
                    obj_in=models.StaffUpdate(order=update.order),
                )
        return JSONResponse({"status": "success"})
    except Exception as e:
        return JSONResponse({"error": f"Failed to update order: {str(e)}"}, status_code=400)


@router.delete("/staff/{staff_id}")
async def delete_staff_member(
    staff_id: int,
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Delete staff member"""
    if not context["user_permissions"].staff:
        return JSONResponse({"error": "Unauthorized"}, status_code=403)

    staff_member = await crud.staff.get(db=db, id=staff_id)
    if not staff_member:
        return JSONResponse({"error": "Staff member not found"}, status_code=404)

    if staff_member.photo_url:
        await crud.staff.delete_photo(staff_member.photo_url)

    await crud.staff.remove(db=db, id=staff_id)
    return JSONResponse({"status": "success"})


@router.get("/staff-list")
async def list_staff_members(
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Get list of staff members for order modal"""
    if not context["user_permissions"].staff:
        return JSONResponse({"error": "Unauthorized"}, status_code=403)

    staff_members = db.exec(select(models.Staff).order_by(col(models.Staff.order))).all()

    return JSONResponse(
        [{"id": member.id, "name": member.name, "order": member.order} for member in staff_members]
    )
