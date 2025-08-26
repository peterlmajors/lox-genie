from fastapi import APIRouter, HTTPException
from typing import Optional, Union
from collections import Counter
import pandas as pd
import polars as pl

from functions.sleeper.utils import get_league_rosters, get_league_users, get_all_league_drafts, get_all_draft_picks
from config import settings

router = APIRouter()

players = get_fantasy_players()
off_stats = settings.OFFENSE_STATS
def_stats = settings.DEFENSE_STATS
k_stats = settings.KICKER_STATS

@router.get("/leagues/{league_id}/rosters")
def get_league_rosters_metadata(league_id: str, exclude_names: Optional[Union[str, list[str]]] = None, players: dict = players) -> pd.DataFrame:

    league_rosters = pd.DataFrame()
    users = get_league_users(league_id)
    for user in users:
        if user.get("display_name") in exclude_names:
            continue

        df = get_user_roster(league_id, user.get("user_id"), players, df=True)
        if df is not None:
            league_rosters = pd.concat([league_rosters, df], ignore_index=True)

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
            users_teams.append({"user_id": user_id,
                    "display_name": display_name,
                    "team_name": team_name,
                }
            )

        except Exception as e:
            print(f"Error mapping user to teams at index {idx}: {e}")
            continue

    return users_teams