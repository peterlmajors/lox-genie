from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from services.genie.api.routes.fantasycalc import router as fantasy_calc_router
from services.genie.api.routes.sleeper_user import router as sleeper_user_router
from services.genie.api.routes.sleeper_team import router as sleeper_team_router
from services.genie.api.routes.sleeper_league import router as sleeper_league_router
from services.genie.api.routes.sleeper_draft import router as sleeper_draft_router
from services.genie.core.config import settings

# Configure logging
logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL))
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown events."""
    # Startup
    logger.info(f"Starting {settings.NAME} v{settings.VERSION}")
    logger.info(f"Environment: {settings.ENV}")

    yield

    # Shutdown
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


# Include API routes
app.include_router(fantasy_calc_router, prefix="/fantasycalc", tags=["Fantasy Calc"])
app.include_router(sleeper_user_router, prefix="/sleeper_user", tags=["Sleeper User"])
app.include_router(sleeper_team_router, prefix="/sleeper_team", tags=["Sleeper Team"])
app.include_router(sleeper_league_router, prefix="/sleeper_league", tags=["Sleeper League"])
app.include_router(sleeper_draft_router, prefix="/sleeper_draft", tags=["Sleeper Draft"])