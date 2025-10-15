import re
import os
import sys
import httpx
import logging
import argparse
import asyncio
from typing import Optional
from langchain_community.document_loaders import YoutubeLoader
from langchain_openai import ChatOpenAI

from services.api.pipelines.prompts.youtube_summarizer import FANTASY_ADVICE_PROMPT

try:
    import scrapetube
    HAS_SCRAPETUBE = True
except ImportError:
    HAS_SCRAPETUBE = False

logger = logging.getLogger(__name__)

async def get_channel_video_ids(channel_url: str, max_videos: int = 10) -> list[dict]:
    """
    Extract video IDs from a YouTube channel URL.
    Uses scrapetube as primary method, with BeautifulSoup fallback.
    
    Args:
        channel_url: URL of the YouTube channel
        max_videos: Maximum number of videos to retrieve
        
    Returns:
        list[dict]: List of dicts with video_id and title
    """
    try:
        # Get the channel ID from the URL
        try:
            url = channel_url.rstrip('/').replace('/videos', '')
            channel_id = url.split('/')[-1]
        except Exception as e:
            logger.error(f"Error extracting channel ID from URL: {e}")

        logger.info(f"Fetching videos from channel: {channel_id}")
        
        # Method 1: Use scrapetube (preferred)
        if HAS_SCRAPETUBE:
            try:
                videos = []
                # Determine if channel_id is a username (@) or channel ID
                if channel_id.startswith('@'):
                    channel_videos = scrapetube.get_channel(channel_username=channel_id[1:])
                else:
                    try:
                        channel_videos = scrapetube.get_channel(channel_id=channel_id)
                    except:
                        channel_videos = scrapetube.get_channel(channel_username=channel_id)
                
                # Extract video data
                for i, video in enumerate(channel_videos):
                    if i >= max_videos:
                        break
                    video_id = video.get('videoId')
                    title = video.get('title', {}).get('runs', [{}])[0].get('text', 'Unknown Title')
                    if video_id:
                        videos.append({"video_id": video_id, "title": title})
                if videos:
                    logger.info(f"Found {len(videos)} videos using scrapetube")
                    return videos
                    
            except Exception as e:
                logger.warning(f"Scrapetube failed for channel {channel_id}: {e}")
    except Exception as e:
        logger.error(f"Error extracting video IDs from channel: {e}")
        raise


def get_video_transcript(video_id: str) -> Optional[str]:
    """
    Get the transcript for a YouTube video.
    
    Args:
        video_id: YouTube video ID
        
    Returns:
        str: Full transcript text, or None if unavailable
    """
    try:
        logger.info(f"Getting transcript for video {video_id}")
        loader = YoutubeLoader.from_youtube_url(f"https://www.youtube.com/watch?v={video_id}", add_video_info=False)
        content = loader.load()

        lines = content[0].page_content.split('\n') if isinstance(content[0].page_content, str) else list(content[0].page_content)
        transcript = '\n'.join(lines)    
        return transcript
    except Exception as e:
        logger.warning(f"Could not retrieve transcript for video {video_id}: {e}")
        return None


async def extract_fantasy_advice(title: str, transcript: str, llm_base_url: str) -> str:
    """
    Use LLM to extract general fantasy football advice from a transcript.
    
    Args:
        title: Video title
        transcript: Video transcript text
        llm_base_url: Base URL for the LLM service
        
    Returns:
        str: Extracted fantasy football advice synopsis
    """
    try:
        # Initialize LLM with same pattern as other agents
        llm = ChatOpenAI(
            base_url=llm_base_url,
            api_key="not-needed",  # llama.cpp doesn't require API key
            model="llama-3.2-3b-instruct",
            temperature=0.3,
        )
        
        # Format prompt with transcript
        prompt = FANTASY_ADVICE_PROMPT.format(title=title, transcript=transcript)
        
        # Get LLM response
        response = await llm.ainvoke(prompt)
        
        return response.content
        
    except Exception as e:
        logger.error(f"Error extracting advice with LLM: {e}")
        return f"Error processing video: {str(e)}"


async def summarize_youtube_channel(
    channel_url: str,
    max_videos: int = 10,
    output_file: str = "services/api/pipelines/data/ff_lesson.md"
) -> None:
    """
    Main pipeline function to scrape YouTube channel videos, extract transcripts,
    and generate fantasy football advice summaries.
    
    Args:
        channel_url: URL of the YouTube channel to scrape
        max_videos: Number of recent videos to process (default: 10)
        output_file: Path to output markdown file
    """
    try:
        logger.info(f"Starting YouTube channel summarization for: {channel_url}")
        
        # Get LLM base URL from environment
        llm_base_url = os.getenv("LLM_BASE_URL", "http://localhost:8002/v1")
        
        # Step 1: Get video IDs from channel
        videos = await get_channel_video_ids(channel_url, max_videos)
        
        if not videos:
            logger.warning("No videos found in channel")
            return
        
        # Step 2: Process each video
        summaries = []
        for i, video in enumerate(videos, 1):
            video_id = video["video_id"]
            title = video["title"]
            
            logger.info(f"Processing video {i}/{len(videos)}: {title}")
            
            # Get transcript
            transcript = get_video_transcript(video_id)
            
            if not transcript:
                logger.warning(f"Skipping video {video_id} - no transcript available")
                summaries.append({
                    "title": title,
                    "video_id": video_id,
                    "advice": "No transcript available for this video.",
                    "url": f"https://www.youtube.com/watch?v={video_id}"
                })
                continue
            
            # Extract fantasy advice using LLM
            logger.info(f"Extracting fantasy advice from: {title}")
            advice = await extract_fantasy_advice(title, transcript, llm_base_url)
            
            summaries.append({
                "title": title,
                "video_id": video_id,
                "advice": advice,
                "url": f"https://www.youtube.com/watch?v={video_id}"
            })
        
        # Step 3: Write to markdown file
        await write_summaries_to_markdown(summaries, output_file, channel_url)
        
        logger.info(f"Successfully processed {len(summaries)} videos. Output saved to {output_file}")
        
    except Exception as e:
        logger.error(f"Error in summarize_youtube_channel: {e}")
        raise


async def write_summaries_to_markdown(
    summaries: list[dict],
    output_file: str,
    channel_url: str
) -> None:
    """
    Write the fantasy football advice summaries to a markdown file.
    
    Args:
        summaries: List of summary dictionaries
        output_file: Path to output file
        channel_url: Original channel URL for reference
    """
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Build markdown content
        markdown_content = f"""# Fantasy Football Lessons from YouTube Channel

**Source Channel:** {channel_url}  
**Videos Analyzed:** {len(summaries)}  
**Generated:** {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

"""
        
        for i, summary in enumerate(summaries, 1):
            markdown_content += f"""## Video {i}: {summary['title']}

**Watch:** {summary['url']}

### General Fantasy Football Wisdom

{summary['advice']}

---

"""
        
        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        logger.info(f"Markdown file written to {output_file}")
        
    except Exception as e:
        logger.error(f"Error writing markdown file: {e}")
        raise


# Convenience function for direct execution
async def run_pipeline(channel_url: str) -> None:
    """
    Run the YouTube summarization pipeline.
    
    Usage:
        import asyncio
        from services.api.pipelines.youtube_summarizer import run_pipeline
        
        asyncio.run(run_pipeline("https://www.youtube.com/@channelname"))
    """
    await summarize_youtube_channel(channel_url)


# ============================================================================
# CLI Interface
# ============================================================================

def parse_args():
    """Parse command line arguments for CLI usage."""
    parser = argparse.ArgumentParser(
        description='Extract fantasy football wisdom from YouTube channel videos',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
The pipeline will:
  1. Scrape the last N videos from the channel
  2. Extract video transcripts
  3. Use LLM to identify general fantasy football advice
  4. Generate a synopsis for each video
  5. Save results to markdown file

Note: Requires LLM service to be running at LLM_BASE_URL
        """
    )
    
    parser.add_argument(
        'channel_url',
        type=str,
        help='YouTube channel URL (e.g., https://www.youtube.com/@ChannelName)'
    )
    
    parser.add_argument(
        '--max-videos',
        type=int,
        default=10,
        help='Maximum number of videos to process (default: 10)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='services/api/pipelines/data/ff_lesson.md',
        help='Output file path (default: services/api/pipelines/data/ff_lesson.md)'
    )
    
    parser.add_argument(
        '--llm-url',
        type=str,
        default=None,
        help='Override LLM base URL (default: from LLM_BASE_URL env var)'
    )
    
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable verbose debug logging'
    )
    
    return parser.parse_args()


async def cli_main():
    """Main entry point for CLI execution."""
    args = parse_args()
    
    # Configure logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Set LLM URL if provided
    if args.llm_url:
        os.environ['LLM_BASE_URL'] = args.llm_url
    
    # Validate LLM service availability
    llm_base_url = os.getenv('LLM_BASE_URL')
    if not llm_base_url:
        logger.warning(
            "LLM_BASE_URL not set. Using default: http://localhost:8002/v1"
        )
        logger.warning(
            "Make sure your LLM service is running or set LLM_BASE_URL environment variable"
        )
    
    logger.info("=" * 70)
    logger.info("YouTube Fantasy Football Summarizer Pipeline")
    logger.info("=" * 70)
    logger.info(f"Channel URL: {args.channel_url}")
    logger.info(f"Max Videos: {args.max_videos}")
    logger.info(f"Output File: {args.output}")
    logger.info(f"LLM Service: {llm_base_url or 'http://localhost:8002/v1'}")
    logger.info("=" * 70)
    
    try:
        # Run the pipeline
        await summarize_youtube_channel(
            channel_url=args.channel_url,
            max_videos=args.max_videos,
            output_file=args.output
        )
        
        logger.info("=" * 70)
        logger.info("✓ Pipeline completed successfully!")
        logger.info(f"✓ Results saved to: {args.output}")
        logger.info("=" * 70)
        
        return 0
        
    except Exception as e:
        logger.error("=" * 70)
        logger.error(f"✗ Pipeline failed: {e}", exc_info=args.verbose)
        logger.error("=" * 70)
        return 1


if __name__ == "__main__":
    # Configure logging for CLI usage
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run CLI
    exit_code = asyncio.run(cli_main())
    sys.exit(exit_code)
