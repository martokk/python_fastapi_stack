from typing import Any

from sqlmodel import Session, select

from app import models
from app.core import security

from .base import BaseCRUD


class UserCRUD(BaseCRUD[models.User, models.UserCreate, models.UserUpdate]):
    async def create_with_password(
        self, db: Session, *, obj_in: models.UserCreateWithPassword
    ) -> models.User:
        """
        Create a new user by generating a hashed password from the provided password.

        Args:
            db (Session): The database session.
            obj_in (models.UserCreateWithPassword): The user to create.

        Returns:
            models.User: The created user.
        """
        obj_in_data = obj_in.model_dump(exclude_unset=True)
        obj_in_data["hashed_password"] = security.get_password_hash(obj_in_data["password"])
        del obj_in_data["password"]

        out_obj = models.UserCreate(**obj_in_data)
        return await self.create(db, obj_in=out_obj)

    async def authenticate(
        self, db: Session, *, username: str, password: str
    ) -> models.User | None:
        """
        Authenticate a user by checking the provided password against the hashed password.

        Args:
            db (Session): The database session.
            username (str): The username to authenticate.
            password (str): The password to authenticate.

        Returns:
            models.User | None: The authenticated user or None if the user does not exist or
                the password is incorrect.
        """
        _user = await self.get_or_none(db, username=username)
        if not _user:
            return None
        if not security.verify_password(
            plain_password=password, hashed_password=_user.hashed_password
        ):
            return None
        return _user

    def is_active(self, _user: models.User) -> bool:
        return _user.is_active

    def is_superuser(self, *, user_: models.User) -> bool:
        return user_.is_superuser

    def get_password_hash(self, password: str) -> str:
        """Get password hash."""
        return security.get_password_hash(password)

    async def create_with_permissions(
        self, db: Session, *, obj_in: models.UserCreateWithPassword
    ) -> models.User:
        """Create a new user with default permissions."""
        # Check if username exists
        existing_user = await self.get_or_none(db, username=obj_in.username)
        if existing_user:
            raise ValueError("username:This username is already taken")

        # Check if email exists
        existing_email = await self.get_or_none(db, email=obj_in.email)
        if existing_email:
            raise ValueError("email:This email is already registered")

        user = await self.create_with_password(db=db, obj_in=obj_in)

        # Create default permissions for the user
        permissions = models.UserPermissions(user_id=user.id)
        db.add(permissions)
        db.commit()

        return user

    async def get_permissions(self, db: Session, *, user_id: str) -> models.UserPermissions | None:
        """Get user permissions."""
        return db.exec(
            select(models.UserPermissions).where(models.UserPermissions.user_id == user_id)
        ).first()

    async def update_permissions(
        self, db: Session, *, user_id: str, permissions_data: dict[str, bool]
    ) -> models.UserPermissions:
        """Update user permissions."""
        permissions = await self.get_permissions(db=db, user_id=user_id)
        if not permissions:
            raise ValueError(f"No permissions found for user {user_id}")

        for field, value in permissions_data.items():
            setattr(permissions, field, value)

        db.add(permissions)
        db.commit()
        db.refresh(permissions)
        return permissions

    async def get_non_superusers(self, db: Session) -> list[models.User]:
        """Get all non-superuser users."""
        return db.exec(
            select(models.User).where(models.User.is_superuser == False)  # noqa: E712
        ).all()

    async def remove(self, db: Session, *, id: str) -> models.User:
        """Remove a user and their permissions."""
        # First delete the user's permissions
        permissions = await self.get_permissions(db=db, user_id=id)
        if permissions:
            db.delete(permissions)
            db.commit()

        # Then delete the user
        user = await self.get(db=db, id=id)
        db.delete(user)
        db.commit()
        return user


user = UserCRUD(model=models.User)
