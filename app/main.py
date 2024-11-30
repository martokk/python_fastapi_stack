from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .middleware.error_handler import error_handler_middleware
from .utils.session import setup_session_middleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add session middleware
setup_session_middleware(app)

# Add error handling middleware
app.middleware("http")(error_handler_middleware)

# Include routers
from .routes import admin, auth

app.include_router(admin.router)
app.include_router(auth.router)
