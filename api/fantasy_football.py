from fastapi import APIRouter
from config import settings

router = APIRouter()

@router.get("/stat_categories")
async def get_stat_categories(stat_type: str):
    
    if stat_type == "offense":
        return {"categories": settings.OFFENSE_STATS}
    elif stat_type == "defense":
        return {"categories": settings.DEFENSE_STATS}
    elif stat_type == "kicker":
        return {"categories": settings.KICKER_STATS}
    else:   
        return {"error": "Invalid stat type. Use 'offense', 'defense', or 'kicker'."}
