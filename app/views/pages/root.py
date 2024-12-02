from fastapi import APIRouter, Depends, Form, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import Session, select

from app import crud, models
from app.core import notify
from app.views import deps, templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def root_index_router(
    request: Request,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Response:
    """
    Home page router

    Args:
        request(Request): The request object
        current_user(models.User): The current user
        db(Session): Database session

    Returns:
        Response: Home page
    """
    # if current_user:
    #     return await root_index_authenticated(request, current_user)
    return await root_index_unauthenticated(request, db)


async def root_index_unauthenticated(
    request: Request,
    db: Session,
) -> Response:
    """
    Home page (Not authenticated)

    Args:
        request(Request): The request object
        db(Session): Database session

    Returns:
        Response: Home page
    """
    stats = await crud.stats.get_first(db=db)

    context = {
        "request": request,
        "stats": stats,
    }
    return templates.TemplateResponse("root/home.html", context=context)


async def root_index_authenticated(
    request: Request,
    current_user: models.User,
) -> Response:
    """
    Home page. (Authenticated)

    Args:
        request(Request): The request object
        current_user(models.User): The current user

    Returns:
        Response: Home page
    """
    # redirect to /admin
    return RedirectResponse(url="/admin")


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
    db: Session = Depends(deps.get_db),
) -> Response:
    """
    Volunteer page

    Returns:
        Response: Volunteer page
    """
    # Get stats
    stats = await crud.stats.get_first(db=db)

    # Get FAQs
    program_name = "Volunteer"
    faqs = await crud.programs.get_faqs_by_program_name(db=db, name=program_name)

    context = {
        "request": request,
        "stats": stats,
        "faqs": faqs,
    }
    return templates.TemplateResponse("root/volunteer.html", context=context)


@router.get("/about", response_class=HTMLResponse)
async def about(
    request: Request,
    db: Session = Depends(deps.get_db),
) -> Response:
    """
    About page

    Returns:
        Response: About page
    """
    # Get staff members
    staff_members = await crud.staff.get_all(db=db)

    # Get board members
    board_members = await crud.board_member.get_all(db=db)

    # Get partners
    partners = await crud.partners.get_all(db=db)

    # Get timeline items
    timeline_items = await crud.timeline.get_all(db=db)

    context = {
        "request": request,
        "staff_members": staff_members,
        "board_members": board_members,
        "partners": partners,
        "timeline_items": timeline_items,
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


@router.post("/contact", response_class=HTMLResponse)
async def contact_post(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    subject: str = Form(...),
    message: str = Form(...),
    db: Session = Depends(deps.get_db),
) -> Response:
    """Handle contact form submission"""
    # Create contact email record
    contact_email = await crud.contact_email.create(
        db=db,
        obj_in=models.ContactEmailCreate(
            name=name,
            email=email,
            subject=subject,
            message=message,
        ),
    )

    # Get admin email from variables
    variables = db.exec(select(models.Variables)).first()
    if variables and variables.email:
        try:
            # Try to send email
            response = notify.send_email(
                email_to=variables.email,
                subject=subject,
                message=f"From: {email} <br> Name: {name} <br> Subject: {subject} <br> Message: {message}",
            )

            # Update sent status if email was sent successfully
            if response and getattr(response, "status_code", None) == 250:
                contact_email.sent = True
                db.commit()
        except Exception:
            pass  # Email sending failed, but we'll still show success to user

    # Redirect to success page
    return templates.TemplateResponse("root/contact_success.html", {"request": request})


@router.get("/contact/success", response_class=HTMLResponse)
async def contact_success(
    request: Request,
) -> Response:
    """Contact success page"""
    return templates.TemplateResponse("root/contact_success.html", {"request": request})


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
