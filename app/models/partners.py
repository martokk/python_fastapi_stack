from typing import Optional

from sqlmodel import Field, SQLModel


class Partner(SQLModel, table=True):
    __tablename__ = "partners"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    url: str
    logo_url: str
