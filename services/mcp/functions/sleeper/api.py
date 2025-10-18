import httpx
from services.mcp.core.config import settings

sleeper_api_url = settings.SLEEPER_API_URL
nfl_year = settings.NFL_YEAR

def get_current_state_nfl():
    """
    Args:
        - None
    Returns:
        - A dictionary containing the current state of the NFL season.
    Example:
        {
        "week": 2, // week
        "season_type": "regular", // pre, post, regular
        "season_start_date": "2020-09-10", // regular season start
        "season": "2020", // current season
        "previous_season": "2019",
        "leg": 2, // week of regular season
        "league_season": "2021", // active season for leagues
        "league_create_season": "2021", // flips in December
        "display_week": 3 // Which week to display in UI, can be different than week
    }
    """
    url = f"{sleeper_api_url}/state/nfl"
    with httpx.Client() as client:
        response = client.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch current state of NFL: {response.status_code}")

def get_user(username: str):
    """
    Args:
        - username: The username of the user.
    Returns:
        {
            "username": "sleeperuser",
            "user_id": "12345678",
            "display_name": "SleeperUser",
            "avatar": "cc12ec49965eb7856f84d71cf85306af"
        }
    """
    url = f"{sleeper_api_url}/user/{username}"
    with httpx.Client() as client:
        response = client.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch user metadata: {response.status_code}")

def get_league_users(league_id: str):
    """
    Args:
        - league_id: The ID of the league.
    Returns:
        - A list of user ids, user metadata, and team names for each user in the league.
    Example:
        [
            {
                "user_id": "<user_id>",
                "username": "<username>",
                "display_name": "<display_name>",
                "avatar": "1233456789",
                "metadata": {
                "team_name": "Dezpacito"
                },
                "is_owner": true   // is commissioner (there can be multiple commissioners)
            },
            ...
        ]
    """
    url = f"{sleeper_api_url}/league/{league_id}/users"
    with httpx.Client() as client:
        response = client.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch league users: {response.status_code}")

def get_league_rosters(league_id: str):
    """
    Args:
        - league_id: The ID of the league.
    Returns:
        - A list of player ids and team metadata for each roster in the league.
    Example:
        [
            {
                "starters": ["2307", "2257", "4034", "147", "642", "4039", "515", "4149", "DET"],
                "settings": {
                "wins": 5,
                "waiver_position": 7,
                "waiver_budget_used": 0,
                "total_moves": 0,
                "ties": 0,
                "losses": 9,
                "fpts_decimal": 78,
                "fpts_against_decimal": 32,
                "fpts_against": 1670,
                "fpts": 1617
                },
                "roster_id": 1,
                "reserve": [],
                "players": ["1046", "138", "147", "2257", "2307", "2319", "4034", "4039", "4040", "4149", "421", "515", "642", "745", "DET"],
                "owner_id": "188815879448829952",
                "league_id": "206827432160788480"
            },
            ...
        ]
    """
    url = f"{sleeper_api_url}/league/{league_id}/rosters"
    with httpx.Client() as client:
        response = client.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch rosters: {response.status_code}")

def get_league_transactions(league_id: str, round: int):
    """
    Args:
        - league_id: The ID of the league.
        - round: The week you want to pull from.
    Returns:
        - A list of transactions for the league.
    Example:
        [
            {
                "type": "trade",
                "transaction_id": "434852362033561600",
                "status_updated": 1558039402803,
                "status": "complete",
                "settings": null,     // trades do not use this field
                "roster_ids": [2, 1], // roster_ids involved in this transaction
                "metadata": null,
                "leg": 1,         // in football, this is the week
                "drops": null,
                "draft_picks": [  // picks that were traded
                {
                    "season": "2019",// the season this draft pick belongs to
                    "round": 5,      // which round this draft pick is
                    "roster_id": 1,  // original owner's roster_id
                    "previous_owner_id": 1,  // previous owner's roster id (in this trade)
                    "owner_id": 2,   // the new owner of this pick after the trade
                },
                {
                    "season": "2019",
                    "round": 3,
                    "roster_id": 2,
                    "previous_owner_id": 2,
                    "owner_id": 1,
                }
                ],
                "creator": "160000000000000000",  // user id who initiated the transaction
                "created": 1558039391576,
                "consenter_ids": [2, 1], // roster_ids of the people who agreed to this transaction
                "adds": null
                "waiver_budget": [   // roster_id 2 sends 55 FAAB dollars to roster_id 3
                {
                    "sender": 2,
                    "receiver": 3,
                    "amount": 55
                }
                ],
            },
            {
                "type": "free_agent",  // could be waiver or trade as well
                "transaction_id": "434890120798142464",
                "status_updated": 1558048393967,
                "status": "complete",
                "settings": null,   // could be {'waiver_bid': 44} if it's FAAB waivers
                "roster_ids": [1],  // roster_ids involved in this transaction
                "metadata": null,   // can contain notes in waivers like why it didn't go through
                "leg": 1,
                "drops": {
                "1736": 1         // player id 1736 dropped from roster_id 1
                },
                "draft_picks": [],
                "creator": "160000000000000000",
                "created": 1558048393967,
                "consenter_ids": [1], // the roster_ids who agreed to this transaction
                "adds": {
                "2315": 1   // player id 2315 added to roster_id 1
                ...
                },
                "waiver_budget": []  // this used for trades only involving FAAB
            },
            ...
        ]
    """
    url = f"{sleeper_api_url}/league/{league_id}/transactions/{round}"
    with httpx.Client() as client:
        response = client.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch league transactions for week {round}: {response.status_code}")

def get_all_league_drafts(league_id: str):
    """
    Args:
        - league_id: The ID of the league.
    Returns:
        - A list of draft metadata for the league.
    Example:
        [
            {
                "type": "snake",
                "status": "complete",
                "start_time": 1515700800000,
                "sport": "nfl",
                "settings": {
                "teams": 6,
                "slots_wr": 2,
                "slots_te": 1,
                "slots_rb": 2,
                "slots_qb": 1,
                "slots_k": 1,
                "slots_flex": 2,
                "slots_def": 1,
                "slots_bn": 5,
                "rounds": 15,
                "pick_timer": 120
                },
                "season_type": "regular",
                "season": "2017",
                "metadata": {
                "scoring_type": "ppr",
                "name": "My Dynasty",
                "description": ""
                },
                "league_id": "257270637750382592",
                "last_picked": 1515700871182,
                "last_message_time": 1515700942674,
                "last_message_id": "257272036450111488",
                "draft_order": null,
                "draft_id": "257270643320426496",
                "creators": null,
                "created": 1515700610526
            },
            ...
        ]
    """
    url = f"{sleeper_api_url}/league/{league_id}/drafts"
    with httpx.Client() as client:
        response = client.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch draft history: {response.status_code}")

def get_all_draft_picks(draft_id):
    """
    Args:
        - draft_id: The ID of the draft to retrieve picks for.
    Returns:
        - A list of draft picks for the draft.
    Example:
        [
            {
                "player_id": "2391",
                "picked_by": "234343434", // user_id this pick will go to (not all leagues have users in every slot, this can be "")
                "roster_id": "1", // roster_id this pick will go to
                "round": 5,
                "draft_slot": 5, // which column this is on the draftboard
                "pick_no": 1,
                "metadata": {
                "team": "ARI",
                "status": "Injured Reserve",
                "sport": "nfl",
                "position": "RB",
                "player_id": "2391",
                "number": "31",
                "news_updated": "1513007102037",
                "last_name": "Johnson",
                "injury_status": "Out",
                "first_name": "David"
                },
                "is_keeper": null,
                "draft_id": "257270643320426496"
            },
            {
                "player_id": "1408",
                "picked_by": "234343434", // user_id this pick will go to (not all leagues have users in every slot, this can be "")
                "roster_id": "1", // roster_id this pick will go to
                "round": 5,
                "draft_slot": 6,
                "pick_no": 2,
                "metadata": {
                "team": "PIT",
                "status": "Active",
                "sport": "nfl",
                "position": "RB",
                "player_id": "1408",
                "number": "26",
                "news_updated": "1515698101257",
                "last_name": "Bell",
                "injury_status": "",
                "first_name": "Le'Veon"
                },
                "is_keeper": null,
                "draft_id": "257270643320426496"
            },
            {
                "player_id": "536",
                "picked_by": "667279356739584",
                "pick_no": 3,
                "metadata": {
                "team": "PIT",
                "status": "Active",
                "sport": "nfl",
                "position": "WR",
                "player_id": "536",
                "number": "84",
                "news_updated": "1515673801292",
                "last_name": "Brown",
                "injury_status": "Probable",
                "first_name": "Antonio"
                },
                "is_keeper": null,
                "draft_id": "257270643320426496"
            },
            ...
        ]
    """
    url = f"{sleeper_api_url}/draft/{draft_id}/picks"
    with httpx.Client() as client:
        response = client.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch draft picks from draft {draft_id}: {response.status_code}")

def get_trending_players(type: str, hours: int = 24, limit: int = 50):
    """
    Args:
        type: Either 'add' or 'drop'
        lookback_hours: Number of hours to look back (default is 24) - optional
        limit: Number of players to return (default is 50) - optional
    Returns:
        - A dictionary of trending players.
    Example:
        [
            {
                "player_id": "1111", // the player_id
                "count": 45 // number of adds or drops
            },
            ...
        ]
    """
    if type not in ['add', 'drop']:
        raise Exception(f"Invalid type: {type}. Must be 'add' or 'drop'.")
    if hours < 0:
        raise Exception(f"Invalid lookback_hours: {hours}. Must be greater than 0.")
    if hours > 24 * 30:
        raise Exception(f"Invalid lookback_hours: {hours}. Must be less than 30 days.")
    if limit < 1:
        raise Exception(f"Invalid limit: {limit}. Must be greater than 0.")
    if limit > 100:
        raise Exception(f"Invalid limit: {limit}. Must be less than 100.")

    url = f"{sleeper_api_url}/players/nfl/trending/{type}/lookback_hours={hours}&limit={limit}"
    with httpx.Client() as client:
        response = client.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch trending players: {response.status_code}")

def get_nfl_leagues_user(user_id: str, year: int = nfl_year):
    """
    Fetch all leagues for a user for a given year and sport.
    API: https://api.sleeper.app/v1/user/{user_id}/leagues/{sport}/{year}
    Returns a list of league objects.
    """
    url = f"{sleeper_api_url}/user/{user_id}/leagues/nfl/{year}"
    with httpx.Client() as client:
        response = client.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"Failed to fetch leagues for user {user_id}: {response.status_code}"
            )

def get_team_performances(league_id: int, week: int = None):
    """
    Fetch matchups for a given week
    """
    if week is None:
        week = get_current_state_nfl()["week"]

    url = f"{sleeper_api_url}/league/{league_id}/matchups/{week}"
    with httpx.Client() as client:
        response = client.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"Failed to fetch matchups for week {week}: {response.status_code}"
            )
