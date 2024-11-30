from typing import List, Optional

import json

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlmodel import Session, select

from app.database import get_session
from app.models.admin import UserPermissions
from app.models.partners import Partner
from app.models.people import BoardMember, Staff
from app.models.programs import FAQ, Program
from app.models.stats import Stats
from app.models.timeline import Timeline
from app.models.user import User
from app.models.variables import Variables
from app.models.wishlist import Wishlist
from app.utils.security import (
    require_board_members,
    require_faq,
    require_partners,
    require_staff,
    require_stats,
    require_timeline,
    require_users,
    require_webpage_variables,
    require_wish_list,
)
from app.utils.upload import save_upload

router = APIRouter(prefix="/admin", tags=["admin"])


# Variables Routes
@router.get("/variables", response_model=Variables)
async def get_variables(
    current_user=Depends(require_webpage_variables), session: Session = Depends(get_session)
):
    variables = session.exec(select(Variables)).first()
    if not variables:
        variables = Variables()
        session.add(variables)
        session.commit()
    return variables


@router.put("/variables", response_model=Variables)
async def update_variables(
    variables: Variables,
    current_user=Depends(require_webpage_variables),
    session: Session = Depends(get_session),
):
    db_variables = session.exec(select(Variables)).first()
    if not db_variables:
        db_variables = Variables()
        session.add(db_variables)

    for key, value in variables.dict(exclude_unset=True).items():
        setattr(db_variables, key, value)

    session.commit()
    session.refresh(db_variables)
    return db_variables


# Wishlist Routes
@router.get("/wishlist", response_model=Wishlist)
async def get_wishlist(
    current_user=Depends(require_wish_list), session: Session = Depends(get_session)
):
    wishlist = session.exec(select(Wishlist)).first()
    if not wishlist:
        wishlist = Wishlist()
        session.add(wishlist)
        session.commit()
    return wishlist


@router.put("/wishlist", response_model=Wishlist)
async def update_wishlist(
    wishlist: Wishlist,
    current_user=Depends(require_wish_list),
    session: Session = Depends(get_session),
):
    db_wishlist = session.exec(select(Wishlist)).first()
    if not db_wishlist:
        db_wishlist = Wishlist()
        session.add(db_wishlist)

    db_wishlist.wishlist = wishlist.wishlist
    session.commit()
    session.refresh(db_wishlist)
    return db_wishlist


# Staff Routes
@router.get("/staff", response_model=List[Staff])
async def get_staff(current_user=Depends(require_staff), session: Session = Depends(get_session)):
    return session.exec(select(Staff)).all()


@router.post("/staff", response_model=Staff)
async def create_staff(
    name: str,
    position: str,
    photo: UploadFile = File(...),
    current_user=Depends(require_staff),
    session: Session = Depends(get_session),
):
    photo_url = await save_upload(photo, "staff_photos")
    staff = Staff(name=name, position=position, photo_url=photo_url)
    session.add(staff)
    session.commit()
    session.refresh(staff)
    return staff


@router.put("/staff/{staff_id}", response_model=Staff)
async def update_staff(
    staff_id: int,
    name: str,
    position: str,
    photo: Optional[UploadFile] = File(None),
    current_user=Depends(require_staff),
    session: Session = Depends(get_session),
):
    staff = session.get(Staff, staff_id)
    if not staff:
        raise HTTPException(status_code=404, detail="Staff member not found")

    staff.name = name
    staff.position = position

    if photo:
        photo_url = await save_upload(photo, "staff_photos")
        staff.photo_url = photo_url

    session.commit()
    session.refresh(staff)
    return staff


@router.delete("/staff/{staff_id}")
async def delete_staff(
    staff_id: int, current_user=Depends(require_staff), session: Session = Depends(get_session)
):
    staff = session.get(Staff, staff_id)
    if not staff:
        raise HTTPException(status_code=404, detail="Staff member not found")

    session.delete(staff)
    session.commit()
    return {"ok": True}


# Board Members Routes
@router.get("/board-members", response_model=List[BoardMember])
async def get_board_members(
    current_user=Depends(require_board_members), session: Session = Depends(get_session)
):
    return session.exec(select(BoardMember)).all()


@router.post("/board-members", response_model=BoardMember)
async def create_board_member(
    board_member: BoardMember,
    current_user=Depends(require_board_members),
    session: Session = Depends(get_session),
):
    session.add(board_member)
    session.commit()
    session.refresh(board_member)
    return board_member


@router.put("/board-members/{member_id}", response_model=BoardMember)
async def update_board_member(
    member_id: int,
    board_member: BoardMember,
    current_user=Depends(require_board_members),
    session: Session = Depends(get_session),
):
    db_member = session.get(BoardMember, member_id)
    if not db_member:
        raise HTTPException(status_code=404, detail="Board member not found")

    for key, value in board_member.dict(exclude_unset=True).items():
        setattr(db_member, key, value)

    session.commit()
    session.refresh(db_member)
    return db_member


@router.delete("/board-members/{member_id}")
async def delete_board_member(
    member_id: int,
    current_user=Depends(require_board_members),
    session: Session = Depends(get_session),
):
    member = session.get(BoardMember, member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Board member not found")

    session.delete(member)
    session.commit()
    return {"ok": True}


# Stats Routes
@router.get("/stats", response_model=Stats)
async def get_stats(current_user=Depends(require_stats), session: Session = Depends(get_session)):
    stats = session.exec(select(Stats)).first()
    if not stats:
        stats = Stats()
        session.add(stats)
        session.commit()
    return stats


@router.put("/stats", response_model=Stats)
async def update_stats(
    stats: Stats,
    current_user=Depends(require_stats),
    session: Session = Depends(get_session),
):
    db_stats = session.exec(select(Stats)).first()
    if not db_stats:
        db_stats = Stats()
        session.add(db_stats)

    for key, value in stats.dict(exclude_unset=True).items():
        setattr(db_stats, key, value)

    session.commit()
    session.refresh(db_stats)
    return db_stats


# Timeline Routes
@router.get("/timeline", response_model=List[Timeline])
async def get_timeline(
    current_user=Depends(require_timeline), session: Session = Depends(get_session)
):
    return session.exec(select(Timeline).order_by(Timeline.date.desc())).all()


@router.post("/timeline", response_model=Timeline)
async def create_timeline(
    timeline: Timeline,
    current_user=Depends(require_timeline),
    session: Session = Depends(get_session),
):
    session.add(timeline)
    session.commit()
    session.refresh(timeline)
    return timeline


@router.put("/timeline/{timeline_id}", response_model=Timeline)
async def update_timeline(
    timeline_id: int,
    timeline: Timeline,
    current_user=Depends(require_timeline),
    session: Session = Depends(get_session),
):
    db_timeline = session.get(Timeline, timeline_id)
    if not db_timeline:
        raise HTTPException(status_code=404, detail="Timeline entry not found")

    for key, value in timeline.dict(exclude_unset=True).items():
        setattr(db_timeline, key, value)

    session.commit()
    session.refresh(db_timeline)
    return db_timeline


@router.delete("/timeline/{timeline_id}")
async def delete_timeline(
    timeline_id: int,
    current_user=Depends(require_timeline),
    session: Session = Depends(get_session),
):
    timeline = session.get(Timeline, timeline_id)
    if not timeline:
        raise HTTPException(status_code=404, detail="Timeline entry not found")

    session.delete(timeline)
    session.commit()
    return {"ok": True}


# Partners Routes
@router.get("/partners", response_model=List[Partner])
async def get_partners(
    current_user=Depends(require_partners), session: Session = Depends(get_session)
):
    return session.exec(select(Partner)).all()


@router.post("/partners", response_model=Partner)
async def create_partner(
    name: str,
    url: str,
    logo: UploadFile = File(...),
    current_user=Depends(require_partners),
    session: Session = Depends(get_session),
):
    logo_url = await save_upload(logo, "partner_logos")
    partner = Partner(name=name, url=url, logo_url=logo_url)
    session.add(partner)
    session.commit()
    session.refresh(partner)
    return partner


@router.put("/partners/{partner_id}", response_model=Partner)
async def update_partner(
    partner_id: int,
    name: str,
    url: str,
    logo: Optional[UploadFile] = File(None),
    current_user=Depends(require_partners),
    session: Session = Depends(get_session),
):
    partner = session.get(Partner, partner_id)
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")

    partner.name = name
    partner.url = url

    if logo:
        logo_url = await save_upload(logo, "partner_logos")
        partner.logo_url = logo_url

    session.commit()
    session.refresh(partner)
    return partner


@router.delete("/partners/{partner_id}")
async def delete_partner(
    partner_id: int,
    current_user=Depends(require_partners),
    session: Session = Depends(get_session),
):
    partner = session.get(Partner, partner_id)
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")

    session.delete(partner)
    session.commit()
    return {"ok": True}


# Users Routes
@router.get("/users", response_model=List[User])
async def get_users(current_user=Depends(require_users), session: Session = Depends(get_session)):
    return session.exec(select(User)).all()


@router.get("/users/{user_id}/permissions", response_model=UserPermissions)
async def get_user_permissions(
    user_id: int,
    current_user=Depends(require_users),
    session: Session = Depends(get_session),
):
    permissions = session.exec(
        select(UserPermissions).where(UserPermissions.user_id == user_id)
    ).first()
    if not permissions:
        raise HTTPException(status_code=404, detail="Permissions not found")
    return permissions


@router.put("/users/{user_id}/permissions", response_model=UserPermissions)
async def update_user_permissions(
    user_id: int,
    permissions: UserPermissions,
    current_user=Depends(require_users),
    session: Session = Depends(get_session),
):
    db_permissions = session.exec(
        select(UserPermissions).where(UserPermissions.user_id == user_id)
    ).first()
    if not db_permissions:
        permissions.user_id = user_id
        session.add(permissions)
    else:
        for key, value in permissions.dict(exclude_unset=True).items():
            if key != "user_id":  # Don't update the user_id
                setattr(db_permissions, key, value)

    session.commit()
    session.refresh(db_permissions if db_permissions else permissions)
    return db_permissions if db_permissions else permissions


# Programs Routes
@router.get("/programs", response_model=List[Program])
async def get_programs(session: Session = Depends(get_session)):
    return session.exec(select(Program)).all()


@router.post("/programs", response_model=Program)
async def create_program(
    program: Program,
    current_user=Depends(require_faq),
    session: Session = Depends(get_session),
):
    session.add(program)
    session.commit()
    session.refresh(program)
    return program


@router.put("/programs/{program_id}", response_model=Program)
async def update_program(
    program_id: int,
    program: Program,
    current_user=Depends(require_faq),
    session: Session = Depends(get_session),
):
    db_program = session.get(Program, program_id)
    if not db_program:
        raise HTTPException(status_code=404, detail="Program not found")

    for key, value in program.dict(exclude_unset=True).items():
        setattr(db_program, key, value)

    session.commit()
    session.refresh(db_program)
    return db_program


@router.delete("/programs/{program_id}")
async def delete_program(
    program_id: int,
    current_user=Depends(require_faq),
    session: Session = Depends(get_session),
):
    program = session.get(Program, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    session.delete(program)
    session.commit()
    return {"ok": True}


# FAQ Routes
@router.get("/faq", response_model=List[FAQ])
async def get_faqs(
    program_id: Optional[int] = None,
    session: Session = Depends(get_session),
):
    query = select(FAQ)
    if program_id:
        query = query.where(FAQ.program_id == program_id)
    return session.exec(query.order_by(FAQ.order)).all()


@router.post("/faq", response_model=FAQ)
async def create_faq(
    faq: FAQ,
    current_user=Depends(require_faq),
    session: Session = Depends(get_session),
):
    session.add(faq)
    session.commit()
    session.refresh(faq)
    return faq


@router.put("/faq/{faq_id}", response_model=FAQ)
async def update_faq(
    faq_id: int,
    faq: FAQ,
    current_user=Depends(require_faq),
    session: Session = Depends(get_session),
):
    db_faq = session.get(FAQ, faq_id)
    if not db_faq:
        raise HTTPException(status_code=404, detail="FAQ not found")

    for key, value in faq.dict(exclude_unset=True).items():
        setattr(db_faq, key, value)

    session.commit()
    session.refresh(db_faq)
    return db_faq


@router.delete("/faq/{faq_id}")
async def delete_faq(
    faq_id: int,
    current_user=Depends(require_faq),
    session: Session = Depends(get_session),
):
    faq = session.get(FAQ, faq_id)
    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")

    session.delete(faq)
    session.commit()
    return {"ok": True}


# Backup Route
@router.get("/backup")
async def backup_database(
    current_user=Depends(require_users),  # Using users permission for backup
    session: Session = Depends(get_session),
):
    """Export all database tables as JSON"""
    data = {
        "variables": [v.dict() for v in session.exec(select(Variables)).all()],
        "wishlist": [w.dict() for w in session.exec(select(Wishlist)).all()],
        "staff": [s.dict() for s in session.exec(select(Staff)).all()],
        "board_members": [b.dict() for b in session.exec(select(BoardMember)).all()],
        "stats": [s.dict() for s in session.exec(select(Stats)).all()],
        "timeline": [t.dict() for t in session.exec(select(Timeline)).all()],
        "partners": [p.dict() for p in session.exec(select(Partner)).all()],
        "programs": [p.dict() for p in session.exec(select(Program)).all()],
        "faq": [f.dict() for f in session.exec(select(FAQ)).all()],
    }

    return data
