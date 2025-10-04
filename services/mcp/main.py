
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

from services.mcp.tools.sleeper_draft import get_all_draft_picks_metadata, get_league_picks
from services.mcp.tools.sleeper_league import get_league_rosters_metadata, get_users_teams
from services.mcp.tools.sleeper_team import get_user_roster, get_user_record, get_waiver_budget
from services.mcp.tools.sleeper_user import get_nfl_leagues_user_metadata, get_current_league_records, get_previous_league_records
# from services.mcp.tools.reddit import reddit_search

from services.mcp.resources.quarterbacks import quarterbacks

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

mcp_resources = [
    quarterbacks,
    # "data://runningbacks",
    # "data://wide_receivers",
    # "data://tight_ends",
    # "data://kickers",
    # "data://defense",
    # "data://special_teams",
]

mcp = FastMCP(
    name = "lox-mcp",
    tools = mcp_tools
)

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> PlainTextResponse:
    return PlainTextResponse("OK")

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8001)