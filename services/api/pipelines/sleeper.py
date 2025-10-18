
from services.api.core.config import settings
import logging
import httpx

logger = logging.getLogger(__name__)

def get_nfl_players() -> list[tuple[dict]]:
    """
    Fetches complete list of NFL players from Sleeper API.
    Returns:
        - A list of player dictionaries containing their metadata.
    Example:
    [
        {
            "hashtag": "#TomBrady-NFL-NE-12",
            "depth_chart_position": 1,
            "status": "Active",
            "sport": "nfl",
            "fantasy_positions": ["QB"],
            "number": 12,
            "search_last_name": "brady",
            "injury_start_date": null,
            "weight": "220",
            "position": "QB",
            "practice_participation": null,
            "sportradar_id": "",
            "team": "NE",
            "last_name": "Brady",
            "college": "Michigan",
            "fantasy_data_id": 17836,
            "injury_status": null,
            "player_id": "3086",
            "height": "6'4\"",
            "search_full_name": "tombrady",
            "age": 40,
            "stats_id": "",
            "birth_country": "United States",
            "espn_id": "",
            "search_rank": 24,
            "first_name": "Tom",
            "depth_chart_order": 1,
            "years_exp": 14,
            "rotowire_id": null,
            "rotoworld_id": 8356,
            "search_first_name": "tom",
            "yahoo_id": null
        },
        ...
    ]
    """
    try:
        url = f"{settings.SLEEPER_API_URL}/players/nfl"
        with httpx.Client() as client:
            response = client.get(url)
            if response.status_code == 200:
                players_dict = response.json()
                players_list = list(players_dict.values())

                logger.info(f"Fetched {len(players_list)} players from Sleeper API")
                return players_list
            else:
                raise Exception(f"Failed to fetch players from Sleeper API: {response.status_code}")
    except Exception as e:
        raise Exception(f"Error fetching players from Sleeper API: {e}") from e