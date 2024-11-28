from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse

from app import models
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
) -> Response:
    """
    Homeless Services page
    """
    context = {
        "request": request,
    }
    return templates.TemplateResponse("programs/homeless-services.html", context=context)
