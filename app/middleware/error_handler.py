from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
import logging


async def error_handler_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        if isinstance(e, HTTPException):
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"},
        )
