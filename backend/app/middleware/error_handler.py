"""Global error handler middleware"""
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from app.core.exceptions import AppException

def add_exception_handlers(app: FastAPI):
    """Add exception handlers to FastAPI app"""
    
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"}
        )
