
import logging
from fastapi import APIRouter, HTTPException
from services.api.pipelines.sleeper import get_nfl_players
from services.api.crud.mongodb import get_mongodb

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/sleeper/fantasy-players-upload", summary="Upload complete list of fantasy players to MongoDB")
async def fantasy_players_upload() -> dict:
    """
    Returns: 
    - dict: Upload completion status.
    Example:
    {
        "success": True,
        "message": "Uploaded 100 fantasy players to MongoDB"
    }
    """
    try:
        logger.info("Starting fantasy_players_upload")
        
        # Fetch players from Sleeper API
        fantasy_players = get_nfl_players()
        if len(fantasy_players) == 0:
            raise HTTPException(status_code=400, detail="No players found from Sleeper API")
        logger.info(f"Retrieved {len(fantasy_players)} players from Sleeper API")

        # Get MongoDB client and collection
        client = await get_mongodb()    
        collection = client.get_collection("players")

        # Write players to MongoDB
        resp = await collection.insert_many(fantasy_players)
        logger.info(f"Successfully uploaded {len(resp.inserted_ids)} fantasy players to MongoDB")
        return {"success": True, "message": f"Uploaded {len(resp.inserted_ids)} fantasy players to MongoDB"}
    except Exception as e:
        logger.error(f"Error uploading fantasy players to MongoDB: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error while uploading fantasy players to MongoDB")

