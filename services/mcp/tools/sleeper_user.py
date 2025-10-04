
from collections import Counter
from services.mcp.functions.sleeper.api import get_nfl_leagues_user
from services.mcp.core.config import settings

def get_nfl_leagues_user_metadata(user_id: str, season: int = settings.NFL_YEAR) -> list:
    """
    Get all NFL leagues for a user with metadata.
    """
    leagues = get_nfl_leagues_user(user_id, season)
    if not leagues:
        raise Exception(
            f"No leagues found for user {user_id} in season {season}. The user may not exist or may not have any leagues for this season.",
        )

    resp = []
    for league in leagues:
        # Keep only the keys we need
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

        # Convert roster_positions to a dictionary
        if "roster_positions" in filtered_league:
            filtered_league["roster_positions"] = dict(
                Counter(filtered_league["roster_positions"])
            )

        # Filter the scoring settings
        scoring_settings = filtered_league.get("scoring_settings", {})
        filtered_league["offense_scoring"] = {
            k: v for k, v in scoring_settings.items() if k in settings.OFFENSE_STATS
        }
        filtered_league["defense_scoring"] = {
            k: v for k, v in scoring_settings.items() if k in settings.DEFENSE_STATS
        }
        filtered_league["kicker_scoring"] = {
            k: v for k, v in scoring_settings.items() if k in settings.KICKER_STATS
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

def get_current_league_records(user_id: str) -> list[dict]:
    """
    Get the record for the current league(s) for a user.
    """
    records = []
    leagues = get_nfl_leagues_user_metadata(user_id)
    for league in leagues:
        if league.get("current_league_id"):
            current_id = league.get("current_league_id")
            record = get_record(current_id, user_id)

            record["league_name"] = league.get("name")
            record["user_id"] = user_id
            record["league_id"] = current_id
            records.append(record)
    return records

def get_previous_league_records(user_id: str) -> list[dict]:
    """
    Get the record for the previous league for a user.
    """
    records = []
    leagues = get_nfl_leagues_user_metadata(user_id)
    for league in leagues:
        if league.get("previous_league_id"):
            prev_id = league.get("previous_league_id")
            record = get_record(prev_id, user_id)

            record["league_name"] = league.get("name")
            record["user_id"] = user_id
            record["league_id"] = prev_id
            records.append(record)
    return records

def get_season_records(user_id: int, year: int) -> list[dict]:
    """Get user records for a specific season across all leagues."""
    records = []
    leagues = get_nfl_leagues_user_metadata(user_id, year)
    for league in leagues:
        record = get_record(league["league_id"], user_id)
        record["league_name"] = league.get("name")
        record["user_id"] = user_id
        record["league_id"] = league.get("league_id")
        records.append(record)
    return records