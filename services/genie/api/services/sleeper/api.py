import httpx
from services.genie.core.config import settings


def get_league_rosters(league_id: str):
    """
    Fetch roster data for league
    """
    url = f"https://api.sleeper.app/v1/league/{league_id}/rosters"
    with httpx.Client() as client:
        response = client.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch rosters: {response.status_code}")


def get_league_users(league_id: str):
    """
    Fetch league members data
    """
    url = f"https://api.sleeper.app/v1/league/{league_id}/users"
    with httpx.Client() as client:
        response = client.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch league users: {response.status_code}")


def get_all_league_drafts(league_id: str):
    """
    Fetch draft history for league
    """
    url = f"https://api.sleeper.app/v1/league/{league_id}/drafts"
    with httpx.Client() as client:
        response = client.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch draft history: {response.status_code}")


def get_all_draft_picks(draft_id):
    """
    Fetch draft history for league
    """
    url = f"https://api.sleeper.app/v1/draft/{draft_id}/picks"
    with httpx.Client() as client:
        response = client.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"Failed to fetch draft picks from draft {draft_id}: {response.status_code}"
            )


def get_league_transactions(league_id: str, round):
    """
    Fetch league transactions for given week
    """
    url = f"https://api.sleeper.app/v1/league/{league_id}/transactions/{round}"
    with httpx.Client() as client:
        response = client.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"Failed to fetch league transactions for week {round}: {response.status_code}"
            )


def get_current_state_nfl():
    """
    Fetch current state of NFL season
    """
    url = "https://api.sleeper.app/v1/state/nfl"
    with httpx.Client() as client:
        response = client.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"Failed to fetch current state of NFL: {response.status_code}"
            )


def get_nfl_players():
    """
    Fetch all players in the NFL
    """
    url = "https://api.sleeper.app/v1/players/nfl"
    with httpx.Client() as client:
        response = client.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch players: {response.status_code}")


def get_nfl_leagues_user(user_id: str, year: int = settings.NFL_YEAR):
    """
    Fetch all leagues for a user for a given year and sport.
    API: https://api.sleeper.app/v1/user/{user_id}/leagues/{sport}/{year}
    Returns a list of league objects.
    """
    url = f"https://api.sleeper.app/v1/user/{user_id}/leagues/nfl/{year}"
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

    url = f"https://api.sleeper.app/v1/league/{league_id}/matchups/{week}"
    with httpx.Client() as client:
        response = client.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"Failed to fetch matchups for week {week}: {response.status_code}"
            )
