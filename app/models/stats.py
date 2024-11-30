from typing import Optional

from sqlmodel import Field, SQLModel


class Stats(SQLModel, table=True):
    __tablename__ = "stats"

    id: Optional[int] = Field(default=None, primary_key=True)
    food_boxes: int = Field(default=0)
    meals_served: int = Field(default=0)
    showers: int = Field(default=0)
    housing_intake: int = Field(default=0)
    survival_food_bags: int = Field(default=0)
