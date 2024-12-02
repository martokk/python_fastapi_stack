from fastapi import APIRouter

from app.views.pages import programs, root
from app.views.pages.admin import admin, login, user

views_router = APIRouter(include_in_schema=False)
views_router.include_router(root.router, tags=["Root"])
views_router.include_router(programs.router, prefix="/programs", tags=["Programs"])
views_router.include_router(login.router, tags=["Logins"])
views_router.include_router(user.router, prefix="/user", tags=["Users"])
views_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
