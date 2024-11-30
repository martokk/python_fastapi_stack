from fastapi import Request
from starlette.middleware.sessions import SessionMiddleware
import secrets


def setup_session_middleware(app):
    app.add_middleware(
        SessionMiddleware,
        secret_key=secrets.token_urlsafe(32),
        session_cookie="mission_session",
        max_age=3600,  # 1 hour
        same_site="lax",
        https_only=True,
    )
