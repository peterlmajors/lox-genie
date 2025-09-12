from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate(
    template="""
        <rate_statistics>
        - Season Points can be misleading because it is a cumulative stat and does not account for the number of games a player played.
        - PPG (Points Per Game) can be misleading because it does not account for the number of snaps a player played.
        </rate_statistics>

        <player_cost_analysis>
        - Value Over Replacement Player (VORP) is a measure of a player's value compared to the average player at their position
        - VORP can vary drastically by league depending on number of teams, starting lineup requirements, and scoring settings
        - PPG ADP expectation is the VORP expectation for a player at their Average Draft Position (ADP).
        </player_cost_analysis>

        <quarterback>
        - Elite, proven dual-threat QBs are worth early picks mainly in leagues with 10 teams or less.
        - In leagues with 10 or more teams, early RB/WR scarcity makes waiting on QB a superior strategy.
        - Outside the top tier, mobility is the tiebreaker: aim for ≥ ~2 rushing fantasy points per game or clear designed-rush usage.
        - QB rushing FPPG is highly predictive year-over-year (YoY) while passing FPPG is not predictive at all YoY
        - TD rate regresses: do not pay up for mid-tier QBs coming off inflated TD% (~>6%); hunt value in capable passers whose TD% was artificially low last year.
        - Second-year starters with legs are prime mid/late-round targets; they deliver cheap upside and year-two jumps.
        - For late darts (and superflex depth), lean on fantasy points per dropback + rushing to spot breakout efficiency.
        - Evaluate per-game stats using ≥90% team pass-attempt share to avoid partial-game bias.
        - Weigh scheme/OC changes, supporting cast, and OL health—use them to adjust, not replace, the core signals.
        - Always craft a contingency: pair a mid/late QB with an upside runner or favorable early schedule, and be ready to stream quickly.
        </quarterback>

        <running_back>
        - Running back evaluation is role-driven (snaps, routes, goal-line carries), skill-measured (evasion and vision), and context-driven (injuries, teammate competition, scheme fit)
        - Metrics like ROE%, RYOE, YPRR help separate system-driven producers from those creating value independently.
        - Dynasty managers should anchor evaluations in tiers to reflect both current production and future volatility.
        - Receiving drives early-round RB value: prioritize prior-year receiving PPG and pass-down usage for your RB1.
        - Context multiplies talent: target clear lead roles (low RB competition by ADP) on high-scoring offenses.
        - Do not chase last points scored last year in the middle rounds; use YPRR and target share indicators to find undervalued volume.
        - Late rounds = role + contingency: pass-catching chops and obvious paths to a takeover beat empty handcuffs; age is not a deal-breaker this late.
        - Injury luck swings prices: after healthy RB seasons, expect overpricing next year—shift capital to mid-round RB
        - Always weigh opportunity cost: adjust RB aggressiveness by league size, scoring, and what you give up at WR/TE/QB
        - High-end RBs are worth early picks in leagues with 10 teams or less.
        </running_back>

        <wide_receiver>

        </wide_receiver>

        <tight_end>
        - Red Zone Target Share (RZTGT%) is a consideration when evaluating the connection between a QB and pass catcher
        </tight_end>

        <defense>
        </defense>

        <kicker>
        </kicker>
        
        <team_building_strategy>
        - Zero-RB strategy: identify cheap RBs with contingent upside and monitor weekly shifts to capture value early.
        - Middle-round RB strategy: focus on ambiguous backfields where one back can consolidate; fade older, non-pass-catching profiles at mid costs.
        </team_building_strategy>
        
        <team_tendencies_and_situation>
        - Pace of Play projections are a relevant when understanding the number of opportunities a team’s offense will have each game to score fantasy points
        - Pass Rate Over Expectation (PROE) is relevant at the extremes and is influenced by offensive coordinators or player callers, which explains team passes and rushes per game
        - Strength of Schedule (SoS) matters most at the extremes. Difficult SoS means more negative game scripts and higher pass volume, while easy SoS means more positive game scripts and higher run volume
        </team_tendencies_and_situation>

        <teammate_competition>
        - For WRs and RBs, teammate competition as measured by distance of ADP, Ranking, or VoRP should be an important consideration
        </teammate_competition>

        <injury_advice>
        - Players who miss significant time in the preseason (multiple weeks) rarely exceed PPG ADP expectation
        </injury_advice>

        <dynasty_strategy>
        - In dynasty leagues, talent is more important than situation because situation changes faster than talent appreciates or degrades`
        </dynasty_strategy>
    """,
    input_variables=["current_date"],
)