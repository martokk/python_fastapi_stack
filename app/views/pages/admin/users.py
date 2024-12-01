from typing import Any

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from sqlmodel import Session

from app import crud, models
from app.utils.model_utils import get_permission_fields
from app.utils.templates import templates
from app.views.deps import get_db
from app.views.pages.admin.deps import get_admin_context

router = APIRouter()


@router.get("/users", response_class=HTMLResponse)
async def admin_users(
    request: Request,
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> HTMLResponse:
    """Admin users page"""
    if not context["user_permissions"].users:
        return templates.TemplateResponse("admin/403.html", context, status_code=403)

    users = await crud.user.get_non_superusers(db=db)
    permission_fields = get_permission_fields()

    context.update({"users": users, "permission_fields": permission_fields})

    return templates.TemplateResponse("admin/users.html", context)


@router.post("/users")
async def create_user(
    request: Request,
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Create a new user"""
    if not context["user_permissions"].users:
        return JSONResponse({"error": "Unauthorized"}, status_code=403)

    try:
        data = await request.json()
        user_in = models.UserCreateWithPassword(
            username=data["username"],
            email=data["email"],
            full_name=data.get("full_name"),
            password=data["password"],
        )

        user = await crud.user.create_with_permissions(db=db, obj_in=user_in)

        if "permissions" in data:
            await crud.user.update_permissions(
                db=db, user_id=user.id, permissions_data=data["permissions"]
            )

        return JSONResponse({"status": "success"})

    except ValueError as e:
        error_msg = str(e)
        if ":" in error_msg:
            field, message = error_msg.split(":", 1)
            return JSONResponse(
                {"error": message, "field": field},
                status_code=400,
            )
        return JSONResponse({"error": error_msg}, status_code=400)
    except Exception as e:
        return JSONResponse({"error": f"Failed to create user: {str(e)}"}, status_code=500)


@router.get("/users/{user_id}")
async def get_user(
    request: Request,
    user_id: str,
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Get user details"""
    if not context["user_permissions"].users:
        return JSONResponse({"error": "Unauthorized"}, status_code=403)

    user = await crud.user.get(db=db, id=user_id)
    return JSONResponse(
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
        }
    )


@router.put("/users/{user_id}")
async def update_user(
    request: Request,
    user_id: str,
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Update user details"""
    if not context["user_permissions"].users:
        return JSONResponse({"error": "Unauthorized"}, status_code=403)

    data = await request.json()
    user = await crud.user.get(db=db, id=user_id)

    update_data = models.UserUpdate(
        email=data.get("email"),
        full_name=data.get("full_name"),
    )

    if "password" in data and data["password"]:
        update_data.hashed_password = crud.user.get_password_hash(data["password"])

    await crud.user.update(db=db, db_obj=user, obj_in=update_data)
    return JSONResponse({"status": "success"})


@router.delete("/users/{user_id}")
async def delete_user(
    request: Request,
    user_id: str,
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Delete a user"""
    if not context["user_permissions"].users:
        return JSONResponse({"error": "Unauthorized"}, status_code=403)

    user = await crud.user.get(db=db, id=user_id)
    if user.is_superuser:
        return JSONResponse({"error": "Cannot delete superuser"}, status_code=400)

    await crud.user.remove(db=db, id=user_id)
    return JSONResponse({"status": "success"})


@router.get("/users/{user_id}/permissions")
async def get_user_permissions(
    request: Request,
    user_id: str,
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Get user permissions"""
    if not context["user_permissions"].users:
        return JSONResponse({"error": "Unauthorized"}, status_code=403)

    permissions = await crud.user.get_permissions(db=db, user_id=user_id)
    if not permissions:
        return JSONResponse({"error": "Permissions not found"}, status_code=404)

    return JSONResponse({field: getattr(permissions, field) for field in get_permission_fields()})


@router.put("/users/{user_id}/permissions")
async def update_user_permissions(
    request: Request,
    user_id: str,
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Update user permissions"""
    if not context["user_permissions"].users:
        return JSONResponse({"error": "Unauthorized"}, status_code=403)

    data = await request.json()
    await crud.user.update_permissions(db=db, user_id=user_id, permissions_data=data)
    return JSONResponse({"status": "success"})
