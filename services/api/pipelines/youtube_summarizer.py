"""
YouTube Fantasy Football Wisdom Extractor

This pipeline extracts general fantasy football advice from YouTube video transcripts, filtering out player-specific and team-specific content.
"""
import os
import sys
import argparse
import asyncio
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig
from langchain_community.document_loaders import YoutubeLoader
from services.api.agent.config import Configuration
from services.api.utils.logger import logger

FANTASY_ADVICE_PROMPT = """
    # Role:
    You are an expert at extracting generalizable concepts from YouTube video transcripts related to fantasy football advice.

    # Task:
    Analyze the following video transcript and extract only generalizable concepts that are not reliant on the current situation of players, teams, coaches, or other contextual factors.

    # Pay Attention to:
    - The underlying reason why a recommendation or piece of advice is made
    - Player or team evaluation criteria used to justify the recommendation or piece of advice
    
    # Output Format: 
    - List of generalizable concepts, however long you deem necessary to fully capture all of the underlying concepts.

    # Video Title:
    {title}

    # Transcript:
    {transcript}
"""

try:
    import scrapetube
    HAS_SCRAPETUBE = True
except ImportError:
    HAS_SCRAPETUBE = False

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


async def extract_fantasy_advice(title: str, transcript: str, config: RunnableConfig) -> str:
    """
    Use LLM to extract general fantasy football advice from a transcript.
    
    Args:
        title: Video title
        transcript: Video transcript text
        config: RunnableConfig
        
    Returns:
        str: Extracted fantasy football advice synopsis
    """
    try:
        # Initialize LLM with same pattern as other agents
        configuration = Configuration.from_runnable_config(config)
        llm = ChatOpenAI(
            base_url=configuration.llm_base_url,
            api_key="not-needed",  # llama.cpp doesn't require API key
            model=configuration.summarizer_model,
            temperature=0.0,
        )
        
        # Format prompt with transcript, invoke LLM
        prompt = ChatPromptTemplate.from_template(FANTASY_ADVICE_PROMPT).format(title=title, transcript=transcript)
        response = await llm.ainvoke(prompt)

        return response.content
    except Exception as e:
        logger.error(f"Error extracting advice with LLM: {e}")
        return f"Error extracting advice: {str(e)}"


async def summarize_youtube_channel(channel_url: str, max_videos: int = 10,output_file: str = "services/api/pipelines/data/ff_lesson.md") -> None:
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
            advice = await extract_fantasy_advice(title, transcript)
            
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


async def write_summaries_to_markdown(summaries: list[dict], output_file: str, channel_url: str) -> None:
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

def parse_args() -> argparse.Namespace:
    """Parse and return CLI arguments for the summarizer."""
    parser = argparse.ArgumentParser(description="Extract fantasy football wisdom from a YouTube channel.")
    parser.add_argument("channel_url", help="YouTube channel URL (e.g. https://www.youtube.com/@ChannelName)")
    parser.add_argument("--max-videos", type=int, default=1, help="Max videos to process (default: 10)")
    parser.add_argument("--output", type=str, default="services/api/pipelines/data/ff_lesson.md", help="Markdown output path")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable debug logging")
    return parser.parse_args()

async def cli_main() -> int:
    """CLI entrypoint for running the pipeline."""
    args = parse_args()
    if args.verbose: logger.setLevel(logger.DEBUG)
    logger.info(f"Running YouTube summarizer on: {args.channel_url} (max_videos={args.max_videos})")
    try:
        await summarize_youtube_channel(args.channel_url, max_videos=args.max_videos, output_file=args.output)
        logger.info(f"✓ Saved results to {args.output}")
        return 0
    except Exception as e:
        logger.error(f"✗ Pipeline failed: {e}", exc_info=args.verbose)
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(cli_main()))
