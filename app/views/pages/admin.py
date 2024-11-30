from typing import Any, Optional

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select

from app.models.admin import UserPermissions
from app.models.partners import Partner
from app.models.people import BoardMember, Staff
from app.models.programs import FAQ, Program
from app.models.stats import Stats
from app.models.timeline import Timeline
from app.models.user import User
from app.models.variables import Variables
from app.models.wishlist import Wishlist
from app.utils.templates import get_template_context, templates
from app.views.deps import get_current_user, get_db

router = APIRouter(
    dependencies=[Depends(get_current_user)],
)


async def get_admin_context(
    request: Request,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> dict[str, Any]:
    """Get admin template context with user permissions"""
    context = await get_template_context(request, current_user, session)

    # Get user permissions
    permissions = session.exec(
        select(UserPermissions).where(UserPermissions.user_id == current_user.id)
    ).first()

    if not permissions:
        permissions = UserPermissions(user_id=current_user.id)
        session.add(permissions)
        session.commit()

    context["user_permissions"] = permissions
    return context


@router.get("", response_class=HTMLResponse)
async def admin_home(
    request: Request,
    context: dict[str, Any] = Depends(get_admin_context),
) -> HTMLResponse:
    """Admin home page"""
    return templates.TemplateResponse("admin/home.html", context)


@router.get("/variables", response_class=HTMLResponse)
async def admin_variables(
    request: Request,
    context: dict[str, Any] = Depends(get_admin_context),
    session: Session = Depends(get_db),
) -> HTMLResponse:
    """Admin variables page"""
    if not context["user_permissions"].webpage_variables:
        return templates.TemplateResponse("admin/403.html", context, status_code=403)

    variables = session.exec(select(Variables)).first()
    if not variables:
        variables = Variables(
            phone="",
            email="",
            service_address="",
            mailing_address="",
            location="",
        )
        session.add(variables)
        session.commit()

    context["variables"] = variables
    return templates.TemplateResponse("admin/variables.html", context)


@router.get("/wishlist", response_class=HTMLResponse)
async def admin_wishlist(
    request: Request,
    context: dict[str, Any] = Depends(get_admin_context),
    session: Session = Depends(get_db),
) -> HTMLResponse:
    """Admin wishlist page"""
    if not context["user_permissions"].wish_list:
        return templates.TemplateResponse("admin/403.html", context, status_code=403)

    wishlist = session.exec(select(Wishlist)).first()
    if not wishlist:
        wishlist = Wishlist()
        session.add(wishlist)
        session.commit()

    context["wishlist"] = wishlist
    return templates.TemplateResponse("admin/wishlist.html", context)


@router.get("/stats", response_class=HTMLResponse)
async def admin_stats(
    request: Request,
    context: dict[str, Any] = Depends(get_admin_context),
    session: Session = Depends(get_db),
) -> HTMLResponse:
    """Admin stats page"""
    if not context["user_permissions"].stats:
        return templates.TemplateResponse("admin/403.html", context, status_code=403)

    stats = session.exec(select(Stats)).first()
    if not stats:
        stats = Stats()
        session.add(stats)
        session.commit()

    context["stats"] = stats
    return templates.TemplateResponse("admin/stats.html", context)


@router.get("/timeline", response_class=HTMLResponse)
async def admin_timeline(
    request: Request,
    context: dict[str, Any] = Depends(get_admin_context),
    session: Session = Depends(get_db),
) -> HTMLResponse:
    """Admin timeline page"""
    if not context["user_permissions"].timeline:
        return templates.TemplateResponse("admin/403.html", context, status_code=403)

    timeline = session.exec(select(Timeline).order_by(Timeline.date)).all()
    context["timeline"] = timeline
    return templates.TemplateResponse("admin/timeline.html", context)


@router.get("/programs", response_class=HTMLResponse)
async def admin_programs(
    request: Request,
    context: dict[str, Any] = Depends(get_admin_context),
    session: Session = Depends(get_db),
) -> HTMLResponse:
    """Admin programs page"""
    if not context["user_permissions"].faq:
        return templates.TemplateResponse("admin/403.html", context, status_code=403)

    programs = session.exec(select(Program)).all()
    context["programs"] = programs
    return templates.TemplateResponse("admin/programs.html", context)


@router.get("/faq", response_class=HTMLResponse)
async def admin_faq(
    request: Request,
    program_id: Optional[int] = None,
    context: dict[str, Any] = Depends(get_admin_context),
    session: Session = Depends(get_db),
) -> HTMLResponse:
    """Admin FAQ page"""
    if not context["user_permissions"].faq:
        return templates.TemplateResponse("admin/403.html", context, status_code=403)

    # Get all programs for the dropdown
    programs = session.exec(select(Program)).all()
    context["programs"] = programs

    # Get FAQs, filtered by program if specified
    query = select(FAQ).order_by(FAQ.order)
    if program_id:
        query = query.where(FAQ.program_id == program_id)
    faqs = session.exec(query).all()

    context["faqs"] = faqs
    context["selected_program"] = program_id
    return templates.TemplateResponse("admin/faq.html", context)


@router.get("/staff", response_class=HTMLResponse)
async def admin_staff(
    request: Request,
    context: dict[str, Any] = Depends(get_admin_context),
    session: Session = Depends(get_db),
) -> HTMLResponse:
    """Admin staff page"""
    if not context["user_permissions"].staff:
        return templates.TemplateResponse("admin/403.html", context, status_code=403)

    staff = session.exec(select(Staff)).all()
    context["staff"] = staff
    return templates.TemplateResponse("admin/staff.html", context)


@router.get("/board", response_class=HTMLResponse)
async def admin_board(
    request: Request,
    context: dict[str, Any] = Depends(get_admin_context),
    session: Session = Depends(get_db),
) -> HTMLResponse:
    """Admin board page"""
    if not context["user_permissions"].board_members:
        return templates.TemplateResponse("admin/403.html", context, status_code=403)

    board_members = session.exec(select(BoardMember)).all()
    context["board_members"] = board_members
    return templates.TemplateResponse("admin/board.html", context)


@router.get("/partners", response_class=HTMLResponse)
async def admin_partners(
    request: Request,
    context: dict[str, Any] = Depends(get_admin_context),
    session: Session = Depends(get_db),
) -> HTMLResponse:
    """Admin partners page"""
    if not context["user_permissions"].partners:
        return templates.TemplateResponse("admin/403.html", context, status_code=403)

    partners = session.exec(select(Partner)).all()
    context["partners"] = partners
    return templates.TemplateResponse("admin/partners.html", context)


@router.get("/users", response_class=HTMLResponse)
async def admin_users(
    request: Request,
    context: dict[str, Any] = Depends(get_admin_context),
    session: Session = Depends(get_db),
) -> HTMLResponse:
    """Admin users page"""
    if not context["user_permissions"].users:
        return templates.TemplateResponse("admin/403.html", context, status_code=403)

    users = session.exec(select(User)).all()
    context["users"] = users
    return templates.TemplateResponse("admin/users.html", context)


@router.get("/backup", response_class=HTMLResponse)
async def admin_backup(
    request: Request,
    context: dict[str, Any] = Depends(get_admin_context),
) -> HTMLResponse:
    """Admin backup page"""
    if not context["user_permissions"].users:  # Using users permission for backup
        return templates.TemplateResponse("admin/403.html", context, status_code=403)

    return templates.TemplateResponse("admin/backup.html", context)
