from app import models

from .base import BaseCRUD


class BoardMemberCRUD(
    BaseCRUD[models.BoardMember, models.BoardMemberCreate, models.BoardMemberUpdate]
):
    pass


board_member = BoardMemberCRUD(model=models.BoardMember)
