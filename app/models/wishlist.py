from typing import Optional

from sqlmodel import Field, SQLModel


class Wishlist(SQLModel, table=True):
    __tablename__ = "wishlist"

    id: Optional[int] = Field(default=None, primary_key=True)
    wishlist: str = Field(default="")  # This will store the WYSIWYG content
