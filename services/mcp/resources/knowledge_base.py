from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate(
    template="""
        <rate_statistics>
        - PPS (Points Per Snap) can be misleading because it does not account for the involvement of the player in the offense.

        </rate_statistics>

        <volume_statistics>
        - While rate statistics are relevant for predicting future production, players who recieve greater targets or rushes provide a higher floor and cannot be ignored.
        - Snaps played, targets, and rushing attempts, are all relevant statistics - which can be influenced by the team's offensive output, scheme, game scripts, and teammate competition.
        - Within individual season, offensive output and teammate competition are more subject to change based on injuries or trades, while scheme will remain more consistent based on coaching staff and personnel.
        - Game scripts can be influenced by the strength of opponent a team has played, as well as the team's own defense - but is strength ofschedule is more influential than the team's own defense.
        - A team that is often down in games will throw more leading to greater potential for recieving and passing volume, while a team that is often up in games will run more to control the clock.
        - For example, a player who receives 25 rush attempts per game in a run-heavy offense with talent around him is valuable regardless of his rate statistics - at least in the short term.
        - For example, a player who run averages 32 routes run and 6 targets per game in a pass-heavy offense with is valuable regardless of his depth of target or red zone involvement because he provides a steady floor.
        </volume_statistics>

        <player_cost_analysis>
        - Value Over Replacement Player (VORP) is a measure of a player's value compared to the average player at their position.
        - VORP can vary drastically by league depending on number of teams, starting lineup requirements, and scoring settings.
        - PPG ADP expectation is the VORP expectation for a player at their Average Draft Position (ADP).
        </player_cost_analysis>

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

        <predictive_statistics>
        - First Downs per Route Run (1stD/RR) and Yards per Route Run (YPR) are the two most predictive statistics for WR fantasy production.
        - PPG (Points Per Game) does not correlate more to rest of season production than average draft position until week 5 or 6 of the season.
        </predictive_statistics>

        <dynasty_strategy>
        - Talent is more important than situation because situation changes faster than talent appreciates or degrades
        - Each year, dynasty teams should either be building for the future or for the present - the worst place to be is stuck in the middle
        </dynasty_strategy>
    """
)