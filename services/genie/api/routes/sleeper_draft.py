from fastapi import APIRouter, HTTPException
from services.genie.core.config import settings
from services.genie.api.services.sleeper.api import get_league_users, get_all_draft_picks, get_all_league_drafts

router = APIRouter()

@router.get("/leagues/{league_id}/drafts/{draft_id}/picks")
def get_all_draft_picks_metadata(league_id: int, draft_id: int) -> list[dict]:
    """
    Get all draft picks metadata
    Args:
        league_id: int
        draft_id: int
    Returns:
        list[dict]: List of draft picks metadata
    """
    # Get league users, draft picks, and draft metadata
    users = get_league_users(league_id)
    picks = get_all_draft_picks(draft_id)
    draft = next(
        draft
        for draft in get_all_league_drafts(settings.SLEEPER_IFL_24)
        if draft["draft_id"] == str(draft_id)
    )

    # Create response
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


@router.get("/leagues/{league_id}/picks")
async def get_league_picks(league_id: str) -> list[dict]:
    try:
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
        return league_picks
    except Exception as e:
        raise HTTPException(
            status_code=502, detail=f"Failed to fetch league picks: {e}"
        )
