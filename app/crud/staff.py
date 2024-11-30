from app import models

from .base import BaseCRUD


class StaffCRUD(BaseCRUD[models.Staff, models.StaffCreate, models.StaffUpdate]):
    pass


staff = StaffCRUD(model=models.Staff)
