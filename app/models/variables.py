from typing import Optional

from sqlmodel import Field, SQLModel


class Variables(SQLModel, table=True):
    __tablename__ = "user_variables"

    id: Optional[int] = Field(default=None, primary_key=True)
    phone: str = Field(index=True)
    email: str = Field(index=True)
    service_address: str
    mailing_address: str
    location: str  # Coordinates for service location
