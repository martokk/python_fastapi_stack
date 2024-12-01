from typing import Any

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from sqlmodel import Session

from app import crud, models
from app.utils.templates import templates
from app.views.deps import get_db
from app.views.pages.admin.deps import get_admin_context

router = APIRouter()


@router.get("/faq", response_class=HTMLResponse)
async def admin_faq(
    request: Request,
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> HTMLResponse:
    """Admin FAQ page"""
    if not context["user_permissions"].faq:
        return templates.TemplateResponse("admin/403.html", context, status_code=403)

    faqs = await crud.faq.get_all_ordered(db=db)
    programs = await crud.programs.get_all(db=db)
    context.update({"faqs": faqs, "programs": programs})
    return templates.TemplateResponse("admin/faq.html", context)


@router.get("/faq/programs/{program_id}/items")
async def get_program_faqs(
    request: Request,
    program_id: str,
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Get FAQs for a specific program"""
    if not context["user_permissions"].faq:
        return JSONResponse({"error": "Unauthorized"}, status_code=403)

    faqs = await crud.faq.get_by_program(db=db, program_id=program_id)
    return JSONResponse(
        [{"id": faq.id, "question": faq.question, "order": faq.order} for faq in faqs]
    )


@router.post("/faq")
async def create_faq(
    request: Request,
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Create a new FAQ"""
    if not context["user_permissions"].faq:
        return JSONResponse({"error": "Unauthorized"}, status_code=403)

    try:
        data = await request.json()
        faq_in = models.FAQCreate(
            program_id=data["program_id"],
            question=data["question"],
            answer=data["answer"],
        )
        faq = await crud.faq.create(db=db, obj_in=faq_in)
        return JSONResponse({"status": "success", "id": faq.id})
    except ValueError as e:
        return JSONResponse({"error": str(e)}, status_code=400)
    except Exception as e:
        return JSONResponse({"error": f"Failed to create FAQ: {str(e)}"}, status_code=500)


@router.get("/faq/{faq_id}")
async def get_faq(
    request: Request,
    faq_id: int,
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Get FAQ details"""
    if not context["user_permissions"].faq:
        return JSONResponse({"error": "Unauthorized"}, status_code=403)

    faq = await crud.faq.get(db=db, id=faq_id)
    return JSONResponse(
        {
            "id": faq.id,
            "program_id": faq.program_id,
            "question": faq.question,
            "answer": faq.answer,
        }
    )


@router.put("/faq/{faq_id}")
async def update_faq(
    request: Request,
    faq_id: int,
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Update FAQ details"""
    if not context["user_permissions"].faq:
        return JSONResponse({"error": "Unauthorized"}, status_code=403)

    try:
        data = await request.json()
        faq = await crud.faq.get(db=db, id=faq_id)
        update_data = models.FAQUpdate(
            program_id=data.get("program_id"),
            question=data.get("question"),
            answer=data.get("answer"),
        )
        await crud.faq.update(db=db, db_obj=faq, obj_in=update_data)
        return JSONResponse({"status": "success"})
    except ValueError as e:
        return JSONResponse({"error": str(e)}, status_code=400)
    except Exception as e:
        return JSONResponse({"error": f"Failed to update FAQ: {str(e)}"}, status_code=500)


@router.delete("/faq/{faq_id}")
async def delete_faq(
    request: Request,
    faq_id: int,
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Delete a FAQ"""
    if not context["user_permissions"].faq:
        return JSONResponse({"error": "Unauthorized"}, status_code=403)

    try:
        await crud.faq.remove(db=db, id=faq_id)
        return JSONResponse({"status": "success"})
    except Exception as e:
        return JSONResponse({"error": f"Failed to delete FAQ: {str(e)}"}, status_code=500)


@router.put("/faq/programs/{program_id}/order")
async def update_faq_order(
    request: Request,
    program_id: str,
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Update FAQ order for a program"""
    if not context["user_permissions"].faq:
        return JSONResponse({"error": "Unauthorized"}, status_code=403)

    try:
        data = await request.json()
        await crud.faq.update_orders(db=db, program_id=program_id, faq_orders=data["orders"])
        return JSONResponse({"status": "success"})
    except ValueError as e:
        return JSONResponse({"error": str(e)}, status_code=400)
    except Exception as e:
        return JSONResponse({"error": f"Failed to update FAQ order: {str(e)}"}, status_code=500)
