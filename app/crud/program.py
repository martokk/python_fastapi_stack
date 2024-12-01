from app import models

from .base import BaseCRUD


class ProgramCRUD(BaseCRUD[models.Program, models.ProgramCreate, models.ProgramUpdate]):
    pass


program = ProgramCRUD(model=models.Program)
