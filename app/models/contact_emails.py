from typing import Optional

from datetime import datetime

from sqlmodel import Field, SQLModel


class ContactEmailsBase(SQLModel):
    name: str = Field(...)
    email: str = Field(...)
    subject: str = Field(...)
    message: str = Field(...)
    sent: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ContactEmails(ContactEmailsBase, table=True):
    __tablename__ = "contact_emails"

    id: Optional[int] = Field(default=None, primary_key=True)


class ContactEmailsCreate(ContactEmailsBase):
    pass


class ContactEmailsUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    subject: Optional[str] = None
    message: Optional[str] = None
    sent: Optional[bool] = None
