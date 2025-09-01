import httpx
import json
import pandas as pd
from fastapi import APIRouter, HTTPException
from services.genie.core.config import settings

router = APIRouter()


@router.get("/rankings")
async def get_rankings(
    dynasty: bool = False,
    superflex: bool = True,
    teams: int = 10,
    ppr: float = 1,
    top_n: int = 10,
):
    """
    Get rankings from Fantasy Calc API
    Args:
        dynasty: bool = False
        superflex: bool = True
        teams: int = 10
        ppr: float = 1
        top_n: int = 10
    Returns:
        list[dict]: List of rankings
    """
    try:
        dynasty = "false" if not dynasty else "true"
        qb_count = "2" if superflex else "1"

        # Fetch data from Fantasy Calc API
        resp = httpx.get(
            f"https://api.fantasycalc.com/values/current?isDynasty={dynasty}&numQbs={qb_count}&numTeams={teams}&ppr={ppr}&includeAdp=true"
        )
        if resp.status_code == 200:
            resp_str = resp.content.decode("utf-8")
            resp_json = json.loads(resp_str)
            df_fc = pd.DataFrame(resp_json)

            # Extract name and sleeperId columns
            df_fc["name"] = df_fc.iloc[:, 0].apply(
                lambda x: x.get("name") if isinstance(x, dict) else None
            )
            df_fc["sleeperId"] = df_fc.iloc[:, 0].apply(
                lambda x: x.get("sleeperId") if isinstance(x, dict) else None
            )
            cols = ["name", "sleeperId"] + [
                col
                for col in df_fc.columns
                if col not in ["name", "sleeperId", "player"]
            ]
            df_fc = df_fc[cols]

            # Drop unnecessary columns
            df_fc.drop(
                columns=[
                    "maybeMovingStandardDeviationPerc",
                    "maybeMovingStandardDeviationAdjusted",
                    "displayTrend",
                    "maybeOwner",
                    "starter",
                    "maybeTier",
                    "maybeAdp",
                    "maybeTradeFrequency",
                    "maybeMovingStandardDeviation",
                    "redraftDynastyValueDifference",
                    "redraftDynastyValuePercDifference",
                ],
                inplace=True,
            )
            df_fc.rename(columns={"name": "player"}, inplace=True)
            df_fc = df_fc[~df_fc["player"].str.contains(r" Pick | Round ", regex=True)]

            return df_fc.to_dict(orient="records")[:top_n]
        else:
            raise Exception(
                f"Failed to fetch data from Fantasy Calc API: {resp.status_code}"
            )
    except Exception as exc:
        raise HTTPException(
            status_code=502, detail=f"Failed to fetch rankings from get_rankings: {exc}"
        )
