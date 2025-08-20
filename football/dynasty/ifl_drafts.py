from config import settings
from football.external.sleeper.draft import get_all_draft_picks_metadata
import polars as pl


def get_ifl_draft_metadata(
    league_id: int = str(settings.SLEEPER_IFL_24), year: int = 2024
) -> pl.DataFrame:

    # Rookie Draft
    rookie = get_all_draft_picks_metadata(league_id, 1048193774259703809)
    rookie_df = pl.DataFrame(rookie)
    rookie_df = rookie_df.with_columns(
        [pl.lit(None).alias("drafted"), pl.lit(True).alias("price")]
    )

    # Auction Drafts
    auction_1 = get_all_draft_picks_metadata(league_id, 1128164401430827008)
    auction_2 = get_all_draft_picks_metadata(league_id, 1128136462362361856)
    auction_df = pl.concat([pl.DataFrame(auction_1), pl.DataFrame(auction_2)])

    # Add missing columns to auction_df to match rookie_df structure
    auction_df = auction_df.with_columns(
        [pl.lit(False).alias("drafted"), pl.lit(None).alias("price")]
    )

    # Ensure both dataframes have the same columns in the same order
    common_columns = [col for col in rookie_df.columns if col in auction_df.columns]
    rookie_df = rookie_df.select(common_columns)
    auction_df = auction_df.select(common_columns)

    draft = pl.concat([auction_df, rookie_df])

    draft = draft.with_columns([pl.lit(year).alias("season")])
    draft = draft.with_columns(
        [
            pl.col("price").cast(pl.Float64),
        ]
    )
    draft = draft.with_columns([pl.lit(None, dtype=pl.Int64).alias("years")])
    cols = ["season"] + [col for col in draft.columns if col != "season"]
    draft = draft.select(cols)
    return draft
