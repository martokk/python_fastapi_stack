from typing import Awaitable, Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.types import ASGIApp

from app.utils.templates import get_template_context
from app.views.deps import get_current_user, get_db


class TemplateContextMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        db_generator = get_db()
        db = next(db_generator)
        try:
            # Try to get current user
            try:
                current_user = await get_current_user(request)
            except:
                current_user = None

            # Get template context
            context = await get_template_context(
                request=request,
                session=db,
                current_user=current_user,
            )
            # Store the context in request state
            request.state.template_context = context
            # Call next middleware/route
            response = await call_next(request)
            return response
        finally:
            db.close()
            db_generator.close()
