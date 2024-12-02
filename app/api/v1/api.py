from app import models, settings, version
from app.routes.api import api_router


@api_router.get("/", response_model=models.HealthCheck, tags=["status"])
async def health_check() -> dict[str, str]:
    """
    Health check endpoint.

    Returns:
        dict[str, str]: Health check response.
    """
    return {
        "name": settings.PROJECT_NAME,
        "version": version,
        "description": settings.PROJECT_DESCRIPTION,
    }
