import pandas as pd
from typing import Optional, Union
from football.external.sleeper.players import get_fantasy_players
from football.external.sleeper.sleeper import get_league_rosters, get_league_users
from football.external.sleeper.draft import get_all_league_drafts, get_all_draft_picks
import polars as pl

players = get_fantasy_players()


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


def get_user_roster(
    league_id: str, user_id: str, players: dict = players, df: bool = True
) -> Union[dict, pd.DataFrame]:

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


def get_league_rosters_metadata(
    league_id: str,
    exclude_names: Optional[Union[str, list[str]]] = None,
    players: dict = players,
) -> pd.DataFrame:

    league_rosters = pd.DataFrame()
    users = get_league_users(league_id)
    for user in users:
        if user.get("display_name") in exclude_names:
            continue

        df = get_user_roster(league_id, user.get("user_id"), players, df=True)
        if df is not None:
            league_rosters = pd.concat([league_rosters, df], ignore_index=True)

    return league_rosters


def _match_id_metadata(
    dict_name: str, players: dict, roster: dict, users: list[dict]
) -> list[dict]:
    """
    Matches IDs in a roster to player/user metadata, with enhanced debugging and error handling.
    """
    try:
        nickname_ids = [
            id.split("_")[-1] for id in list(roster.get("nicknames", {}).keys())
        ]
        resp = []
        if roster.get(dict_name):
            if dict_name == "user_id":
                user = next(
                    (
                        user
                        for user in users
                        if roster["user_id"] == user.get("user_id")
                    ),
                    None,
                )
                if not user:
                    raise Exception(
                        f"_match_id_metadata(): No match found for user_id {roster['user_id']}"
                    )
                user.pop("user_id")
                return user
            else:
                for id in roster[dict_name]:
                    try:
                        if id and str(id) != "0":
                            # Match player data
                            player_data = players.get(
                                id,
                                {
                                    "full_name": None,
                                    "position": None,
                                    "headshot": None,
                                    "player_id": id,
                                },
                            )

                            # Match roster-assigned nickname
                            nickname = (
                                roster.get("nicknames", {}).get(f"p_nick_{id}")
                                if id in nickname_ids
                                else None
                            )
                            player_data = (
                                player_data.copy()
                            )  # Avoid mutating the original dict
                            player_data["nickname"] = nickname
                            resp.append(player_data)

                    except Exception as e:
                        print(
                            f"_match_id_metadata(): Error matching {dict_name} id {id}: {e}"
                        )
                        continue
        return resp

    except Exception as e:
        print(f"_match_id_metadata(): General error: {e}")
        return None


def _roster_dict_to_df(roster: dict):

    rows = []
    # Add starters
    for player in roster.get("starters", []):
        player_row = player.copy()
        player_row["roster_slot"] = "starter"
        rows.append(player_row)
    # Add bench (non_starters)
    for player in roster.get("non_starters", []):
        player_row = player.copy()
        player_row["roster_slot"] = "bench"
        rows.append(player_row)
    # Add taxi
    for player in roster.get("taxi", []):
        player_row = player.copy()
        player_row["roster_slot"] = "taxi"
        rows.append(player_row)

    df = pd.DataFrame(rows)
    return df


def get_league_picks(league_id: str) -> pl.DataFrame:
    league_picks = []
    drafts = get_all_league_drafts(league_id)
    for d in drafts:
        draft_type = "rookie" if d.get("type") == "snake" else "auction"
        draft_id = d.get("draft_id")
        season = d.get("season")
        picks = get_all_draft_picks(draft_id)
        for p in picks:
            metadata = p.get("metadata", {})
            pick = {
                "player_id": p.get("player_id"),
                "player_name": f"{metadata.get('first_name', '')} {metadata.get('last_name', '')}".strip(),
                "user_id": p.get("picked_by"),
                "years_exp": metadata.get("years_exp"),
                "draft_salary": metadata.get("amount"),
                "ifl_pick_no": p.get("pick_no"),
                "ifl_round": p.get("round"),
                "draft": draft_type,
                "draft_id": draft_id,
                "season": season,
            }
            league_picks.append(pick)
    pick_history = pl.DataFrame(league_picks)
    return pick_history
