from pydantic import field_validator
from datetime import date
from typing import Any


class TimelineValidator:
    @field_validator("date")
    @classmethod
    def validate_date(cls, v: date) -> date:
        if v > date.today():
            raise ValueError("Date cannot be in the future")
        return v


class StaffValidator:
    @field_validator("photo_url")
    @classmethod
    def validate_photo_url(cls, v: str) -> str:
        if not v.startswith("/static/uploads/"):
            raise ValueError("Invalid photo URL")
        return v
