from typing import Optional

from sqlmodel import Field, SQLModel


class WishlistBase(SQLModel):
    content: str = Field(
        default="", description="HTML content from the WYSIWYG editor", nullable=False
    )


class Wishlist(WishlistBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)


class WishlistCreate(WishlistBase):
    pass


class WishlistUpdate(WishlistBase):
    pass


class WishlistRead(Wishlist):
    pass
