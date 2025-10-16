from services.mcp.main import mcp

@mcp.resource("data://quarterback_strategy")
def quarterback_strategy() -> str:
    """Provides information about quarterback strategy."""
    return """
        # Quarterback Strategy: 
    """

    # - Quarterback Strategy:
    #     - Superflex Specific Strategy:
    #         - Elite, proven dual-threat QBs are always the most valuable assests because:
    #             - They provide real value above replacement level at their position (~5 points per game)
    #             - Their variance in points per game is lower than other positions.
    #             - Quarterbacks are less injury prone than other positions.
    #             - They are not affected as much by teammate injuries.
                
    #     - Non-Superflex Specific Strategy:
    #         - Elite, proven dual-threat QBs are still valuable, but not as much as in superflex.
    #         - If you don't get one of the elite, proven dual-threat QBs (Josh Allen, Lamar Jackson, Jayden Daniels) wait until later rounds.
        
    #     - Statistical Signals:
    #         - Value Over Replacement Player (VORP) vs Average Draft Position (ADP) Curve:
    #             - There is a steep drop off in VORP following the first few players, but levels off quickly.
    #             - Opportunity cost of taking a mid-tier QB is generally higher than a mid-tier RB or WR.
    #         - Rushing points per game:
    #             - Is highly predictive year-over-year and should be heavily weighed.
    #             - Mobility is a good tiebreaker when deciding between two QBs ranked similarly.
    #             - Aim for QBs with ≥ ~2 rushing points per game or clear designed-rush usage.
    #         - Passing points per game:
    #             - Is not predictive year-over-year at all.
    #             - Can be skewed by reciever talent, offensive line play and game script.
    #         - Touchdowns per pass attempt (TD%):
    #             - Regresses heavily year-over-year and is not predictive.
    #             - Do not pay up for mid-tier QBs coming off inflated TD% (~>6%).
    #             - Hunt value in capable passers whose TD% was artificially low last year.
    #         - Points per dropback (PPD):
    #             - An efficiency metric that is moderately predictive of future production.
    #             - Useful as a tiebreaker when deciding between late round QBs.

    #     - Common Phenomena:
    #         - Second-year starters with rushing ability:
    #             - Consistently outperform their expected fantasy production, according to their ADP when drafted in mid/late rounds.
    #             - They deliver cheap upside and often experience year-two jumps in real-life and fantasy production.      

    #     - Tie Breakers:     
    #         - Offensive line play
    #         - Offensive line health
    #         - Whether the play-calling scheme is conducive to QB fantasy production
    #         - Wide receiver talent, which can be easily measured by ADP.    
    # """