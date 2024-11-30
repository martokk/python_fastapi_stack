from typing import Any, Optional

from pydantic import model_validator
from sqlmodel import Field

from app.core.uuid import generate_uuid_random
from app.models.base import BaseModel


class Wishlist(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str = Field(
        default="", description="HTML content from the WYSIWYG editor", nullable=False
    )


class WishlistCreate(Wishlist):

    @model_validator(mode="before")
    @classmethod
    def set_pre_validation_defaults(cls, values: dict[str, Any]) -> dict[str, Any]:
        values["id"] = values.get("id", generate_uuid_random())
        return values


class WishlistUpdate(Wishlist):
    pass


class WishlistRead(Wishlist):
    pass
