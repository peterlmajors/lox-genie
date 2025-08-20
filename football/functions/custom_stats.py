import pandas as pd

# Player Total Snaps, Pct Played, and Snaps Per Game
def calc_snap_pct_snap_pg(snaps: pd.DataFrame, positions = list[str]) -> pd.DataFrame:
    
    grouped_snaps = snaps.groupby(['pfr_player_id']).agg({'offense_snaps': 'sum','offense_pct': 'mean', 
                                        'position': 'first', 'game_id': 'nunique'}).reset_index()

    # Calculate snaps_p/g, remove less than 5% of snaps, only QB, RB, WR, TE
    grouped_snaps['snaps_p/g'] = grouped_snaps['offense_snaps'] / grouped_snaps['game_id']
    grouped_snaps = grouped_snaps[grouped_snaps['offense_pct'] >= 0.05]
    grouped_snaps = grouped_snaps[grouped_snaps['position'].isin(positions)]
    
    return grouped_snaps