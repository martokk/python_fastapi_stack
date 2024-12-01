from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .programs import Program


class FAQ(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    program_id: Optional[str] = Field(default=None, foreign_key="program.id")
    order: int = Field(default=0)
    question: str
    answer: str

    if TYPE_CHECKING:
        program: Optional["Program"] = None
    else:
        program: Optional["Program"] = Relationship(back_populates="faqs")


class FAQCreate(SQLModel):
    program_id: str
    question: str
    answer: str


class FAQUpdate(SQLModel):
    program_id: Optional[str] = None
    question: Optional[str] = None
    answer: Optional[str] = None


class FAQRead(SQLModel):
    id: int
    program_id: str
    order: int
    question: str
    answer: str


class FAQOrderUpdate(SQLModel):
    program_id: str
    faq_orders: List[dict[str, int]]  # List of {id: order} pairs
