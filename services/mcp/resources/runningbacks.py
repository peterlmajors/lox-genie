
# from services.mcp.main import mcp

# @mcp.resource("data://runningback_strategy")
# def runningback_strategy() -> str:
#     """Provides information about running back strategy."""
#     return """
#         # Common Terms and Abrreviations:
#         - RB = Running Back
#         - RB1 = In the context of an NFL roster, the starting running back. In the context of an individual fantasy team, an RB ranking roughly between 1st and 12th in rest of season rankings.
#         - RB2 = In the context of an NFL roster, the backup running back. In the context of an individual fantasy team, an RB ranking roughly between 13th and 24th in rest of season rankings.

#         # Role Driven Evaluation:
#         - Running back evaluation is inherently role driven.
#         - Running back roles are highly volatile, and can change week to week based on: 
#             - Injuries to other running backs on the same roster.
#             - The emergence of younger, more productive running back teammates.
#             - The decline of older, less productive running back teammates.
#         - Being able to understand a player's future snap share and recieving target share is crucial to evaluating their future fantasy production. 

#         # Skill-Based Evaluation:
#         - Rushing Yards over Expectation (RYOE): Excellent measure of a running back's ability to defy rushing efficiency expectation, based on player tracking data.
#         - Yards per Route Run (YPR): Captures ability to get open in space, avoid tackles to gain yardage, and is a leading indicator that an RB will have receiving production moving forward.
#         - Yards per Carry After Contact (YAC/AC): A measure of an RB's ability to gain yards after contact, which somewhat normalizes the impact of the offensive line.
#         - Target Share (TGT%): A display of an RB's recieving production, an indicator of recieving production in the short term.

#         # Context-Driven Evaluation:
#         - Offensive Line Play: 
#             - A running back's ability to gain fantasy points via rushing yards is heavily influenced by the offensive line play.
#                 - Being 'stuffed' behind the line of scrimmage c
#         - Injuries: 
#             - Injury to another running back on the same roster should open up more opportunities for the healthy running back, especially if the healthy back was lower on the depth chart.
#             - Injury to the starting quarterback will likely decrease the offensive's production, limiting the running back's opportunities for touchdowns and rush attempts as the team will be in more passing situations.
#         - Teammate Competition: 
#             - A roster with multiple healthy, capable running backs usually limits the opportunities each player recieves.
#             - A roster with multiply health, but not especially talented running backs is called an "ambiguious backfield".
#                 - Running backs in an ambiguious backfield are often undervalued by the market, as it is difficult to predict which back will emerge with opportunities.
#         - Offensive Scheme: 
#             - Teams who tend to run the ball more often (as measured by Pass Rate Over Expectation (PROE)) provide greater opportunity for running backs in terms of rushing attempts and touchdowns.
#             - Playcallers who put players in positions to positions to maximize their talents can improve their fantasy production.
#                 - Examples:
#                     - A playcaller who schemes for outside zone runs joins a team with a running back who excels at them, and a strong tackle to secure the edge.
#                     - Speedy reciever who is not the strongest route runner being targeted behind the line of scrimmage, who can use his speed to gain yards after the catch.
    
#         # Recieving Production:
#         - Receiving production is a vital part of running back evaluation.
#         - Running backs who do not recieve many targets need to be reliant on touchdown scoring, which can be volatile and subject to the rest of the team's offensive production.
#         - The average fantasy point per receiving target of 1.4 is more than twice as high as the average fantasy point per rushing attempt of 0.6.

#         # Early Down vs Third Down RBs:
#         - Early down running backs handle most rushing attempts on first and second downs, benefiting from volume and touchdown opportunities but lacking significant receiving work.
#         - Third down running backs handle most passing situations, evidenced by higher target shares; they offer some PPR value but usually see fewer carries and less goal line work.
#         - In many offenses, the early down vs third down running back roles are clearly delineated, but the best RBs combine both early down and third down duties, leading to top-tier fantasy production.
        
#         # Types of Rush Attempts:
#         - Outside Run Rate (ORR) is a good indicator of a running back's potential for success, as these types of rush attempts are more likely to result in big plays.

#         # Goal Line Work:
#         - The percent of goal line carries a running back receives is a relfection of the coaching staff's trust in him.
#         - Goal line carries are extremely valuable, as they provide the opportunity for touchdowns, the most valuable scoring mechanism in fantasy football.
#         - If a running back has been successful in converting goal line carries into touchdowns, he will likely retain this pivotal role in the offense.
#         - If a running back has not been successful in converting goal line carries, he could either regress to the mean conversion rate or be replaced.

#         # Team Contenxt:
#         - Running back value can be heaviliy influenced by the overall offense's projected production.
# """        