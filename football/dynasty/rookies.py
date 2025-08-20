import polars as pl
from nfl_data_py import import_draft_picks

def _load_rookie_data(rel_path: str, df: pl.DataFrame) -> pl.DataFrame:
    """Load and join rookie data with draft information."""
    late_round_rookies = pl.read_csv(rel_path)
    rookies = df.join(late_round_rookies, on=["player", "position"], how="inner")

    df_dp = import_draft_picks([2025])
    draft = pl.from_pandas(
        df_dp[df_dp["position"].isin(["QB", "WR", "TE", "RB"])][
            ["round", "pick", "pfr_player_name", "position"]
        ]
    ).rename({"pfr_player_name": "player"})
    rookies = rookies.join(draft, on=["player", "position"], how="left")

    return rookies


def _calculate_costs_and_surplus(rookies: pl.DataFrame) -> pl.DataFrame:
    """Calculate IFL costs and surplus for rookies."""
    round_ifl_cost = {1: 82, 2: 32, 3: 20, 4: 18, 5: 15, 6: 13, 7: 10}
    
    rookies = rookies.with_columns(
        pl.col("round")
        .map_elements(lambda x: round_ifl_cost.get(x, 0), return_dtype=pl.Int64)
        .alias("ifl_cost_yr1")
    )
    rookies = rookies.with_columns(
        [
            (pl.col("auction_late_round") - pl.col("ifl_cost_yr1")).alias(
                "late_round_surplus_yr1"
            ),
            (pl.col("ifl_cost_yr1") * 1.18)
            .round(0)
            .cast(pl.Int64)
            .alias("ifl_cost_yr2"),
        ]
    )
    return rookies


def _calculate_pr_yr2(
    rookies: pl.DataFrame, df: pl.DataFrame
) -> pl.DataFrame:
    """Calculate positional rank for year 2 based on positive surplus."""
    positional_ranks = []
    for rookie_row in rookies.to_dicts():
        pos = rookie_row["position"]
        cost_yr2 = rookie_row["ifl_cost_yr2"]
        surplus_yr1 = rookie_row["late_round_surplus_yr1"]

        # Only calculate positional rank if surplus is positive
        if surplus_yr1 > 0:
            df_pos = df.filter(
                (pl.col("position") == pos)
                & (pl.col("auction_late_round").is_not_null())
            ).sort("pr_late_round")
            if df_pos.height == 0:
                positional_ranks.append(None)
            else:
                diffs = (df_pos["auction_late_round"] - cost_yr2).abs()
                min_idx = diffs.arg_min()
                # Get the actual pr_late_round value instead of the index
                positional_ranks.append(df_pos["pr_late_round"][min_idx])
        else:
            positional_ranks.append(None)

    rookies = rookies.with_columns(pl.Series("pr_yr2", positional_ranks))
    return rookies


def _calculate_breakeven_costs(rookies: pl.DataFrame) -> pl.DataFrame:
    """Calculate breakeven costs for rookies with negative surplus."""
    rookies = rookies.with_columns(
        pl.when(pl.col("late_round_surplus_yr1") < 0)
        .then(
            (
                (pl.col("late_round_surplus_yr1").abs() * 1.1)
                .round(0)
                .cast(pl.Int64)
                + pl.col("ifl_cost_yr2")
            )
        )
        .otherwise(pl.col("ifl_cost_yr2"))
        .alias("ifl_cost_yr2_breakeven")
    )
    return rookies


def _calculate_positional_rank_breakeven(
    rookies: pl.DataFrame, df: pl.DataFrame
) -> pl.DataFrame:
    """Calculate positional rank for breakeven scenarios."""
    positional_ranks_breakeven = []
    for rookie_row in rookies.to_dicts():
        pos = rookie_row["position"]
        cost_yr2_breakeven = rookie_row["ifl_cost_yr2_breakeven"]
        surplus_yr1 = rookie_row["late_round_surplus_yr1"]

        # Only calculate positional rank if surplus is negative
        if surplus_yr1 <= 0:
            df_pos = df.filter(
                (pl.col("position") == pos)
                & (pl.col("auction_late_round").is_not_null())
            ).sort("pr_late_round")
            if df_pos.height == 0:
                positional_ranks_breakeven.append(None)
            else:
                diffs = (df_pos["auction_late_round"] - cost_yr2_breakeven).abs()
                min_idx = diffs.arg_min()
                # Get the actual pr_late_round value instead of the index
                positional_ranks_breakeven.append(df_pos["pr_late_round"][min_idx])
        else:
            positional_ranks_breakeven.append(None)

    rookies = rookies.with_columns(
        pl.Series("pr_yr2_breakeven", positional_ranks_breakeven)
    )
    return rookies


def _cleanup_columns(rookies: pl.DataFrame) -> pl.DataFrame:
    """Remove unnecessary columns from the final dataset."""
    rookies = rookies.drop(
        [
            "auction_fantasy_calc",
            "redraft_value",
            "sleeper_id",
            "round",
            "ifl_cost_yr2_breakeven",
            "overall_fantasy_calc",
        ]
    )
    return rookies


def merge_rookies(rel_path: str, df: pl.DataFrame) -> pl.DataFrame:
    """Main function to merge and process rookie data."""
    rookies = _load_rookie_data(rel_path, df)
    rookies = _calculate_costs_and_surplus(rookies)
    rookies = _calculate_pr_yr2(rookies, df)
    rookies = _calculate_breakeven_costs(rookies)
    rookies = _calculate_positional_rank_breakeven(rookies, df)
    rookies = _cleanup_columns(rookies)

    return rookies