from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from api.fantasycalc import router as fantasy_calc_router
from api.sleeper_user import router as sleeper_user_router
from api.sleeper_team import router as sleeper_team_router
from api.sleeper_leagues import router as sleeper_leagues_router
from api.sleeper_draft import router as sleeper_draft_router
from config import settings

app = FastAPI(title=settings.NAME, description=settings.DESCRIPTION, version=settings.VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(fantasy_calc_router, prefix="/fantasycalc", tags=["Fantasy Calc"])
app.include_router(sleeper_user_router, prefix="/sleeper_user", tags=["Sleeper User"])
app.include_router(sleeper_team_router, prefix="/sleeper_team", tags=["Sleeper Team"])
app.include_router(sleeper_leagues_router, prefix="/sleeper_leagues", tags=["Sleeper Leagues"])
app.include_router(sleeper_draft_router, prefix="/sleeper_draft", tags=["Sleeper Draft"])

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.NAME}",
        "version": settings.VERSION,
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
