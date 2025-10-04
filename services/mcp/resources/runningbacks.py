
from services.mcp.main import mcp

@mcp.resource("data://runningback_strategy")
def runningback_strategy() -> str:
    """Provides the application configuration."""
    return """
        - Running back evaluation is role-driven (snaps, routes, goal-line carries), skill-measured (evasion and vision), and context-driven (injuries, teammate competition, scheme fit)
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