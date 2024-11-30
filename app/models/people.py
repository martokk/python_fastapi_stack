from typing import Optional

from sqlmodel import Field, SQLModel


class Staff(SQLModel, table=True):
    __tablename__ = "staff"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    position: str
    photo_url: str


class BoardMember(SQLModel, table=True):
    __tablename__ = "board_members"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    position: str
    description: str
