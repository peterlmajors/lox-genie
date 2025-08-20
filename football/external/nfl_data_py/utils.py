import pandas as pd

def calc_fantasy_points(df: pd.DataFrame, scoring: str = 'ppr') -> pd.DataFrame:
    
    df = df.copy()
    scoring = {'receptions': 0, 'receiving_tds': 6, 'receiving_yards': 0.1, 'rushing_tds': 6,
               'rushing_yards': 0.1, 'passing_yards': .04, 'passing_tds': 4, 'interceptions': -1,
               'passing_2pt_conversions': 2, 'receiving_2pt_conversions': 2, 'rushing_2pt_conversions': 2,
               'receiving_fumbles_lost': -2, 'rushing_fumbles_lost': -2, 'sack_fumbles_lost': -2, 
               'receptions': 1}

    df['fantasy_points_calc'] = df.apply(lambda row: sum(row[col] * scoring[col] for col in scoring), axis=1)
    
    return df


def ppg_leaders_top_20(stats: pd.DataFrame, min_games: int = 8) -> pd.DataFrame:

    # Filter players who played more than 8 games
    qual_stats = stats[stats['games'] > min_games]

    # Calculate PPR points per game and rank within each season/position
    qual_stats = qual_stats.copy()
    qual_stats.loc[:, 'ppr_ppg'] = round(qual_stats['fantasy_points_ppr'] / qual_stats['games'], 1)
    qual_stats.loc[:, 'ppr_ppg_rank'] = qual_stats.groupby(['season', 'position'])['ppr_ppg'].rank(method='min', ascending=False)

    # Select relevant columns and aggregate by player/season/position
    col = ['player_name', 'gsis_id',  'season', 'position', 'fantasy_points_ppr', 'ppr_ppg', 'ppr_ppg_rank']
    ppg_l = (
        qual_stats[col]
        .groupby(['player_name', 'gsis_id', 'season', 'position'])
        .sum()
        .reset_index()
        .sort_values(by='ppr_ppg', ascending=False)
    )

    # For each position and rank (top 20), compute mean PPR PPG and export to CSV
    ppg_leaders_top_20 = (
        ppg_l[ppg_l['ppr_ppg_rank'] < 20]
        .groupby(['position', 'ppr_ppg_rank'])
        .agg({'ppr_ppg': 'mean'})
        .reset_index()
    )
    ppg_leaders_top_20.to_csv('../../data/2025/ppg_leaders_top_20.csv')
    return ppg_leaders_top_20