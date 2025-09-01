from services.genie.api.services.sleeper.api import get_nfl_players

def get_fantasy_players(players=None, positions: list[str] = ["QB", "WR", "TE", "RB"]) -> dict:
    """
    Filters player data to only include specified fantasy positions.
    Adds debugging and error handling.
    """
    if players is None:
        try:
            players = get_nfl_players()
            print(f"get_fantasy_players(): Loaded {len(players)} players.")
        except Exception as e:
            print(f"get_fantasy_players(): Error loading players: {e}")
            return {}

    filtered = {}
    count_skipped = 0
    for player_id, player_data in players.items():
        try:
            position = player_data.get("position", "NA")
            if position in positions and player_data.get("active"):
                espn_id = player_data.get("espn_id")
                headshot = (
                    f"https://a.espncdn.com/i/headshots/nfl/players/full/{espn_id}.png"
                    if espn_id
                    else None
                )

                filtered[player_id] = {
                    "player_id": player_data.get("player_id", player_id),
                    "full_name": player_data.get("full_name", "Unknown"),
                    "position": position,
                    "headshot": headshot,
                }
        except Exception as e:
            print(
                f"get_fantasy_players(): Skipping player_id {player_id} due to error: {e}"
            )
            count_skipped += 1
            continue

    print(
        f"get_fantasy_players(): Filtered to {len(filtered)} players. Skipped {count_skipped} due to errors."
    )
    return filtered