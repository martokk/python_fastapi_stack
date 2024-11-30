from typing import Optional

from datetime import date

from sqlmodel import Field, SQLModel


class Timeline(SQLModel, table=True):
    __tablename__ = "timeline"

    id: Optional[int] = Field(default=None, primary_key=True)
    date: date = Field(index=True)
    title: str
    description: str
