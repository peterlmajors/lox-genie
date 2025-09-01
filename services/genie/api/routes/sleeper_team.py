import json
from pathlib import Path
from fastapi import APIRouter
from services.genie.api.services.sleeper.api import get_league_rosters
from services.genie.api.services.sleeper.utils import (
    match_id_metadata,
    roster_dict_to_df,
    get_league_users_teams,
)

# Get the project root directory (two levels up from this file)
project_root = Path(__file__).parent.parent.parent.parent
fantasy_players_path = project_root / "data" / "fantasy_players.json"
with fantasy_players_path.open("r", encoding="utf-8") as f:
    sleeper_players: dict = json.load(f)

router = APIRouter()


@router.get("/leagues/{league_id}/users/{user_id}/roster")
def get_user_roster(
    league_id: str, user_id: str, players: dict = sleeper_players, df: bool = True
):
    """
    Fetches and processes user rosters for a given league_id.
    """

    def get_user_roster_ids(league_id: str, user_id: str) -> dict:
        rosters_raw = get_league_rosters(league_id)
        user_roster = next(
            (r for r in rosters_raw if r.get("owner_id") == user_id), None
        )
        if not user_roster:
            print(f"No roster found for user_id {user_id} in league {league_id}")
            return {}
        else:
            user_id_val = user_roster.get("owner_id", None)
            starters = user_roster.get("starters", [])
            players = user_roster.get("players", [])
            taxi = user_roster.get("taxi", [])

            metadata = user_roster.get("metadata", {})
            if not isinstance(metadata, dict):
                metadata = {}
            nicknames = {k: v for k, v in metadata.items() if "p_nick" in k}
            if players:
                non_starters = [player for player in players if player not in starters]
            else:
                non_starters = []

            processed_roster = {
                "user_id": user_id_val,
                "starters": starters,
                "non_starters": non_starters,
                "taxi": taxi,
                "nicknames": nicknames,
            }
            return processed_roster

    roster = get_user_roster_ids(league_id, user_id)
    users_teams = get_league_users_teams(league_id)
    for user in users_teams:
        if user["user_id"] == user_id:
            team = user["team_name"]
            break

    roster["user"] = match_id_metadata("user_id", players, roster, users_teams)
    roster["starters"] = match_id_metadata("starters", players, roster, users_teams)
    roster["non_starters"] = match_id_metadata(
        "non_starters", players, roster, users_teams
    )
    roster["taxi"] = match_id_metadata("taxi", players, roster, users_teams)
    roster.pop("nicknames")

    if df:
        roster_df = roster_dict_to_df(roster)
        roster_df["team_name"] = team
        return roster_df.to_dict(orient="records")
    return roster


@router.get("/users/{user_id}/leagues/{league_id}/record")
def get_record(league_id: int, user_id: int) -> dict:
    """
    Get the record for a user in a league.
    """
    for roster in get_league_rosters(league_id):
        if roster.get("owner_id") == str(user_id):
            wins = roster["settings"]["wins"]
            losses = roster["settings"]["losses"]
            return {"wins": wins, "losses": losses}


@router.get("/leagues/{league_id}/users/{user_id}/waiver_budget")
def get_waiver_budget_spent(league_id: str, user_id: int = None) -> int | dict:

    rosters = get_league_rosters(league_id)

    if user_id is not None:
        # Return specific user's waiver budget
        for roster in rosters:
            if int(roster["owner_id"]) == user_id:
                return roster.get("settings").get("waiver_budget_used", 0)
        else:
            raise ValueError(f"User {user_id} not found in league {league_id} rosters.")
    else:
        # Return all users' waiver budgets
        waiver_budgets = {}
        for roster in rosters:
            owner_id = int(roster["owner_id"])
            waiver_budget_used = roster.get("settings").get("waiver_budget_used", 0)
            waiver_budgets[owner_id] = waiver_budget_used
        return waiver_budgets
