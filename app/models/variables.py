from typing import Optional

from sqlmodel import Field, SQLModel


class VariablesBase(SQLModel):
    phone: str = Field(default="")
    email: str = Field(default="")
    service_address_1: str = Field(default="")
    service_address_2: str = Field(default="")
    mailing_address_1: str = Field(default="")
    mailing_address_2: str = Field(default="")
    location: str = Field(default="")

    @property
    def service_address(self) -> str:
        """Get the full service address."""
        if self.service_address_2:
            return f"{self.service_address_1}, {self.service_address_2}"
        return self.service_address_1

    @property
    def mailing_address(self) -> str:
        """Get the full mailing address."""
        if self.mailing_address_2:
            return f"{self.mailing_address_1}, {self.mailing_address_2}"
        return self.mailing_address_1


class Variables(VariablesBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class VariablesCreate(VariablesBase):
    pass


class VariablesUpdate(SQLModel):
    phone: Optional[str] = None
    email: Optional[str] = None
    service_address_1: Optional[str] = None
    service_address_2: Optional[str] = None
    mailing_address_1: Optional[str] = None
    mailing_address_2: Optional[str] = None
    location: Optional[str] = None


class VariablesRead(VariablesBase):
    id: int
