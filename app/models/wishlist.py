from typing import Optional

from sqlmodel import Field

from app.models.base import BaseModel


class Wishlist(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    wishlist: str = Field(default="")  # This will store the WYSIWYG content
