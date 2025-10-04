from services.mcp.functions.sleeper.api import get_fantasy_players
from services.genie.crud.aws_s3 import post_s3
import logging

logger = logging.getLogger(__name__)

def update_fantasy_players():
    """
    Updates the fantasy players data in AWS S3 (lox-api).
    """
    try:
        fantasy_players = get_fantasy_players()
    except Exception as e:
        logger.error(f"Error gathering fantasy players from Sleeper API: {e}")
        return
    
    try:
        post_s3(fantasy_players, "lox-api", "fantasy_players.json")
    except Exception as e:
        logger.error(f"Error posting fantasy players to AWS S3 (lox-api): {e}")
        return
    logger.info("Fantasy players updated successfully!")