from typing import Any

from sqlalchemy.engine.base import Engine
from sqlmodel import Session, SQLModel, select

from app import crud, logger, models, settings
from app.db.session import engine as _engine
from app.models.admin import UserPermissions


async def create_all(engine: Engine = _engine, sqlmodel_create_all: bool = False) -> None:
    """
    Create all tables in the database.

    Args:
        engine (Engine): database engine.
        sqlmodel_create_all (bool): whether to create all tables using SQLModel.

    Returns:
        None
    """
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line or use
    # sqlmodel_create_all=True
    if sqlmodel_create_all:
        logger.debug("Initializing database...")
        SQLModel.metadata.create_all(bind=engine)
    return


async def init_initial_data(db: Session, **kwargs: Any) -> None:
    """Initialize database with initial data"""

    await create_all(**kwargs)

    superuser = await crud.user.get_or_none(db=db, username=settings.FIRST_SUPERUSER_USERNAME)
    if not superuser:
        user_create = models.UserCreateWithPassword(
            username=settings.FIRST_SUPERUSER_USERNAME,
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        superuser = await crud.user.create_with_password(db=db, obj_in=user_create)

    # Check and set full privileges for superuser
    permissions = db.exec(
        select(UserPermissions).where(UserPermissions.user_id == superuser.id)
    ).first()

    if not permissions:
        # Create new permissions with all privileges
        permissions = UserPermissions(
            user_id=superuser.id,
            webpage_variables=True,
            wish_list=True,
            staff=True,
            board_members=True,
            stats=True,
            timeline=True,
            partners=True,
            users=True,
            faq=True,
        )
        db.add(permissions)
    else:
        # Update existing permissions to ensure all are True
        permissions.webpage_variables = True
        permissions.wish_list = True
        permissions.staff = True
        permissions.board_members = True
        permissions.stats = True
        permissions.timeline = True
        permissions.partners = True
        permissions.users = True
        permissions.faq = True

    db.commit()
