from typing import Any

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from sqlmodel import Session

from app import crud, models
from app.utils.templates import templates
from app.views.deps import get_db
from app.views.pages.admin.deps import get_admin_context

router = APIRouter()


@router.get("/programs", response_class=HTMLResponse)
async def admin_programs(
    request: Request,
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> HTMLResponse:
    """Admin programs page"""
    if not context["user_permissions"].programs:
        return templates.TemplateResponse("admin/403.html", context, status_code=403)

    programs = await crud.programs.get_all(db=db)
    context["programs"] = programs
    return templates.TemplateResponse("admin/programs.html", context)


@router.post("/programs")
async def create_program(
    request: Request,
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Create a new program"""
    if not context["user_permissions"].programs:
        return JSONResponse({"error": "Unauthorized"}, status_code=403)

    try:
        data = await request.json()
        program_in = models.ProgramsCreate(name=data["name"])
        program = await crud.programs.create(db=db, obj_in=program_in)
        return JSONResponse({"status": "success", "id": program.id})
    except ValueError as e:
        return JSONResponse({"error": str(e)}, status_code=400)
    except Exception as e:
        return JSONResponse({"error": f"Failed to create program: {str(e)}"}, status_code=500)


@router.delete("/programs/{program_id}")
async def delete_program(
    request: Request,
    program_id: str,
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Delete a program and its associated FAQs"""
    if not context["user_permissions"].programs:
        return JSONResponse({"error": "Unauthorized"}, status_code=403)

    try:
        await crud.programs.remove(db=db, id=program_id)
        return JSONResponse({"status": "success"})
    except Exception as e:
        return JSONResponse({"error": f"Failed to delete program: {str(e)}"}, status_code=500)


@router.get("/programs/{program_id}")
async def get_program(
    request: Request,
    program_id: str,
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Get program details"""
    if not context["user_permissions"].programs:
        return JSONResponse({"error": "Unauthorized"}, status_code=403)

    program = await crud.programs.get(db=db, id=program_id)
    return JSONResponse(
        {
            "id": program.id,
            "name": program.name,
        }
    )


@router.put("/programs/{program_id}")
async def update_program(
    request: Request,
    program_id: str,
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Update program details"""
    if not context["user_permissions"].programs:
        return JSONResponse({"error": "Unauthorized"}, status_code=403)

    try:
        data = await request.json()
        program = await crud.programs.get(db=db, id=program_id)
        update_data = models.ProgramsUpdate(name=data["name"])  # Changed to direct access
        updated = await crud.programs.update(db=db, db_obj=program, obj_in=update_data)

        return JSONResponse({"status": "success"})
    except ValueError as e:
        return JSONResponse({"error": str(e)}, status_code=400)
    except Exception as e:
        return JSONResponse({"error": f"Failed to update program: {str(e)}"}, status_code=500)
