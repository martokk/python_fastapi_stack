from typing import Optional

from sqlmodel import Field, SQLModel


class StaffBase(SQLModel):
    name: str = Field(index=True)
    position: str
    photo_url: str | None = None


class Staff(SQLModel, table=True):
    __tablename__ = "staff"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    position: str
    photo_url: str | None = None


class StaffCreate(SQLModel):
    name: str
    position: str
    photo_url: str | None = None


class StaffUpdate(SQLModel):
    name: str | None = None
    position: str | None = None
    photo_url: str | None = None


class StaffRead(SQLModel):
    id: int
    name: str
    position: str
    photo_url: str | None = None


class BoardMemberBase(SQLModel):
    name: str = Field(index=True)
    position: str
    description: str


class BoardMember(SQLModel, table=True):
    __tablename__ = "board_members"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    position: str
    description: str


class BoardMemberCreate(SQLModel):
    name: str
    position: str
    description: str


class BoardMemberUpdate(SQLModel):
    name: str | None = None
    position: str | None = None
    description: str | None = None


class BoardMemberRead(SQLModel):
    id: int
    name: str
    position: str
    description: str
