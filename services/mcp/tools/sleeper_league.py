from fastapi import APIRouter
from services.genie.api.services.sleeper.api import get_league_users, get_league_rosters
from services.genie.api.services.sleeper.utils import get_league_users_teams

router = APIRouter()

@router.get("/leagues/{league_id}/rosters")
def get_league_rosters_metadata(league_id: str) -> list[dict]:
    """
    Get league rosters metadata.
    """
    league_rosters = []
    users = get_league_users_teams(league_id)
    rosters_raw = get_league_rosters(league_id)
    for user in users:
        user_roster = next((r for r in rosters_raw if r.get("owner_id") == user.get("user_id")), None)
        if user_roster:
            roster_data = {
                "user_id": user.get("user_id"),
                "display_name": user.get("display_name"),
                "team_name": user.get("team_name"),
                "starters_count": len(user_roster.get("starters", [])),
                "players_count": len(user_roster.get("players", [])),
                "taxi_count": len(user_roster.get("taxi", [])),
                "wins": user_roster.get("settings", {}).get("wins", 0),
                "losses": user_roster.get("settings", {}).get("losses", 0),
            }
            league_rosters.append(roster_data)

    return league_rosters


@router.get("/leagues/{league_id}/users")
def get_users_teams(league_id: str) -> list[dict]:

    users_teams = []
    users_raw = get_league_users(league_id)
    for idx, x in enumerate(users_raw):
        try:
            user_id = x.get("user_id", None)
            display_name = x.get("display_name", None)
            metadata = x.get("metadata", {})
            team_name = metadata.get("team_name", None)
            users_teams.append(
                {
                    "user_id": user_id,
                    "display_name": display_name,
                    "team_name": team_name,
                }
            )

        except Exception as e:
            print(f"Error mapping user to teams at index {idx}: {e}")
            continue

    return users_teams
