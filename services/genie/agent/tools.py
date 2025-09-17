from langchain_core.tools import tool
import requests


@tool
def subreddit_search(query: str, subreddit: str) -> list[dict]:
    """
    Description:
        Search a specific subreddit for information.
    Parameters:
        query (str): The query to search the subreddit for
        subreddit (str): The subreddit to search. Available subreddits include: 'DynastyFF' and 'FantasyFootball'
    Example:
        SubredditSearch("Caleb Williams", "DynastyFF")
    Returns:
        A list of dictionaries, each containing the post data and metadata.
    """
    query = query.replace(" ", "+")
    url = f"https://www.reddit.com/r/{subreddit}/search.json?q=/{query}"

    # Get the response from the subreddit
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    resp = response.json()

    # Parse the response
    posts = []
    for post in resp["data"]["children"][0]:  # TEMP: First post only

        post_data = {}
        fields = [
            ("id", "id"),
            ("url", "url"),
            ("title", "title"),
            ("author", "author"),
            ("selftext", "selftext"),
            ("upvotes", "ups"),
            ("upvote_ratio", "upvote_ratio"),
            ("comments", "num_comments"),
            ("media", "media"),
            ("is_video", "is_video"),
            ("media_only", "media_only"),
        ]
        post_data = {key: post["data"][reddit_key] for key, reddit_key in fields}
        posts.append(post_data)

    return posts
