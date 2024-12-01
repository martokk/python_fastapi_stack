from typing import TYPE_CHECKING, Any, List, Optional

from pydantic import model_validator
from sqlmodel import Field, Relationship, SQLModel

from app.core.uuid import generate_uuid_from_string

if TYPE_CHECKING:
    from .faq import FAQ


class ProgramBase(SQLModel):
    id: str = Field(
        primary_key=True,
        index=True,
        nullable=False,
        default=None,
    )
    name: str = Field(index=True)


class Program(ProgramBase, table=True):
    if TYPE_CHECKING:
        faqs: List["FAQ"] = []
    else:
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
