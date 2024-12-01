from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.user import User


class UserPermissions(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    webpage_variables: bool = Field(default=False)
    wish_list: bool = Field(default=False)
    staff: bool = Field(default=False)
    board_members: bool = Field(default=False)
    stats: bool = Field(default=False)
    timeline: bool = Field(default=False)
    partners: bool = Field(default=False)
    users: bool = Field(default=False)
    faq: bool = Field(default=False)
    programs: bool = Field(default=False)
    backup: bool = Field(default=False)

    # Relationship
    if TYPE_CHECKING:
        user: "User" = None
    else:
        user: "User" = Relationship(back_populates="permissions")
