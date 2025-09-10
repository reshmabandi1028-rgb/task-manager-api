from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException
import logging, traceback

from .database import Base, engine
from . import models, routes, tasks

# Create tables
Base.metadata.create_all(bind=engine)

# Configure logging (safe against double handlers in reload)
if not logging.getLogger().hasHandlers():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

logger = logging.getLogger(__name__)

# App init
app = FastAPI(title="Task Manager API")

# Include routers
app.include_router(routes.router, prefix="/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

# Health check
@app.get("/")
def read_root():
    return {"message": "API is running!"}

# --- Exception Handlers ---

# Global fallback
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    error_trace = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    logger.error(f"Unexpected error at {request.url}: {error_trace}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Something went wrong. Please try again later."},
    )

# HTTPException handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"HTTP {exc.status_code} at {request.url}: {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

# Validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error at {request.url}: {exc.errors()}")
    return JSONResponse(status_code=422, content={"detail": exc.errors()})
