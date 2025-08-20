import json
import pandas as pd
import httpx
from football.external.utils import check_local_relevant


def get_fantasy_calc_rankings(dynasty: bool = False, superflex: bool = True, teams: int = 10, ppr: float = 1) -> pd.DataFrame:
    
    dynasty = 'false' if not dynasty else 'true'
    qb_count = '2' if superflex else '1'
    rel_path = f'../../data/2025/fantasy_calc/{dynasty}_{qb_count}_{teams}_ppr_{ppr}.csv'
    if check_local_relevant(rel_path):
        return pd.read_csv(rel_path)
    
    print("Fetching Fantasy Calc rankings from API...")
    resp = httpx.get(f'https://api.fantasycalc.com/values/current?isDynasty={dynasty}&numQbs={qb_count}&numTeams={teams}&ppr={ppr}&includeAdp=true')
    if resp.status_code != '200':

        resp_str = resp.content.decode('utf-8')
        resp_json = json.loads(resp_str)
        df_fc = pd.DataFrame(resp_json)

        df_fc['name'] = df_fc.iloc[:, 0].apply(lambda x: x.get('name') if isinstance(x, dict) else None)
        df_fc['sleeperId'] = df_fc.iloc[:, 0].apply(lambda x: x.get('sleeperId') if isinstance(x, dict) else None)
        cols = ['name', 'sleeperId'] + [col for col in df_fc.columns if col not in ['name', 'sleeperId', 'player']]
        df_fc = df_fc[cols]

        df_fc.drop(columns=['maybeMovingStandardDeviationPerc', 'maybeMovingStandardDeviationAdjusted', 'displayTrend', 
            'maybeOwner', 'starter', 'maybeTier', 'maybeAdp', 'maybeTradeFrequency', 'maybeMovingStandardDeviation',
            'redraftDynastyValueDifference', 'redraftDynastyValuePercDifference'], inplace=True)
        df_fc.rename(columns={'name': 'player'}, inplace=True)
        df_fc = df_fc[~df_fc['player'].str.contains(r' Pick | Round ', regex=True)]
        
        df_fc.to_csv(rel_path, index=False)
        print(f"Fantasy Calc data saved to: {rel_path}")
        return df_fc
    else: 
        raise Exception(f"Failed to fetch data from Fantasy Calc API: {resp.status_code}")
    