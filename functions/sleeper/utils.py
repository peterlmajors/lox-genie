import pandas as pd

def _match_id_metadata(dict_name: str, players: dict, roster: dict, users: list[dict]) -> list[dict]:
    """
    Matches IDs in a roster to player/user metadata, with enhanced debugging and error handling.
    """
    try:
        resp = []
        nickname_ids = [id.split("_")[-1] for id in list(roster.get("nicknames", {}).keys())]
        if roster.get(dict_name):
            if dict_name == "user_id":
                user = next((user for user in users if roster["user_id"] == user.get("user_id")), None)
                if not user:
                    raise Exception(f"_match_id_metadata(): No match found for user_id {roster['user_id']}")
                user.pop("user_id")
                return user
            else:
                for id in roster[dict_name]:
                    try:
                        if id and str(id) != "0":
                            # Match player data
                            player_data = players.get(id, {"full_name": None, "position": None, "headshot": None, "player_id": id})

                            # Match roster-assigned nickname
                            nickname = roster.get("nicknames", {}).get(f"p_nick_{id}") if id in nickname_ids else None
                            player_data = player_data.copy()  # Avoid mutating the original dict
                            player_data["nickname"] = nickname
                            resp.append(player_data)

                    except Exception as e:
                        print(f"_match_id_metadata(): Error matching {dict_name} id {id}: {e}")
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