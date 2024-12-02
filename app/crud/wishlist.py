from app import models

from .base import BaseCRUD


class WishlistCRUD(BaseCRUD[models.Wishlist, models.WishlistCreate, models.WishlistUpdate]):
    pass


wishlist = WishlistCRUD(model=models.Wishlist)
