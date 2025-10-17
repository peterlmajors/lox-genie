from services.mcp.main import mcp

@mcp.tool("resource_explorer")
def resource_explorer(query: str) -> str:
    """
    Explore a resource by query.

    Parameters:
        query (str): The query to explore the resource by.
    Example:
        ResourceExplorer("wide_reciever_strategy")
        ResourceExplorer("quarterback_strategy")
        ResourceExplorer("runningback_strategy")
        ResourceExplorer("tightend_strategy")
        ResourceExplorer("kicker_strategy")
        ResourceExplorer("defense_strategy")
        ResourceExplorer("special_teams_strategy")
    Returns:
        A string containing the description of the resource.
    """
    return mcp.resources[query].description