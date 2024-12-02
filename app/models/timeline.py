from typing import Optional

from datetime import date as datetime_date

from sqlmodel import Field, SQLModel

from app.models.base import BaseModel


class Timeline(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: datetime_date = Field(...)
    title: str = Field(...)
    description: str = Field(...)
