from typing import Optional

from sqlmodel import Field, SQLModel


class UserPermissions(SQLModel, table=True):
    __tablename__ = "user_permissions"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    webpage_variables: bool = Field(default=False)
    wish_list: bool = Field(default=False)
    staff: bool = Field(default=False)
    board_members: bool = Field(default=False)
    stats: bool = Field(default=False)
    timeline: bool = Field(default=False)
    partners: bool = Field(default=False)
    users: bool = Field(default=False)
    faq: bool = Field(default=False)
