from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session
from starlette.middleware.base import BaseHTTPMiddleware

from app import logger, models, settings, version
from app.api import deps
from app.core import notify
from app.db.init_db import init_initial_data
from app.middleware.error_handler import error_handler_middleware
from app.paths import STATIC_PATH
from app.routes.api import api_router
from app.routes.views import views_router

# Initialize FastAPI App
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=version,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    debug=settings.DEBUG,
)
app.include_router(api_router, prefix=settings.API_V1_PREFIX)
app.include_router(views_router)

# STATIC_PATH.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_PATH))


# Add the middleware to your FastAPI app
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware that adds security headers to all responses.

    This middleware adds various security headers to help protect against common web vulnerabilities:
    - X-Frame-Options: Prevents clickjacking attacks
    - X-Content-Type-Options: Prevents MIME type sniffing
    - Referrer-Policy: Controls how much referrer information is sent
    - Strict-Transport-Security: Enforces HTTPS connections
    - Content-Security-Policy: Controls allowed content sources
    """

    async def dispatch(self, request, call_next):
        """Process the request/response and add security headers.

        Args:
            request: The incoming request
            call_next: The next middleware/route handler in the chain

        Returns:
            response: The response with added security headers
        """
        response = await call_next(request)
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = (
            """
            default-src 'self';
            script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://donorbox.org https://*.googleapis.com https://maps.googleapis.com https://cdn.quilljs.com;
            script-src-elem 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://donorbox.org https://*.googleapis.com https://maps.googleapis.com https://cdn.quilljs.com;
            style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://cdn.quilljs.com;
            font-src 'self' https://fonts.gstatic.com;
            img-src 'self' data: https://*.googleapis.com https://*.gstatic.com;
            frame-src https://donorbox.org https://www.google.com https://*.google.com;
            connect-src 'self' https://*.googleapis.com https://maps.googleapis.com;
            worker-src 'self' blob:;
            child-src blob:;
        """.replace(
                "\n", " "
            ).strip()
        )
        return response


app.add_middleware(SecurityHeadersMiddleware)
app.middleware("http")(error_handler_middleware)


@app.on_event("startup")  # type: ignore
async def on_startup(db: Session = next(deps.get_db())) -> None:
    """
    Event handler that gets called when the application starts.
    Logs application start and creates database and tables if they do not exist.

    Args:
        db (Session): Database session.
    """
    logger.info("--- Start FastAPI ---")
    logger.debug("Starting FastAPI App...")
    if settings.NOTIFY_ON_START:
        await notify.notify(text=f"{settings.PROJECT_NAME}('{settings.ENV_NAME}') started.")

    await init_initial_data(db=db)


# @app.on_event("startup")  # type: ignore
# @repeat_every(seconds=120, wait_first=False)
# async def repeating_task() -> None:
#     logger.debug("This is a repeating task example that runs every 120 seconds.")
