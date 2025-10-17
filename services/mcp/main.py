
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

from services.mcp.tools.sleeper_draft import get_all_draft_picks_metadata, get_league_picks
from services.mcp.tools.sleeper_league import get_league_rosters_metadata, get_users_teams
from services.mcp.tools.sleeper_team import get_user_roster, get_user_record, get_waiver_budget
from services.mcp.tools.sleeper_user import get_nfl_leagues_user_metadata, get_current_league_records, get_previous_league_records
# from services.mcp.tools.reddit import reddit_search

# from services.mcp.resources.quarterbacks import quarterback_strategy
# from services.mcp.resources.runningbacks import runningback_strategy
# from services.mcp.resources.widerecievers import wide_reciever_strategy
# from services.mcp.resources.tightends import tightend_strategy
# from services.mcp.resources.kickers import kicker_strategy
# from services.mcp.resources.defense import defense_strategy
# from services.mcp.resources.psychology import psychology
# from services.mcp.resources.terminology import terminology

mcp_tools = [
    get_all_draft_picks_metadata,
    get_league_picks,
    get_league_rosters_metadata,
    get_users_teams,
    get_user_roster,
    get_user_record,
    get_waiver_budget,
    get_nfl_leagues_user_metadata,
    get_current_league_records,
    get_previous_league_records,
    # reddit_search
]

# mcp_resources = [
#     quarterback_strategy,
#     runningback_strategy,
#     wide_reciever_strategy,
#     kicker_strategy,
#     defense_strategy,
#     psychology,
#     terminology,
# ]

mcp = FastMCP(
    name = "lox-mcp",
    tools = mcp_tools
)

@mcp.resource("data://{name}")
def resource(name: str) -> str:
    """Provides the resource content."""
    with open(f"services/mcp/resources/{name}.md", "r") as file:
        return file.read()

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> PlainTextResponse:
    return PlainTextResponse("OK")

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8001, path="/mcp")