from pydantic import BaseModel, HttpUrl, Field

class YouTubeSummarizerRequest(BaseModel):
    """Request model for YouTube summarizer endpoint."""
    channel_url: HttpUrl = Field(..., description="YouTube channel URL (e.g., https://www.youtube.com/@ChannelName)")
    max_videos: int = Field(default=10, ge=1, le=50, description="Maximum number of videos to process (1-50)")
    output_file: str = Field(default="services/api/pipelines/data/ff_lesson.md", description="Output file path for the generated markdown")
    
class YouTubeSummarizerResponse(BaseModel):
    """Response model for YouTube summarizer endpoint."""
    status: str = Field(..., description="Status of the request (e.g., 'processing', 'success', 'error')")
    message: str = Field(..., description="Human-readable status message")
    channel_url: str = Field(..., description="The channel URL being processed")
    max_videos: int = Field(..., description="Number of videos to process")
    output_file: str = Field(..., description="Path where results will be saved")