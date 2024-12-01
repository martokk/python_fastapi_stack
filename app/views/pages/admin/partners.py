from typing import Any

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from sqlmodel import Session, col, select

from app import crud, models
from app.utils.templates import templates
from app.views.deps import get_db
from app.views.pages.admin.deps import get_admin_context


class OrderUpdate(BaseModel):
    id: int
    order: int


class OrderUpdateRequest(BaseModel):
    updates: list[OrderUpdate]


router = APIRouter()


@router.get("/partners", response_class=HTMLResponse)
async def admin_partners(
    request: Request,
    context: dict[str, Any] = Depends(get_admin_context),
    session: Session = Depends(get_db),
) -> HTMLResponse:
    """Admin partners page"""
    if not context["user_permissions"].partners:
        return templates.TemplateResponse("admin/403.html", context, status_code=403)

    partners = session.exec(select(models.Partner).order_by(col(models.Partner.order))).all()
    context["partners"] = partners
    return templates.TemplateResponse("admin/partners.html", context)


@router.post("/partners")
async def create_partner(
    name: str = Form(...),
    url: str = Form(...),
    logo: UploadFile | None = File(None),
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Create new partner"""
    if not context["user_permissions"].partners:
        raise HTTPException(status_code=403, detail="Unauthorized")

    try:
        # Get max order and add 1
        result = db.exec(select(models.Partner).order_by(col(models.Partner.order).desc())).first()
        next_order = (result.order + 1) if result else 0

        # Handle logo upload
        logo_url = None
        if logo and logo.filename:
            try:
                logo_url = await crud.partners.save_photo(logo, name)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Failed to save logo: {str(e)}")

        # Ensure URL has https://
        if not url.startswith("http://") and not url.startswith("https://"):
            url = f"https://{url}"

        partner = models.PartnerCreate(
            name=name,
            url=url,
            logo_url=logo_url,
            order=next_order,
        )
        created_partner = await crud.partners.create(db=db, obj_in=partner)
        return JSONResponse({"id": created_partner.id})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/partners/{partner_id}")
async def get_partner(
    partner_id: int,
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Get partner by ID"""
    if not context["user_permissions"].partners:
        raise HTTPException(status_code=403, detail="Unauthorized")

    partner = await crud.partners.get(db=db, id=partner_id)
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")

    return JSONResponse(
        {
            "id": partner.id,
            "name": partner.name,
            "url": partner.url,
            "logo_url": partner.logo_url,
        }
    )


@router.put("/partners/{partner_id}")
async def update_partner(
    partner_id: int,
    name: str = Form(...),
    url: str = Form(...),
    logo: UploadFile | None = File(None),
    remove_logo: bool = Form(False),
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Update partner"""
    if not context["user_permissions"].partners:
        raise HTTPException(status_code=403, detail="Unauthorized")

    try:
        partner = await crud.partners.get(db=db, id=partner_id)
        if not partner:
            raise HTTPException(status_code=404, detail="Partner not found")

        # Handle logo update
        logo_url = partner.logo_url
        if remove_logo:
            logo_url = None
            if partner.logo_url:
                try:
                    await crud.partners.delete_photo(partner.logo_url)
                except Exception as e:
                    raise HTTPException(status_code=400, detail=f"Failed to remove logo: {str(e)}")
        elif logo and logo.filename:
            try:
                if partner.logo_url:
                    await crud.partners.delete_photo(partner.logo_url)
                logo_url = await crud.partners.save_photo(logo, name)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Failed to update logo: {str(e)}")

        # Ensure URL has https://
        if not url.startswith("http://") and not url.startswith("https://"):
            url = f"https://{url}"

        partner_update = models.PartnerUpdate(
            name=name,
            url=url,
            logo_url=logo_url,
        )
        partner = await crud.partners.update(db=db, db_obj=partner, obj_in=partner_update)
        return JSONResponse({"id": partner.id})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/partners-order")
async def update_partners_order(
    order_update: OrderUpdateRequest,
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Update partners order"""
    if not context["user_permissions"].partners:
        raise HTTPException(status_code=403, detail="Unauthorized")

    try:
        for update in order_update.updates:
            partner = await crud.partners.get(db=db, id=update.id)
            if partner:
                await crud.partners.update(
                    db=db,
                    db_obj=partner,
                    obj_in=models.PartnerUpdate(order=update.order),
                )
        return JSONResponse({"status": "success"})
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to update order: {str(e)}")


@router.delete("/partners/{partner_id}")
async def delete_partner(
    partner_id: int,
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Delete partner"""
    if not context["user_permissions"].partners:
        raise HTTPException(status_code=403, detail="Unauthorized")

    try:
        partner = await crud.partners.get(db=db, id=partner_id)
        if not partner:
            raise HTTPException(status_code=404, detail="Partner not found")

        if partner.logo_url:
            try:
                await crud.partners.delete_photo(partner.logo_url)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Failed to delete logo: {str(e)}")

        await crud.partners.remove(db=db, id=partner_id)
        return JSONResponse({"status": "success"})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/partners-list")
async def list_partners(
    context: dict[str, Any] = Depends(get_admin_context),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Get list of partners for order modal"""
    if not context["user_permissions"].partners:
        raise HTTPException(status_code=403, detail="Unauthorized")

    try:
        partners = db.exec(select(models.Partner).order_by(col(models.Partner.order))).all()
        return JSONResponse(
            [
                {"id": partner.id, "name": partner.name, "order": partner.order}
                for partner in partners
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
