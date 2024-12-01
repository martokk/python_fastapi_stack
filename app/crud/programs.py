from app import models

from .base import BaseCRUD


class ProgramsCRUD(BaseCRUD[models.Programs, models.ProgramsCreate, models.ProgramsUpdate]):
    pass


programs = ProgramsCRUD(model=models.Programs)
