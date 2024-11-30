from sqlmodel import SQLModel
from typing import Any


class BaseModel(SQLModel):
    """Base model that sets table name automatically"""

    @property
    def __tablename__(cls) -> str:  # type: ignore
        """Return lowercase class name as table name."""
        return cls.__class__.__name__.lower()
