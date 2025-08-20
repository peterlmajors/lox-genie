from users import get_nfl_leagues_user_metadata
from leagues import get_league_rosters, get_users_teams
  
  
def get_record(league_id: int, user_id: int) -> dict:
    """
    Get the record for a user in a league.
    """
    for roster in get_league_rosters(league_id):
        if roster.get('owner_id') == str(user_id):
            wins = roster['settings']['wins']
            losses = roster['settings']['losses']
            return {'wins': wins, 'losses': losses}

def get_current_league_records(user_id: int) -> list[dict]:
    """
    Get the record for the current league for a user.
    """
    records = []
    leagues = get_nfl_leagues_user_metadata(user_id)
    for league in leagues:
        if league.get('current_league_id'):
            current_id = league.get('current_league_id')
            record = get_record(current_id, user_id)
            
            record['league_name'] = league.get('name')
            record['user_id'] = user_id
            record['league_id'] = current_id
            records.append(record)
    return records

def get_previous_league_records(user_id: int) -> list[dict]:
    """
    Get the record for the previous league for a user.
    """
    records = []
    leagues = get_nfl_leagues_user_metadata(user_id)
    for league in leagues:
        if league.get('previous_league_id'):
            prev_id = league.get('previous_league_id')
            record = get_record(prev_id, user_id)
            
            record['league_name'] = league.get('name')
            record['user_id'] = user_id
            record['league_id'] = prev_id
            records.append(record)
    return records

def get_win_percentage(league_id: int, user_id: int) -> float:
    """Calculate win percentage for a user in a league."""
    record = get_record(league_id, user_id)
    return round(record['wins'] / (record['wins'] + record['losses']), 2) 
    
def get_season_records(user_id: int, year: int) -> list[dict]:
    """Get user records for a specific season across all leagues."""
    records = []
    leagues = get_nfl_leagues_user_metadata(user_id, year)
    for league in leagues:
        record = get_record(league['league_id'], user_id)
        record['league_name'] = league.get('name')
        record['user_id'] = user_id
        record['league_id'] = league.get('league_id')
        records.append(record)
    return records

# def get_pf_pa(league_id, user_id):
#     """Get points scored and points against for a user."""
    
#     for roster in get_league_rosters(league_id):
#         if roster.get('owner_id') == str(user_id):
#             roster_id = roster.get('roster_id')
#             break
    
#     pf, pa = 0, 0
#     for week in range(1, 19):
#         performances = get_team_performances(league_id, week)
#         for performance in performances:
#             matchup_id = performance.get('matchup_id')
#             if matchup_id:
#                 if performance.get('roster_id') == roster_id:
#                     pf += performance['points']
#                     break
#         for performance in performances:
#             if performance.get('matchup_id') == matchup_id:
#                 pa += performance['points']
#                 break
                
#     ratio = round(pf / pa, 2) if pa != 0 else 'N/A'
#     return {'points_for': round(pf, 2), 'points_against': round(pa, 2), 'ratio': ratio}
