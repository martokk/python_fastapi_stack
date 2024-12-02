from typing import Optional

from sqlmodel import Field, SQLModel


class StaffBase(SQLModel):
    name: str = Field(index=True)
    position: str
    photo_url: str | None = None
    order: int = Field(default=0)


class Staff(SQLModel, table=True):
    __tablename__ = "staff"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    position: str
    photo_url: str | None = None
    order: int = Field(default=0, index=True)


class StaffCreate(SQLModel):
    name: str
    position: str
    photo_url: str | None = None
    order: int = Field(default=0)


class StaffUpdate(SQLModel):
    name: str | None = None
    position: str | None = None
    photo_url: str | None = None
    order: int | None = None


class StaffRead(SQLModel):
    id: int
    name: str
    position: str
    photo_url: str | None = None
    order: int


class BoardMemberBase(SQLModel):
    name: str = Field(index=True)
    position: str
    description: str
    order: int = Field(default=0)


class BoardMember(SQLModel, table=True):
    __tablename__ = "board_members"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    position: str
    description: str
    order: int = Field(default=0, index=True)


class BoardMemberCreate(SQLModel):
    name: str
    position: str
    description: str
    order: int = Field(default=0)


class BoardMemberUpdate(SQLModel):
    name: str | None = None
    position: str | None = None
    description: str | None = None
    order: int | None = None


class BoardMemberRead(SQLModel):
    id: int
    name: str
    position: str
    description: str
    order: int
