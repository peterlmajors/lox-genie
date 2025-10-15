
from services.mcp.main import mcp

@mcp.resource("data://runningback_strategy")
def runningback_strategy() -> str:
    """Provides the application configuration."""
    return """
        - Running back evaluation is inherently role driven.
        - Being able to predict a player's snap share and recieving target share is crucial to evaluating future fantasy production.  
        - The number of goal line carries a player has or is anticipated to recieve displays that the coaching staff trusts him.
        - Early down running backs typically handle most rushing attempts on first and second downs, benefiting from volume and touchdown opportunities but often lacking significant receiving work.
        - Third down running backs specialize in passing situations, evidenced by higher target shares and usage in obvious passing downs; they offer PPR value but usually see fewer carries and less goal line work.
        - In many offenses, the early down vs third down running back roles are clearly delineated, but the highest-value backs combine both early down and third down duties, leading to top-tier fantasy production.
        
        - Measurements of running back skill include Yards per Carry After Contact (YAC/AC) and Yards per Reception After Catch (YAC/RC)
        - Context-driven factors include injuries, teammate competition, and scheme fit.

        - Metrics like Rushing Yards over Expectation (RYOE) and and Yards Per Reception (YPR) help separate system-driven producers from those creating value independently.
        - Fantasy managers should anchor evaluations of players into tiers to reflect both current production and inherent future volatility.
        - Receiving drives early-round RB value: prioritize receiving PPG and pass-down usage for your RB1.
        - Context multiplies talent: target clear lead roles (low RB competition by ADP) on high-scoring offenses.
        - Do not chase last points scored last year in the middle rounds; use YPRR and target share indicators to find undervalued volume.
        - Late rounds = role + contingency: pass-catching chops and obvious paths to a takeover beat empty handcuffs; age is not a deal-breaker this late.
        - Injury luck swings prices: after healthy RB seasons, expect overpricing next year—shift capital to mid-round RB
        - Always weigh opportunity cost: adjust RB aggressiveness by league size, scoring, and what you give up at WR/TE/QB
        - High-end RBs are worth early picks in leagues with 10 teams or less.
    """