from typing import Any

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select

from app.models.alerts import Alerts
from app.models.variables import Variables
from app.utils.templates import templates
from app.views.deps import get_db
from app.views.pages.admin.deps import get_admin_context

router = APIRouter()


@router.get("/variables", response_class=HTMLResponse)
async def admin_variables(
    request: Request,
    context: dict[str, Any] = Depends(get_admin_context),
    session: Session = Depends(get_db),
) -> HTMLResponse:
    """Admin variables page"""
    if not context["user_permissions"].variables:
        return templates.TemplateResponse("admin/403.html", context, status_code=403)

    variables = session.exec(select(Variables)).first()
    if not variables:
        variables = Variables(
            phone="",
            email="",
            service_address_1="",
            service_address_2="",
            mailing_address_1="",
            mailing_address_2="",
        )
        session.add(variables)
        session.commit()

    context["variables"] = variables
    return templates.TemplateResponse("admin/variables.html", context)


@router.post("/variables", response_class=HTMLResponse)
async def admin_variables_post(
    request: Request,
    phone: str = Form(...),
    email: str = Form(...),
    service_address_1: str = Form(...),
    service_address_2: str = Form(""),
    mailing_address_1: str = Form(...),
    mailing_address_2: str = Form(""),
    kwc_mission: str = Form(...),
    kwc_vision: str = Form(...),
    kwc_values: str = Form(...),
    context: dict[str, Any] = Depends(get_admin_context),
    session: Session = Depends(get_db),
) -> HTMLResponse:
    """Update variables"""
    if not context["user_permissions"].variables:
        return templates.TemplateResponse("admin/403.html", context, status_code=403)

    variables = session.exec(select(Variables)).first()
    if not variables:
        variables = Variables(
            phone=phone,
            email=email,
            service_address_1=service_address_1,
            service_address_2=service_address_2,
            mailing_address_1=mailing_address_1,
            mailing_address_2=mailing_address_2,
            kwc_mission=kwc_mission,
            kwc_vision=kwc_vision,
            kwc_values=kwc_values,
        )
        session.add(variables)

    variables.phone = phone
    variables.email = email
    variables.service_address_1 = service_address_1
    variables.service_address_2 = service_address_2
    variables.mailing_address_1 = mailing_address_1
    variables.mailing_address_2 = mailing_address_2
    variables.kwc_mission = kwc_mission
    variables.kwc_vision = kwc_vision
    variables.kwc_values = kwc_values
    session.commit()

    # Add success alert
    alerts = Alerts()
    alerts.success.append("Variables updated successfully!")
    context["alerts"] = alerts

    # Add updated variables to context
    context["variables"] = variables

    return templates.TemplateResponse("admin/variables.html", context)
