import httpx
from fastapi import APIRouter
from fastapi.responses import Response

router = APIRouter()

@router.get("/user/avatar/{username}")
async def fetch_avatar(username: str) -> Response:
    """
    Fetch avatar image from SleeperCDN.
    Args:
        username: The username of the user.
    Returns:
        Response: The avatar image.
    """
    # Fetch user metadata
    um = httpx.get(f'https://api.sleeper.app/v1/user/{username}')
    if um.status_code != 200:
        raise Exception(f"Failed to fetch user metadata for {username}. Response: {um.status_code} - {um.text}")
    elif um.json() == None:
        raise Exception(f"Username {username} not found. Response: {um.status_code} - {um.text}")

    # Parse avatar ID from user metadata
    avatar_id = um.json().get('avatar', None)
    if not avatar_id:
        raise Exception(f"No avatar found for {username}.")
    
    # Fetch avatar image from SleeperCDN
    avatar_url = httpx.get(f'https://sleepercdn.com/avatars/{avatar_id}')
    if avatar_url.status_code != 200:
        raise Exception(f"Failed to fetch avatar for {username}: Response: {avatar_url.status_code} - {avatar_url.text}")
    
    # Save avatar image to file
    avatar_data = avatar_url.content
    return Response(content=avatar_data, media_type="image/jpeg")