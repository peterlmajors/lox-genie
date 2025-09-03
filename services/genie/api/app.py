from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

from services.genie.api.routes.chat import router as chat_router
from services.genie.core.config import settings

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
app.include_router(chat_router, prefix="/genie", tags=["Chat"])

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": settings.NAME}


@app.get("/")
async def root():
    """Root endpoint with service information."""
    return {
        "message": f"Welcome to {settings.NAME}",
        "version": settings.VERSION,
        "environment": settings.ENV,
        "docs": "/docs",
    }