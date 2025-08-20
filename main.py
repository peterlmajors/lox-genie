from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from api.health import router as health_router
from api.fantasy_football import router as fantasy_football_router

app = FastAPI(
    title="Lox Research",
    description="[Description pending].",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your API routes
app.include_router(health_router, prefix = "/health", tags=["Health"])
app.include_router(fantasy_football_router, prefix = "/fantasy_stats", tags=["Stats"])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
