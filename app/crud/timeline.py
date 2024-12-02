from app import models

from .base import BaseCRUD


class TimelineCRUD(BaseCRUD[models.Timeline, models.Timeline, models.Timeline]):
    pass


timeline = TimelineCRUD(model=models.Timeline)
