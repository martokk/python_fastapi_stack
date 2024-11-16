from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from sqlmodel import Session

from app import crud, models
from app.views import deps, templates

router = APIRouter()


@router.get("/guests", response_class=HTMLResponse)
async def list_guests(
    request: Request,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Returns HTML response with list of guests.

    Args:
        request(Request): The request object
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: HTML page with the guests

    """
    # Get alerts dict from cookies
    alerts = models.Alerts().from_cookies(request.cookies)

    guests = await crud.guest.get_multi(db=db, owner_id=current_user.id)
    return templates.TemplateResponse(
        "guest/list.html",
        {"request": request, "guests": guests, "current_user": current_user, "alerts": alerts},
    )


@router.get("/guests/all", response_class=HTMLResponse)
async def list_all_guests(
    request: Request,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_superuser
    ),
) -> Response:
    """
    Returns HTML response with list of all guests from all users.

    Args:
        request(Request): The request object
        db(Session): The database session.
        current_user(User): The authenticated superuser.

    Returns:
        Response: HTML page with the guests

    """
    # Get alerts dict from cookies
    alerts = models.Alerts().from_cookies(request.cookies)

    guests = await crud.guest.get_all(db=db)
    return templates.TemplateResponse(
        "guest/list.html",
        {"request": request, "guests": guests, "current_user": current_user, "alerts": alerts},
    )


@router.get("/guest/{guest_id}", response_class=HTMLResponse)
async def view_guest(
    request: Request,
    guest_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    View guest.

    Args:
        request(Request): The request object
        guest_id(str): The guest id
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: View of the guest
    """
    alerts = models.Alerts()
    try:
        guest = await crud.guest.get(db=db, id=guest_id)
    except crud.RecordNotFoundError:
        alerts.danger.append("Guest not found")
        response = RedirectResponse("/guests", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response

    return templates.TemplateResponse(
        "guest/view.html",
        {"request": request, "guest": guest, "current_user": current_user, "alerts": alerts},
    )


@router.get("/guests/create", response_class=HTMLResponse)
async def create_guest(
    request: Request,
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    New Guest form.

    Args:
        request(Request): The request object
        current_user(User): The authenticated user.

    Returns:
        Response: Form to create a new guest
    """
    alerts = models.Alerts().from_cookies(request.cookies)
    return templates.TemplateResponse(
        "guest/create.html",
        {"request": request, "current_user": current_user, "alerts": alerts},
    )


@router.post("/guests/create", response_class=HTMLResponse, status_code=status.HTTP_201_CREATED)
async def handle_create_guest(
    title: str = Form(...),
    description: str = Form(...),
    url: str = Form(...),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Handles the creation of a new guest.

    Args:
        title(str): The title of the guest
        description(str): The description of the guest
        url(str): The url of the guest
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: List of guests view
    """
    alerts = models.Alerts()
    guest_create = models.GuestCreate(
        title=title, description=description, url=url, owner_id=current_user.id
    )
    try:
        await crud.guest.create(db=db, obj_in=guest_create)
    except crud.RecordAlreadyExistsError:
        alerts.danger.append("Guest already exists")
        response = RedirectResponse("/guests/create", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response

    alerts.success.append("Guest successfully created")
    response = RedirectResponse(url="/guests", status_code=status.HTTP_303_SEE_OTHER)
    response.headers["Method"] = "GET"
    response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
    return response


@router.get("/guest/{guest_id}/edit", response_class=HTMLResponse)
async def edit_guest(
    request: Request,
    guest_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    New Guest form.

    Args:
        request(Request): The request object
        guest_id(str): The guest id
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: Form to create a new guest
    """
    alerts = models.Alerts().from_cookies(request.cookies)
    try:
        guest = await crud.guest.get(db=db, id=guest_id)
    except crud.RecordNotFoundError:
        alerts.danger.append("Guest not found")
        response = RedirectResponse("/guests", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response
    return templates.TemplateResponse(
        "guest/edit.html",
        {"request": request, "guest": guest, "current_user": current_user, "alerts": alerts},
    )


@router.post("/guest/{guest_id}/edit", response_class=HTMLResponse)
async def handle_edit_guest(
    request: Request,
    guest_id: str,
    title: str = Form(...),
    description: str = Form(...),
    url: str = Form(...),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    Handles the creation of a new guest.

    Args:
        request(Request): The request object
        guest_id(str): The guest id
        title(str): The title of the guest
        description(str): The description of the guest
        url(str): The url of the guest
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: View of the newly created guest
    """
    alerts = models.Alerts()
    guest_update = models.GuestUpdate(title=title, description=description, url=url)

    try:
        new_guest = await crud.guest.update(db=db, obj_in=guest_update, id=guest_id)
    except crud.RecordNotFoundError:
        alerts.danger.append("Guest not found")
        response = RedirectResponse(url="/guests", status_code=status.HTTP_303_SEE_OTHER)
        response.headers["Method"] = "GET"
        response.set_cookie(key="alerts", value=alerts.json(), httponly=True, max_age=5)
        return response
    alerts.success.append("Guest updated")
    return templates.TemplateResponse(
        "guest/edit.html",
        {"request": request, "guest": new_guest, "current_user": current_user, "alerts": alerts},
    )


@router.get("/guest/{guest_id}/delete", response_class=HTMLResponse)
async def delete_guest(
    guest_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(  # pylint: disable=unused-argument
        deps.get_current_active_user
    ),
) -> Response:
    """
    New Guest form.

    Args:
        guest_id(str): The guest id
        db(Session): The database session.
        current_user(User): The authenticated user.

    Returns:
        Response: Form to create a new guest
    """
    alerts = models.Alerts()
    try:
        await crud.guest.remove(db=db, id=guest_id)
        alerts.success.append("Guest deleted")
    except crud.RecordNotFoundError:
        alerts.danger.append("Guest not found")
    except crud.DeleteError:
        alerts.danger.append("Error deleting guest")

    response = RedirectResponse(url="/guests", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="alerts", value=alerts.json(), max_age=5, httponly=True)
    return response
