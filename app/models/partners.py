from typing import Optional

from sqlmodel import Field, SQLModel


class PartnerBase(SQLModel):
    name: str = Field(index=True)
    url: str
    logo_url: str | None = None
    order: int = Field(default=0)


class Partner(PartnerBase, table=True):
    __tablename__ = "partners"

    id: Optional[int] = Field(default=None, primary_key=True)


class PartnerCreate(PartnerBase):
    pass


class PartnerUpdate(SQLModel):
    name: str | None = None
    url: str | None = None
    logo_url: str | None = None
    order: int | None = None


class PartnerRead(PartnerBase):
    id: int
