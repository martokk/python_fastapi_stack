from sqlmodel import Session, select

from app import models

from .base import BaseCRUD


class VariablesCRUD(BaseCRUD[models.Variables, models.VariablesCreate, models.VariablesUpdate]):
    pass


variables = VariablesCRUD(model=models.Variables)
