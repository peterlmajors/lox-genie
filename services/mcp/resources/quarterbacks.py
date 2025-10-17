# from services.mcp.main import mcp

# @mcp.resource("data://quarterbacks")
# def quarterback_strategy() -> str:
#     """Provides information about quarterback strategy."""
#     return """
#         # Tiered Strategy:
#         - Elite, proven dual-threat QBs are always the most valuable assests:
#             - Provide material value above replacement level at their position (~4 points per game)
#             - They are not as affected by teammate injuries or fluctuations in performance
#             - They are less injury prone than other positions
#         - Mid-tier QBs:
#             - Should generally be avoided at cost unless they provide a proven rushing floor
#             - Opportunity cost of taking a mid-tier QB is generally higher than a mid-tier RB or WR.
#         - Lower-tier QBs:
#             - Target statistical signals to identify value in this ambiguous tier:
#                 - An existing rushing floor
#                 - Recent drop in price due to low TD%

#         # Relevant Metrics:
#         - Rushing Points per Game (RPPG):
#             - Highly predictive year-over-year and should be heavily weighed
#         - Passing Points per Game (PPPG):
#             - Is not predictive year-over-year at all
#             - Can be skewed by reciever talent, offensive line performance and game script
#         - Touchdowns per Pass Attempt (TD%):
#             - Regresses heavily year-over-year and is not predictive
#             - Do not pay up for mid-tier QBs coming off inflated TD% (~>6%)
#             - Hunt value in capable passers whose TD% was artificially low last year
#         - Points per Dropback (PPDB):
#             - An efficiency metric that is moderately predictive of future production
#             - Useful as a tiebreaker when deciding between late round QBs

#         # Context Driven Evaluation:
#         - Offensive Line Performance and Health:
#             - Without a competent offensive line to provide the QB with time to throw, he will have a difficult gaining points through the air
#     """