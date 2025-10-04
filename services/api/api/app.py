
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

from services.api.api.routes.chat import router as chat_router
from services.api.api.routes.user import router as user_router
from services.api.api.routes.health import router as health_router
from services.api.api.routes.root import router as root_router
from services.api.core.config import settings

# Configure logging
logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL))
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown events."""
    logger.info(f"Starting {settings.NAME} v{settings.VERSION}")
    logger.info(f"Environment: {settings.ENV}")
    yield
    logger.info(f"Shutting down {settings.NAME}")

# Initialize FastAPI app with lifespan
app = FastAPI(
    title=settings.NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    lifespan=lifespan,
    debug=settings.DEBUG,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unexpected errors."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

# Include API routes
app.include_router(chat_router, tags=["Chat"])
app.include_router(user_router, tags=["User"])
app.include_router(health_router, tags=["Health"])
app.include_router(root_router, tags=["Root"])