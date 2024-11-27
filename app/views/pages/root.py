from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse

from app import models
from app.views import deps, templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def root_index_router(
    request: Request,
    current_user: models.User = Depends(deps.get_current_user),
) -> Response:
    """
    Home page router

    Args:
        request(Request): The request object
        current_user(models.User): The current user

    Returns:
        Response: Home page
    """
    if current_user:
        return await root_index_authenticated(request, current_user)
    return await root_index_unauthenticated(request)


async def root_index_unauthenticated(
    request: Request,
) -> Response:
    """
    Home page (Not authenticated)

    Returns:
        Response: Home page
    """
    context = {
        "request": request,
    }
    return templates.TemplateResponse("root/home.html", context=context)


async def root_index_authenticated(
    request: Request,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Response:
    """
    Home page. (Authenticated)

    Args:
        request(Request): The request object
        current_user(models.User): The current user

    Returns:
        Response: Home page
    """
    alerts = models.Alerts().from_cookies(request.cookies)
    context = {
        "request": request,
        "current_user": current_user,
        "alerts": alerts,
    }
    return templates.TemplateResponse("root/home.html", context=context)


@router.get("/services", response_class=HTMLResponse)
async def services(
    request: Request,
) -> Response:
    """
    Services page

    Returns:
        Response: Services page
    """
    context = {
        "request": request,
    }
    return templates.TemplateResponse("root/services.html", context=context)


@router.get("/volunteer", response_class=HTMLResponse)
async def volunteer(
    request: Request,
) -> Response:
    """
    Volunteer page

    Returns:
        Response: Volunteer page
    """
    context = {
        "request": request,
    }
    return templates.TemplateResponse("root/volunteer.html", context=context)


@router.get("/about", response_class=HTMLResponse)
async def about(
    request: Request,
) -> Response:
    """
    About page

    Returns:
        Response: About page
    """
    context = {
        "request": request,
    }
    return templates.TemplateResponse("root/about.html", context=context)


@router.get("/contact", response_class=HTMLResponse)
async def contact(
    request: Request,
) -> Response:
    """
    Contact page

    Returns:
        Response: Contact page
    """
    context = {
        "request": request,
    }
    return templates.TemplateResponse("root/contact.html", context=context)


@router.get("/donate", response_class=HTMLResponse)
async def donate(
    request: Request,
) -> Response:
    """
    Donate page

    Returns:
        Response: Donate page
    """
    context = {
        "request": request,
    }
    return templates.TemplateResponse("root/donate.html", context=context)


@router.get("/about2", response_class=HTMLResponse)
async def about(
    request: Request,
) -> Response:
    """
    About page

    Returns:
        Response: About page
    """
    context = {
        "request": request,
    }
    return templates.TemplateResponse("temp/about.html", context=context)
