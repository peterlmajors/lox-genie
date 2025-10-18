
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import time

from services.api.api.routes.chat import router as chat_router
from services.api.api.routes.user import router as user_router
from services.api.api.routes.health import router as health_router
from services.api.api.routes.root import router as root_router
from services.api.api.routes.thread import router as thread_router
from services.api.api.routes.wish import router as wish_router
from services.api.api.routes.youtube import router as youtube_router
from services.api.api.routes.sleeper import router as sleeper_router
from services.api.api.routes.nfl_players import router as nfl_players_router
from services.api.redis.client import startup_redis, shutdown_redis
from services.api.crud.mongodb import mongodb_client
from services.api.core.config import settings

# Configure logging
logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL))
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown events."""
    logger.info(f"Starting {settings.NAME} v{settings.VERSION}")
    logger.info(f"Environment: {settings.ENV}")
    
    # Startup
    await startup_redis()
    await mongodb_client.connect()
    logger.info("MongoDB connected successfully")
    yield
    
    # Shutdown
    await shutdown_redis()
    await mongodb_client.disconnect()
    logger.info(f"Shutting down {settings.NAME}")

# Initialize FastAPI app with lifespan
app = FastAPI(
    title=settings.NAME,
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

# Add response time middleware
@app.middleware("http")
async def add_response_time_header(request: Request, call_next):
    """Add X-Response-Time header to all responses."""
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Response-Time"] = f"{process_time:.4f}s"
    return response

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unexpected errors."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

# Include API routes
app.include_router(chat_router, tags=["Chat"])
app.include_router(wish_router, tags=["Wish"])
app.include_router(thread_router, tags=["Thread"])
app.include_router(user_router, tags=["User"])
app.include_router(sleeper_router, tags=["Sleeper"])
app.include_router(nfl_players_router, tags=["NFL Players"])
app.include_router(youtube_router, tags=["YouTube"])
app.include_router(health_router, tags=["Health"])
app.include_router(root_router, tags=["Root"])