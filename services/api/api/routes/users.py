import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response, JSONResponse

router = APIRouter(prefix="/users")

@router.get("/avatar/{username}")
async def fetch_avatar_image(username: str) -> Response:
    """
    Fetch avatar image from SleeperCDN.
    Args:
        username: The username of the user.
    Returns:
        Response: The avatar image.
    """
    # Fetch user metadata
    async with httpx.AsyncClient() as client:
        try:
            um = await client.get(f'https://api.sleeper.app/v1/user/{username}')
            if um.status_code != 200:
                raise HTTPException(status_code=404, detail=f"Failed to fetch user metadata for {username}")
            
            user_data = um.json()
            if user_data is None:
                raise HTTPException(status_code=404, detail=f"Username {username} not found on Sleeper")

            # Parse avatar ID from user metadata
            avatar_id = user_data.get('avatar', None)
            if not avatar_id:
                raise HTTPException(status_code=404, detail=f"No avatar found for {username} on Sleeper")
            
            # Fetch avatar image from SleeperCDN
            avatar_response = await client.get(f'https://sleepercdn.com/avatars/{avatar_id}')
            if avatar_response.status_code != 200:
                raise HTTPException(status_code=404, detail=f"Failed to fetch avatar for {username}")
            
            # Return avatar image
            avatar_data = avatar_response.content
            return Response(content=avatar_data, media_type="image/jpeg")
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Failed to connect to Sleeper API: {str(e)}")

@router.get("/{username}")
async def fetch_user_metadata(username: str) -> JSONResponse:
    """
    Fetch user metadata from Sleeper.
    Args:
        username: The username of the user.
    Returns:
        JSONResponse: The user metadata.
    """
    async with httpx.AsyncClient() as client:
        try:
            metadata = await client.get(f'https://api.sleeper.app/v1/user/{username}')
            if metadata.status_code != 200:
                raise HTTPException(status_code=404, detail=f"Failed to fetch user metadata for {username}")
            
            user_data = metadata.json()
            if user_data is None:
                raise HTTPException(status_code=404, detail=f"Username {username} not found on Sleeper")
            
            return JSONResponse(content=user_data)
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Failed to connect to Sleeper API: {str(e)}")