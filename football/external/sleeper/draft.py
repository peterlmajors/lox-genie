from football.external.sleeper.sleeper import (
    get_league_users,
    get_all_draft_picks,
    get_all_league_drafts,
)
from config import settings


def get_all_draft_picks_metadata(league_id: int, draft_id: int) -> list[dict]:

    users = get_league_users(league_id)
    picks = get_all_draft_picks(draft_id)
    draft = next(
        draft
        for draft in get_all_league_drafts(settings.SLEEPER_IFL_24)
        if draft["draft_id"] == str(draft_id)
    )

    response = []
    for pick in picks:
        pick_dict = {}
        pick_dict["player_id"] = pick["player_id"]
        pick_dict["player_name"] = (
            pick["metadata"]["first_name"] + " " + pick["metadata"]["last_name"]
        )
        pick_dict["round"] = pick["round"]
        pick_dict["pick"] = pick["pick_no"]
        pick_dict["user_id"] = pick["picked_by"]

        for user in users:
            if user["user_id"] == pick_dict["user_id"]:
                pick_dict["team_name"] = user["metadata"]["team_name"]
                pick_dict["display_name"] = user["display_name"]
                break

        if draft["type"] == "auction":
            pick_dict["price"] = pick["metadata"]["amount"]

        response.append(pick_dict)
    return response
