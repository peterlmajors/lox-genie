import pandas as pd
import nfl_data_py as nfl
from utils import calc_fantasy_points


def import_seasons_rosters_ids(seasons: list[int]):
    
    stats = nfl.import_seasonal_data(seasons, "REG")
    stats.rename({'player_id': 'gsis_id', 'wopr_x': 'wopr_1', 'wopr_y': 'wopr_2',
                  'tgt_sh': 'target_share_1', 'target_share': 'target_share_2'}, axis = 1, inplace = True)

    rosters = nfl.import_rosters(seasons)
    rosters.rename({'player_id': 'gsis_id'}, axis = 1, inplace = True)
    rosters.drop(columns=['espn_id','sportradar_id', 'yahoo_id', 'rotowire_id', 'pff_id', 'pfr_id', 
                'fantasy_data_id', 'sleeper_id', 'status_description_abbr', 'football_name'], inplace=True)

    ids = nfl.import_ids()
    ids.rename({'name': 'player_name'}, axis = 1, inplace = True)
    ids.drop(['db_season', 'twitter_username', 'height', 'weight', 'college', 'merge_name', 'position', 'team'], axis=1, inplace=True)
    
    return stats, rosters, ids


def merge_stats_rosters_ids(stats: pd.DataFrame, rosters: pd.DataFrame, ids: pd.DataFrame):

    # Stats, IDs and Rosters ----------------------------------
    
    # Merge Player Name onto Stats DataFrame, Place in Front
    stats = stats.merge(ids[['player_name','gsis_id']], on = 'gsis_id', how = 'left')
    cols = ['player_name'] + [col for col in stats.columns if col not in ['player_name']]
    stats = stats[cols]
    
    # Merge Position onto Stats DataFrame, Place in Front
    stats = stats.merge(rosters[['position', 'season', 'gsis_id']], on = ['gsis_id','season'], how = 'left')
    stats = stats[stats['position'].isin(['QB', 'RB', 'WR', 'TE'])]

    # IDs and Rosters ----------------------------------------
    
    # Move IDs in Rosters DF to IDs DF, Ensure No Duplicate IDs Following Merge
    ids = ids.merge(rosters[['gsis_id', 'esb_id', 'gsis_it_id', 'smart_id']], on = 'gsis_id', how = 'left')
    ids.drop_duplicates(subset = ['gsis_id'], inplace = True)
    rosters.drop(columns = ids.columns[-3:], inplace = True)

    # Move Birthday, Age and Draft Info in Rosters DF to IDs DF  
    rosters = rosters.merge(ids[['gsis_id', 'birthdate', 'age', 'draft_year', 'draft_round', 'draft_pick', 'draft_ovr']], on = 'gsis_id', how = 'left')
    ids.drop(columns = rosters.columns[-6:], inplace = True)
    
    # Bios and Rosters ----------------------------------------
    
    # Split Rosters DF into two DataFrames, One with Static Player Info, One with Seasonal Roster Info
    # bio = rosters[['gsis_id', 'player_name', 'first_name', 'last_name', 'age', 'birthdate', 'height', 'weight', 'college', 
    #                'draft_year', 'draft_round', 'draft_pick', 'draft_ovr', 'entry_year', 'rookie_year', 'draft_club']]    
    # rosters.drop(columns = bio.columns[2:] , inplace = True)
    # rosters.drop(columns = ['status', 'week', 'game_type', 'birth_date', 'draft_number'], inplace = True)
    
    # # Drop Duplicate IDs in Bio DF Since Data Not Seasonal
    # bio = bio.drop_duplicates().copy()
    
    return stats, rosters, ids
    
    
def reorder_columns(stats: pd.DataFrame, rosters: pd.DataFrame, ids: pd.DataFrame):
    
    # Reorder Columns ----------------------------------------
    stats_col_order = ["player_name", "gsis_id", "season", "position", "season_type", "team", "games", "completions", "attempts", 
                   "passing_yards", "passing_tds", "interceptions", "sacks", "sack_yards", "sack_fumbles", "sack_fumbles_lost", 
                   "passing_air_yards", "passing_epa", "pacr", "dakota", "passing_yards_after_catch", "passing_first_downs", 
                   "passing_2pt_conversions", "carries", "rushing_yards", "rushing_tds", "rushing_fumbles", "rushing_fumbles_lost",
                   "rushing_first_downs", "rushing_2pt_conversions", "ry_sh", "rtd_sh", "rfd_sh", "rtdfd_sh", "rushing_epa",
                   "targets", "receptions", "receiving_yards", "receiving_tds", "receiving_fumbles", "receiving_fumbles_lost", 
                   "receiving_air_yards", "receiving_yards_after_catch", "receiving_first_downs", "receiving_2pt_conversions", 
                   "target_share_1", "target_share_2", "ay_sh", "air_yards_share", "yac_sh", "racr", "receiving_epa", "wopr_1", 
                   "wopr_2", "dom", "w8dom", "yptmpa", "special_teams_tds", "ppr_sh", "fantasy_points", "fantasy_points_ppr"]
    rosters_col_order = ["player_name", "gsis_id", "season", "team", "jersey_number", "position", 
                    "depth_chart_position", "ngs_position", "years_exp", "headshot_url"]
    # bios_col_order = ["gsis_id", "player_name", "first_name", "last_name", "age", "birthdate", "height", "weight", 
    #                 "college", "entry_year", "rookie_year", "draft_year", "draft_round", "draft_pick", "draft_ovr", "draft_club"]
    
    # Organize stats columns --------------------------------
    existing_columns = [col for col in stats_col_order if col in stats.columns]
    remaining_columns = [col for col in stats.columns if col not in stats_col_order]
    stats = stats[existing_columns + remaining_columns]
    
    # Organize rosters columns --------------------------------
    existing_columns = [col for col in rosters_col_order if col in rosters.columns]
    remaining_columns = [col for col in rosters.columns if col not in rosters_col_order]
    rosters = rosters[existing_columns + remaining_columns]
    
    # Organize ids columns --------------------------------
    id_cols = ['gsis_id', 'player_name'] + [col for col in ids.columns if col not in ['gsis_id', 'player_name']]
    ids = ids[id_cols]
    
    # Organize bio columns --------------------------------
    # bio = bio[bios_col_order]
    
    return stats, rosters, ids


def update_stats(first: int = 2001, last: int = 2024):

    stats, rosters, ids = import_seasons_rosters_ids(list(range(first, last + 1)))
    stats, rosters, ids = merge_stats_rosters_ids(stats, rosters, ids)
    stats, rosters, ids = reorder_columns(stats, rosters, ids)
    stats = calc_fantasy_points(stats)

    stats.to_csv('../../data/2025/stats.csv', index = False)
    rosters.to_csv('../../data/2025/rosters.csv', index = False)
    ids.to_csv('../../data/2025/ids.csv', index = False)
 
   
update_stats()