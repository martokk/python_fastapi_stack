from typing import Any, List, Optional

from pydantic import model_validator
from sqlmodel import Field, Relationship, SQLModel

from app.core.uuid import generate_uuid_from_string


class ProgramBase(SQLModel):
    id: str = Field(
        primary_key=True,
        index=True,
        nullable=False,
        default=None,
    )
    name: str = Field(index=True)


class Program(ProgramBase, table=True):

    faqs: List["FAQ"] = Relationship(
        back_populates="program", sa_relationship_kwargs={"cascade": "all, delete"}
    )


class ProgramCreate(ProgramBase):
    @model_validator(mode="before")
    @classmethod
    def set_pre_validation_defaults(cls, values: dict[str, Any]) -> dict[str, Any]:
        values["id"] = values.get("id", generate_uuid_from_string(string=values["name"]))
        return values


class ProgramUpdate(SQLModel):
    name: Optional[str] = None


class ProgramRead(ProgramBase):
    pass


class FAQ(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    program_id: Optional[str] = Field(default=None, foreign_key="program.id")
    order: int = Field(default=0)
    question: str
    answer: str

    # Relationships
    program: Optional[Program] = Relationship(back_populates="faqs")
