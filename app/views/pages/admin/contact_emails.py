from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select

from app import crud, models
from app.core import notify
from app.utils.templates import templates
from app.views.deps import get_db
from app.views.pages.admin.deps import get_admin_context

router = APIRouter()


@router.get("/contact-emails", response_class=HTMLResponse)
async def admin_contact_emails(
    request: Request,
    filter: str = "all",
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> HTMLResponse:
    """Admin contact emails page"""
    if not context["user_permissions"].contact_emails:
        return templates.TemplateResponse("admin/403.html", context, status_code=403)

    # Get unsent count
    unsent_count = await crud.contact_emails.get_unsent_count(db=db)

    # Get filtered emails
    emails = await crud.contact_emails.get_filtered(
        db=db, filter_status=filter if filter != "all" else None
    )

    context.update({"emails": emails, "unsent_count": unsent_count, "filter": filter})
    return templates.TemplateResponse("admin/contact_emails.html", context)


@router.post("/contact-emails/{email_id}/resend", response_class=HTMLResponse)
async def resend_contact_email(
    email_id: int,
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> HTMLResponse:
    """Resend contact email"""
    if not context["user_permissions"].contact_emails:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Get email
    contact_email = await crud.contact_emails.get(db=db, id=email_id)
    if not contact_email:
        raise HTTPException(status_code=404, detail="Email not found")

    # Get variables for admin email
    variables = db.exec(select(models.Variables)).first()
    if not variables or not variables.email:
        raise HTTPException(status_code=400, detail="Admin email not configured")

    # Send email
    try:
        message = f"""
        Name: {contact_email.name} <br>
        Email: {contact_email.email} <br>
        Subject: {contact_email.subject} <br><br>
        {contact_email.message}
        """

        response = notify.send_email(
            email_to=variables.email,
            subject=contact_email.subject,
            message=message,
        )

        if response and getattr(response, "status_code", None) == 250:
            contact_email.sent = True
            db.commit()
            return HTMLResponse(status_code=200)
        else:
            raise HTTPException(status_code=500, detail="Failed to send email")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
