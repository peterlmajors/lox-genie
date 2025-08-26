from fastapi import APIRouter, HTTPException
from typing import Optional, Union
from collections import Counter
import pandas as pd
import polars as pl

from functions.sleeper.utils import get_league_rosters, get_league_users, get_all_league_drafts, get_all_draft_picks
from config import settings

router = APIRouter()

players = get_fantasy_players()

@router.get("/leagues/{league_id}/users/{user_id}/roster")
def get_user_roster_ids(league_id: str, user_id: str) -> dict:
    """
    Fetches and processes user rosters for a given league_id.
    """
    rosters_raw = get_league_rosters(league_id)
    user_roster = next((r for r in rosters_raw if r.get("owner_id") == user_id), None)
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

@router.get("/leagues/{league_id}/users/{user_id}/roster")
def get_user_roster(league_id: str, user_id: str, players: dict = players, df: bool = True) -> Union[dict, pd.DataFrame]:

    roster = get_user_roster_ids(league_id, user_id)
    users_teams = get_users_teams(league_id)
    for user in users_teams:
        if user["user_id"] == user_id:
            team = user["team_name"]
            break

    roster["user"] = _match_id_metadata("user_id", players, roster, users_teams)
    roster["starters"] = _match_id_metadata("starters", players, roster, users_teams)
    roster["non_starters"] = _match_id_metadata(
        "non_starters", players, roster, users_teams
    )
    roster["taxi"] = _match_id_metadata("taxi", players, roster, users_teams)
    roster.pop("nicknames")

    if df:
        roster_df = _roster_dict_to_df(roster)
        roster_df["team_name"] = team
        return roster_df
    return roster

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