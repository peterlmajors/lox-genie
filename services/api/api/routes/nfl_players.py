from fastapi import APIRouter, HTTPException, Query
from typing import Any
from services.api.crud.mongodb import get_mongodb, MongoDBClient
from fastapi import Depends
from rapidfuzz import process, fuzz

router = APIRouter(prefix="/nfl_players")

@router.get("/search", summary="Find the closest matching NFL player by name")
async def search_nfl_player(name: str, client: MongoDBClient = Depends(get_mongodb)) -> dict:
    """
    Find the closest match to a player's full_name in the MongoDB players collection.

    Args:
        name: The player name to find.

    Returns:
        dict: The closest match player document.
    """
    collection = client.get_collection("players")
    cursor = collection.find({}, {"full_name": 1})

    names = []
    name_to_doc = {}
    async for doc in cursor:
        if "full_name" in doc and doc["full_name"]:
            names.append(doc["full_name"])
            name_to_doc[doc["full_name"]] = doc

    if not names:
        raise HTTPException(status_code=404, detail="No player names found in the database")

    best_match = process.extractOne(name, names, scorer=fuzz.WRatio)
    if not best_match or best_match[1] < 60:
        raise HTTPException(status_code=404, detail=f"No close match found for '{name}'")
    matched_name = best_match[0]

    player_doc = await collection.find_one({"full_name": matched_name})
    if not player_doc:
        raise HTTPException(status_code=404, detail=f"Player not found: {matched_name}")

    player_doc["_id"] = str(player_doc["_id"])  # Convert ObjectId to str for JSON serialization
    return {"match": matched_name, "score": best_match[1], "player": player_doc}

