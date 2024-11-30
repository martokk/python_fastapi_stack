from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, SQLModel

if TYPE_CHECKING:
    from .faq import FAQ


class Program(SQLModel, table=True):
    __tablename__ = "programs"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str

    if TYPE_CHECKING:
        faqs: List["FAQ"] = []


class FAQ(SQLModel, table=True):
    __tablename__ = "faq"

    id: Optional[int] = Field(default=None, primary_key=True)
    program_id: Optional[int] = Field(default=None, foreign_key="programs.id")
    order: int
    question: str
    answer: str
