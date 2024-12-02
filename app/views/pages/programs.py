from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse
from sqlmodel import Session

from app import crud
from app.views import deps, templates

router = APIRouter()


@router.get("/food-pantry", response_class=HTMLResponse)
async def food_pantry(
    request: Request,
) -> Response:
    """
    Food Pantry page

    Returns:
        Response: Food Pantry page
    """
    context = {
        "request": request,
    }
    return templates.TemplateResponse("programs/food-pantry.html", context=context)


@router.get("/breakfast", response_class=HTMLResponse)
async def breakfast(
    request: Request,
) -> Response:
    """
    Breakfast Program page
    """
    context = {
        "request": request,
    }
    return templates.TemplateResponse("programs/breakfast.html", context=context)


@router.get("/showers", response_class=HTMLResponse)
async def showers(
    request: Request,
) -> Response:
    """
    Shower Program page
    """
    context = {
        "request": request,
    }
    return templates.TemplateResponse("programs/showers.html", context=context)


@router.get("/homeless-services", response_class=HTMLResponse)
async def homeless_services(
    request: Request,
    db: Session = Depends(deps.get_db),
) -> Response:
    """
    Homeless Services page
    """
    program_name = "Homeless Services"
    faqs = await crud.programs.get_faqs_by_program_name(db=db, name=program_name)

    context = {
        "request": request,
        "faqs": faqs,
    }
    return templates.TemplateResponse("programs/homeless-services.html", context=context)
