from sleeper import get_nfl_leagues_user, get_league_rosters
from typing import Union, Optional
from collections import Counter
from config import settings

off_stats = settings.OFFENSE_STATS
def_stats = settings.DEFENSE_STATS
k_stats = settings.KICKER_STATS


def get_nfl_leagues_user_metadata(user_id: int, season: int = settings.NFL_YEAR) -> list:
    """
    Get all NFL leagues for a user with metadata.
    """
    leagues = get_nfl_leagues_user(user_id, season)
    if leagues:
        resp = []
        for league in leagues:
            keys_to_keep = [
                "league_id",
                "draft_id",
                "name",
                "status",
                "season_type",
                "total_rosters",
                "roster_positions",
                "scoring_settings",
                "metadata",
                "previous_league_id",
            ]
            filtered_league = {k: league[k] for k in keys_to_keep if k in league}

            if "roster_positions" in filtered_league:
                filtered_league["roster_positions"] = dict(
                    Counter(filtered_league["roster_positions"])
                )

            scoring_settings = filtered_league.get("scoring_settings", {})
            filtered_league["offense_scoring"] = {
                k: v for k, v in scoring_settings.items() if k in off_stats
            }
            filtered_league["defense_scoring"] = {
                k: v for k, v in scoring_settings.items() if k in def_stats
            }
            filtered_league["kicker_scoring"] = {
                k: v for k, v in scoring_settings.items() if k in k_stats
            }
            filtered_league.pop(
                "scoring_settings", None
            )  # Remove the original scoring settings

            # Set ppr flag if offense_scoring ppr is 1
            if filtered_league["offense_scoring"].get("ppr", 0) == 1:
                filtered_league["ppr"] = True
            else:
                filtered_league["ppr"] = False

            # Set tight end premium flag if offense_scoring bonus_rec_te exists and is > 0
            if filtered_league["offense_scoring"].get("bonus_rec_te", 0) > 0:
                filtered_league["tight_end_premium"] = True
            else:
                filtered_league["tight_end_premium"] = False

            # Set two_qb flag if there are at least two 'QB' or one 'QB' and one 'SUPER_FLEX' in roster_positions
            roster_positions = filtered_league.get("roster_positions", {})
            qb_count = roster_positions.get("QB", 0)
            superflex_count = roster_positions.get("SUPER_FLEX", 0)
            if qb_count >= 2 or (qb_count >= 1 and superflex_count >= 1):
                filtered_league["superflex"] = True
            else:
                filtered_league["superflex"] = False

            resp.append(filtered_league)

    return resp

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
