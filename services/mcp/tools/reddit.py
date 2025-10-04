
from datetime import datetime, timezone
import requests

def reddit_search(query: str, subreddit: str) -> list[dict]:
    """
    Description:
        Search a specific subreddit for information. Available subreddits include: 'DynastyFF' and 'FantasyFootball'
    Parameters:
        query (str): The query to search the subreddit for
        subreddit (str): The subreddit to search.
    Example:
        RedditSearch("Caleb Williams", "DynastyFF")
    Returns:
        A list of dictionaries, each containing the post data and metadata.
    """
    query = query.replace(" ", "+")
    url = f"https://www.reddit.com/r/{subreddit}/search.json?q=/{query}"

    # Get the response from the subreddit
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        resp = response.json()

        # Parse the response
        posts = []
        if "data" in resp and "children" in resp["data"]:
            for post in resp["data"]["children"]:  # Iterate through all posts
                if "data" in post:
                    post_data = {}
                    fields = [
                        ("id", "id"),
                        ("created", "created"),
                        ("url", "url"),
                        ("subreddit", "subreddit"),
                        ("title", "title"),
                        ("selftext", "selftext"),
                        ("upvotes", "ups"),
                        ("upvote_ratio", "upvote_ratio"),
                        ("comments", "num_comments"),
                        # ("media", "media"),
                        ("is_video", "is_video"),
                        ("media_only", "media_only"),
                    ]
                    try:
                        post_data = {key: post["data"].get(reddit_key, "") for key, reddit_key in fields}
                        post_data["created"] = datetime.fromtimestamp(post_data["created"], tz=timezone.utc).strftime("%B %d, %Y %H:%M UTC")
                        posts.append(post_data)
                    except Exception as e:
                        print(f"Error parsing post data: {e}")
                        continue
        else:
            print("No data found in Reddit response")
            
        return posts
    except requests.exceptions.RequestException as e:
        print(f"Error fetching from Reddit: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []
