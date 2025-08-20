import polars as pl
from nfl_data_py import import_draft_picks


def _rename_late_round(df: pl.DataFrame) -> pl.DataFrame:

    rename_dict = {
        "AJ Brown": "A.J. Brown",
        "JJ McCarthy": "J.J. McCarthy",
        "CJ Stroud": "C.J. Stroud",
        "TJ Hockenson": "T.J. Hockenson",
        "JK Dobbins": "J.K. Dobbins",
        "Marvin Harrison": "Marvin Harrison Jr",
        "Devonta Smith": "DeVonta Smith",
        "Cam Ward": "Cameron Ward",
        "Josh Palmer": "Joshua Palmer",
        "Demario Douglas": "DeMario Douglas",
    }
  
    df = df.with_columns(pl.col("Player").str.strip_chars().alias("Player"))
    df = df.with_columns(
        pl.col("Player")
        .map_elements(lambda x: rename_dict.get(x, x), return_dtype=pl.Utf8)
        .alias("Player")
    )

    return df


def preprocess_late_round(rel_path: str) -> pl.DataFrame:

    df = pl.read_csv(rel_path)
    df = _rename_late_round(df)
    df = df.drop(["Tier"])
    df = df.rename({"Overall": "overall_late_round", "Pos Rank": "pr_late_round"})
    df = df.rename({col: col.lower() for col in df.columns})
    return df


def preprocess_fantasy_calc(rel_path: str) -> pl.DataFrame:

    df = pl.read_csv(rel_path)
    df = df.drop(["positionRank"])
    df = df.rename(
        {
            "overallRank": "overall_fantasy_calc",
            "redraftValue": "redraft_value",
            "combinedValue": "combined_value",
            "sleeperId": "sleeper_id",
        }
    )
    df = df.rename({col: col.lower() for col in df.columns})
    return df


def create_auction_values(late_round_rankings: pl.DataFrame, fantasy_calc_rankings: pl.DataFrame) -> pl.DataFrame:

    df = late_round_rankings.join(fantasy_calc_rankings, on="player", how="left")

    roster_slots = 10 * 21
    df = df.sort("overall_late_round", descending=False)
    df_rosterable = df.head(roster_slots)

    total_budget = 900 * 10
    total_redraft_value = df_rosterable["redraft_value"].sum()
    df_rosterable = df_rosterable.with_columns(
        [
            (pl.col("redraft_value") / total_redraft_value * total_budget)
            .cast(pl.Int64)
            .alias("auction_fantasy_calc")
        ]
    )

    # Create a mapping dataframe from overall_fantasy_calc to auction_fantasy_calc
    auction_map = df_rosterable.select(
        [pl.col("overall_fantasy_calc"),
        pl.col("auction_fantasy_calc").alias("auction_late_round")]
        ).filter(pl.col("overall_fantasy_calc").is_not_null()).sort("overall_fantasy_calc")


    # Merge auction_late_round onto df_rosterable using overall_late_round <-> overall_fantasy_calc
    df_rosterable = df_rosterable.join(
        auction_map,
        left_on="overall_late_round",
        right_on="overall_fantasy_calc",
        how="left"
    )

    reorder = [
        "player",
        "position",
        "pr_late_round",
        "overall_late_round",
        "overall_fantasy_calc",
        "auction_late_round",
        "auction_fantasy_calc",
        "trend30day",
        "redraft_value",
        "sleeper_id",
    ]
    df_rosterable = df_rosterable.select(
        [col for col in reorder if col in df_rosterable.columns]
    )
    df_rosterable = df_rosterable.with_columns(pl.col("auction_late_round").fill_null(0))
    return df_rosterable

