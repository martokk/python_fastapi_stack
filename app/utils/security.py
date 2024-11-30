from typing import Optional

from datetime import datetime

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer
from jose import jwt
import secrets
from sqlmodel import Session, select
from fastapi.responses import JSONResponse
import time
from collections import defaultdict

from app.database import get_session
from app.models.admin import UserPermissions
from app.models.user import User  # assuming this exists
from app.utils.auth import get_current_user  # assuming this exists


class FailedLogin(SQLModel, table=True):
    __tablename__ = "failed_logins"

    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    username: str
    ip_address: str
    user_agent: str
    additional_info: str = Field(default="")


class PermissionChecker:
    def __init__(self, permission_name: str):
        self.permission_name = permission_name

    async def __call__(
        self,
        current_user: User = Depends(get_current_user),
        session: Session = Depends(get_session),
    ) -> User:
        # Query user permissions
        stmt = select(UserPermissions).where(UserPermissions.user_id == current_user.id)
        result = session.exec(stmt).first()

        if not result:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="No permissions found for user"
            )

        # Check if user has the required permission
        if not getattr(result, self.permission_name, False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User does not have {self.permission_name} permission",
            )

        return current_user


# Create permission checker instances for each permission type
require_webpage_variables = PermissionChecker("webpage_variables")
require_wish_list = PermissionChecker("wish_list")
require_staff = PermissionChecker("staff")
require_board_members = PermissionChecker("board_members")
require_stats = PermissionChecker("stats")
require_timeline = PermissionChecker("timeline")
require_partners = PermissionChecker("partners")
require_users = PermissionChecker("users")
require_faq = PermissionChecker("faq")


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


csrf_token_header = "X-CSRF-Token"
security = HTTPBearer()


def generate_csrf_token() -> str:
    return secrets.token_urlsafe(32)


async def verify_csrf_token(request: Request):
    csrf_token = request.headers.get(csrf_token_header)
    session_token = request.session.get("csrf_token")

    if not csrf_token or not session_token or csrf_token != session_token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid CSRF token")


# Simple in-memory rate limiting
RATE_LIMIT_DURATION = 60  # seconds
MAX_REQUESTS = 100  # requests per duration
request_counts = defaultdict(list)


async def rate_limit(request: Request):
    client_ip = request.client.host
    now = time.time()

    # Clean old requests
    request_counts[client_ip] = [
        t for t in request_counts[client_ip] if now - t < RATE_LIMIT_DURATION
    ]

    if len(request_counts[client_ip]) >= MAX_REQUESTS:
        return JSONResponse(status_code=429, content={"detail": "Too many requests"})

    request_counts[client_ip].append(now)
