from typing import Optional

from datetime import datetime

from sqlmodel import Field, Session, SQLModel


class FailedLogin(SQLModel, table=True):
    __tablename__ = "failed_logins"

    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    username: str
    ip_address: str
    user_agent: str
    additional_info: str = Field(default="")


def log_failed_login(
    db: Session, username: str, ip_address: str, user_agent: str, additional_info: str = ""
):
    failed_login = FailedLogin(
        username=username,
        ip_address=ip_address,
        user_agent=user_agent,
        additional_info=additional_info,
    )
    db.add(failed_login)
    db.commit()
