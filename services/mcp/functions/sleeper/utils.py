
import pandas as pd
from services.mcp.functions.sleeper.api import get_league_users

def match_id_metadata(dict_name: str, players: dict, roster: dict, users: list[dict]) -> list[dict]:
    """
    - Matches IDs in a roster to player/user metadata
    - Adds debugging and error handling
    """
    resp = []
    nickname_ids = [id.split("_")[-1] for id in list(roster.get("nicknames", {}).keys())]
    if roster.get(dict_name):
        if dict_name == "user_id":
            user = next((user for user in users if roster["user_id"] == user.get("user_id")), None)
            if not user:
                raise Exception(f"match_id_metadata(): No match found for user_id {roster['user_id']}")
            user.pop("user_id")
            resp.append(user)
        else:
            for id in roster[dict_name]:
                try:
                    player = next((player for player in players if player.get("player_id") == id), None)
                    if not player:
                        raise Exception(f"match_id_metadata(): No match found for {dict_name} id {id}")
                    player = player.copy()
                    player["nickname"] = roster.get("nicknames", {}).get(f"p_nick_{id}") if id in nickname_ids else None
                    resp.append(player)
                except Exception as e:
                    raise Exception(f"match_id_metadata(): Error matching {dict_name} id {id}: {e}")
    return resp 

def roster_dict_to_df(roster: dict) -> pd.DataFrame:
    """
    - Converts a roster dictionary to a pandas DataFrame
    """
    rows = []
    for player in roster.get("starters", []):
        try:
            player_row = player.copy()
            player_row["roster_slot"] = "starter"
            rows.append(player_row)
        except Exception as e:
            raise Exception(f"roster_dict_to_df(): Error converting starter {player} to DataFrame: {e}")
    # Add bench (non_starters)
    for player in roster.get("non_starters", []):
        try:
            player_row = player.copy()
            player_row["roster_slot"] = "bench"
            rows.append(player_row)
        except Exception as e:
            raise Exception(f"roster_dict_to_df(): Error converting non-starter {player} to DataFrame: {e}")
        rows.append(player_row)
    # Add taxi
    for player in roster.get("taxi", []):
        try:
            player_row = player.copy()
            player_row["roster_slot"] = "taxi"
            rows.append(player_row)
        except Exception as e:
            raise Exception(f"roster_dict_to_df(): Error converting taxi {player} to DataFrame: {e}")
        rows.append(player_row)

    df = pd.DataFrame(rows)
    return df

def get_league_users_teams(league_id: str) -> list[dict]:
    """
    - Get users and their team names for a league.
    - This function is moved here to avoid circular imports.
    """
    users_teams = []
    users_raw = get_league_users(league_id)
    for idx, x in enumerate(users_raw):
        try:
            user_id = x.get("user_id")
            display_name = x.get("display_name")
            metadata = x.get("metadata", {})
            team_name = metadata.get("team_name")
            users_teams.append(
                {
                    "user_id": user_id,
                    "display_name": display_name,
                    "team_name": team_name,
                }
            )

        except Exception as e:  
            raise Exception(f"get_league_users_teams(): Error mapping user to teams at index {idx}: {e}")
    return users_teams