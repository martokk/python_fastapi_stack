from typing import Any

import os

from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from sqlmodel import Session, select

from app import crud, models
from app.paths import UPLOAD_PATH
from app.utils.templates import templates
from app.views.deps import get_db
from app.views.pages.admin.deps import get_admin_context

router = APIRouter()


@router.get("/staff", response_class=HTMLResponse)
async def admin_staff(
    request: Request,
    context: dict[str, Any] = Depends(get_admin_context),
    session: Session = Depends(get_db),
) -> HTMLResponse:
    """Admin staff page"""
    if not context["user_permissions"].staff:
        return templates.TemplateResponse("admin/403.html", context, status_code=403)

    staff = session.exec(select(models.Staff)).all()
    context["staff_members"] = staff
    return templates.TemplateResponse("admin/staff.html", context)


@router.post("/staff")
async def create_staff(
    name: str = Form(...),
    position: str = Form(...),
    photo: UploadFile | None = File(None),
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Create new staff member"""
    if not context["user_permissions"].staff:
        return JSONResponse({"error": "Unauthorized"}, status_code=403)

    photo_url = None
    if photo:
        # Save photo to uploads/staff directory
        upload_dir = UPLOAD_PATH / "staff"
        os.makedirs(upload_dir, exist_ok=True)

        file_extension = os.path.splitext(photo.filename)[1]
        file_name = f"{name.lower().replace(' ', '_')}{file_extension}"
        file_path = upload_dir / file_name

        with open(file_path, "wb") as f:
            content = await photo.read()
            f.write(content)

        photo_url = f"/uploads/staff/{file_name}"

    staff_in = models.StaffCreate(
        name=name,
        position=position,
        photo_url=photo_url,
    )
    staff = await crud.staff.create(db=db, obj_in=staff_in)
    return JSONResponse({"id": staff.id})


@router.get("/staff/{staff_id}")
async def get_staff(
    staff_id: int,
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Get staff member by ID"""
    if not context["user_permissions"].staff:
        return JSONResponse({"error": "Unauthorized"}, status_code=403)

    staff = await crud.staff.get(db=db, id=staff_id)
    if not staff:
        return JSONResponse({"error": "Staff member not found"}, status_code=404)

    return JSONResponse(
        {
            "id": staff.id,
            "name": staff.name,
            "position": staff.position,
            "photo_url": staff.photo_url,
        }
    )


@router.put("/staff/{staff_id}")
async def update_staff(
    staff_id: int,
    name: str = Form(...),
    position: str = Form(...),
    photo: UploadFile | None = File(None),
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Update staff member"""
    if not context["user_permissions"].staff:
        return JSONResponse({"error": "Unauthorized"}, status_code=403)

    staff = await crud.staff.get(db=db, id=staff_id)
    if not staff:
        return JSONResponse({"error": "Staff member not found"}, status_code=404)

    # Handle photo upload if provided
    photo_url = staff.photo_url
    if photo:
        # Save photo to uploads/staff directory
        upload_dir = UPLOAD_PATH / "staff"
        os.makedirs(upload_dir, exist_ok=True)

        # Delete old photo if it exists
        if staff.photo_url:
            old_file_path = UPLOAD_PATH / staff.photo_url.lstrip("/uploads/")
            if os.path.exists(old_file_path):
                os.remove(old_file_path)

        file_extension = os.path.splitext(photo.filename)[1]
        file_name = f"{name.lower().replace(' ', '_')}{file_extension}"
        file_path = upload_dir / file_name

        with open(file_path, "wb") as f:
            content = await photo.read()
            f.write(content)

        photo_url = f"/uploads/staff/{file_name}"

    staff_in = models.StaffUpdate(
        name=name,
        position=position,
        photo_url=photo_url,
    )
    staff = await crud.staff.update(db=db, db_obj=staff, obj_in=staff_in)
    return JSONResponse({"id": staff.id})


@router.delete("/staff/{staff_id}")
async def delete_staff(
    staff_id: int,
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Delete staff member"""
    if not context["user_permissions"].staff:
        return JSONResponse({"error": "Unauthorized"}, status_code=403)

    staff = await crud.staff.get(db=db, id=staff_id)
    if not staff:
        return JSONResponse({"error": "Staff member not found"}, status_code=404)

    # Delete photo file if it exists
    if staff.photo_url:
        file_path = UPLOAD_PATH / staff.photo_url.lstrip("/uploads/")
        if os.path.exists(file_path):
            os.remove(file_path)

    await crud.staff.remove(db=db, id=staff_id)
    return JSONResponse({"status": "success"})
