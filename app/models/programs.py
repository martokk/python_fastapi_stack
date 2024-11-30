from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship

from app.models.base import BaseModel


class Program(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str = Field(default="")

    # Relationships
    faqs: List["FAQ"] = Relationship(back_populates="program")


class FAQ(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    program_id: Optional[int] = Field(default=None, foreign_key="program.id")
    order: int = Field(default=0)
    question: str
    answer: str

    # Relationships
    program: Optional[Program] = Relationship(back_populates="faqs")
