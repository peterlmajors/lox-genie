"""
YouTube Summarizer API Route

This route provides an HTTP endpoint to trigger the YouTube channel
fantasy football summarization pipeline.
"""

import logging
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, HttpUrl, Field

from services.api.pipelines.youtube_summarizer import summarize_youtube_channel

logger = logging.getLogger(__name__)

router = APIRouter()


class YouTubeSummarizerRequest(BaseModel):
    """Request model for YouTube summarizer endpoint."""
    
    channel_url: HttpUrl = Field(
        ...,
        description="YouTube channel URL (e.g., https://www.youtube.com/@ChannelName)"
    )
    max_videos: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Maximum number of videos to process (1-50)"
    )
    output_file: str = Field(
        default="services/api/pipelines/data/ff_lesson.md",
        description="Output file path for the generated markdown"
    )


class YouTubeSummarizerResponse(BaseModel):
    """Response model for YouTube summarizer endpoint."""
    
    status: str = Field(
        ...,
        description="Status of the request (e.g., 'processing', 'success', 'error')"
    )
    message: str = Field(
        ...,
        description="Human-readable status message"
    )
    channel_url: str = Field(
        ...,
        description="The channel URL being processed"
    )
    max_videos: int = Field(
        ...,
        description="Number of videos to process"
    )
    output_file: str = Field(
        ...,
        description="Path where results will be saved"
    )


@router.post("/summarize-channel", response_model=YouTubeSummarizerResponse)
async def summarize_channel_endpoint(
    request: YouTubeSummarizerRequest,
    background_tasks: BackgroundTasks
) -> YouTubeSummarizerResponse:
    """
    Trigger YouTube channel summarization pipeline.
    
    This endpoint accepts a YouTube channel URL and processes the last N videos
    to extract general fantasy football advice using the LLM service.
    
    The processing happens in the background, so this endpoint returns immediately
    with a processing status. Check the output file for results.
    
    Args:
        request: YouTubeSummarizerRequest with channel_url and options
        background_tasks: FastAPI background tasks handler
        
    Returns:
        YouTubeSummarizerResponse with processing status
        
    Raises:
        HTTPException: If request validation fails or processing cannot start
    """
    try:
        logger.info(f"Received YouTube summarizer request for: {request.channel_url}")
        
        # Validate channel URL format
        channel_url_str = str(request.channel_url)
        if "youtube.com" not in channel_url_str and "youtu.be" not in channel_url_str:
            raise HTTPException(
                status_code=400,
                detail="Invalid YouTube URL. Must be a youtube.com or youtu.be URL"
            )
        
        # Add pipeline to background tasks
        background_tasks.add_task(
            summarize_youtube_channel,
            channel_url=channel_url_str,
            max_videos=request.max_videos,
            output_file=request.output_file
        )
        
        return YouTubeSummarizerResponse(
            status="processing",
            message=f"Started processing {request.max_videos} videos from channel. Results will be saved to {request.output_file}",
            channel_url=channel_url_str,
            max_videos=request.max_videos,
            output_file=request.output_file
        )
        
    except HTTPException:
        raise
    except Exception as exc:
        logger.error(f"Error starting YouTube summarizer: {exc}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start summarization: {str(exc)}"
        )


@router.post("/summarize-channel-sync", response_model=YouTubeSummarizerResponse)
async def summarize_channel_sync_endpoint(
    request: YouTubeSummarizerRequest
) -> YouTubeSummarizerResponse:
    """
    Synchronously process YouTube channel summarization (waits for completion).
    
    Similar to /summarize-channel but waits for processing to complete before
    returning. Use this for immediate results but be aware it may take several
    minutes depending on the number of videos.
    
    Args:
        request: YouTubeSummarizerRequest with channel_url and options
        
    Returns:
        YouTubeSummarizerResponse with completion status
        
    Raises:
        HTTPException: If processing fails
    """
    try:
        logger.info(f"Received sync YouTube summarizer request for: {request.channel_url}")
        
        # Validate channel URL format
        channel_url_str = str(request.channel_url)
        if "youtube.com" not in channel_url_str and "youtu.be" not in channel_url_str:
            raise HTTPException(
                status_code=400,
                detail="Invalid YouTube URL. Must be a youtube.com or youtu.be URL"
            )
        
        # Run pipeline synchronously
        await summarize_youtube_channel(
            channel_url=channel_url_str,
            max_videos=request.max_videos,
            output_file=request.output_file
        )
        
        return YouTubeSummarizerResponse(
            status="success",
            message=f"Successfully processed {request.max_videos} videos from channel. Results saved to {request.output_file}",
            channel_url=channel_url_str,
            max_videos=request.max_videos,
            output_file=request.output_file
        )
        
    except HTTPException:
        raise
    except Exception as exc:
        logger.error(f"Error in YouTube summarizer: {exc}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to summarize channel: {str(exc)}"
        )

