from app import models

from .base import BaseCRUD


class StatsCRUD(BaseCRUD[models.Stats, models.Stats, models.Stats]):
    pass


stats = StatsCRUD(model=models.Stats)
