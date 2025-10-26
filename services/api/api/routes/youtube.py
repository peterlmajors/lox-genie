"""
YouTube Summarizer API Route

This route provides an HTTP endpoint to trigger the YouTube channel
fantasy football summarization pipeline.
"""
import logging
from fastapi import APIRouter, HTTPException
from services.api.schemas.youtube import YouTubeSummarizerRequest, YouTubeSummarizerResponse
from services.api.pipelines.youtube_summarizer import summarize_youtube_channel

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/youtube")

@router.post("/summarize-channel", response_model=YouTubeSummarizerResponse)
async def youtube_summarize_channel(request: YouTubeSummarizerRequest) -> YouTubeSummarizerResponse:
    try:
        logger.info(f"Received YouTube summarizer request for: {request.channel_url}")
        await summarize_youtube_channel(request.channel_url, request.max_videos, request.output_file)
        return YouTubeSummarizerResponse(
            status="success",
            message=f"Successfully summarized {request.max_videos} videos from channel. Results saved to {request.output_file}",
            channel_url=request.channel_url,
            max_videos=request.max_videos,
            output_file=request.output_file
        )
    except Exception as e:
        logger.error(f"Error summarizing YouTube channel: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to summarize YouTube channel: {str(e)}") from e