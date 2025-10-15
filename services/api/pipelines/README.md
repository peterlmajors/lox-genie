# API Pipelines

This directory contains data pipelines for the Lox API.

## YouTube Summarizer Pipeline

Extracts general fantasy football wisdom from YouTube channel videos.

### Installation

```bash
uv pip install -e .
```

### Usage

#### 1. Command Line Interface

Run as a Python module:

```bash
# Basic usage
python -m services.api.pipelines.youtube_summarizer "https://www.youtube.com/@TheFantasyFootballers"

# With options
python -m services.api.pipelines.youtube_summarizer "https://www.youtube.com/@TheFantasyFootballers" \
    --max-videos 5 \
    --output custom_output.md \
    --verbose

# Get help
python -m services.api.pipelines.youtube_summarizer --help
```

#### 2. Python API

```python
import asyncio
from services.api.pipelines.youtube_summarizer import summarize_youtube_channel

asyncio.run(summarize_youtube_channel(
    channel_url="https://www.youtube.com/@TheFantasyFootballers",
    max_videos=10,
    output_file="services/api/pipelines/data/ff_lesson.md"
))
```

#### 3. HTTP API

```bash
# Background processing (returns immediately)
curl -X POST "http://localhost:8000/summarize-channel" \
     -H "Content-Type: application/json" \
     -d '{"channel_url": "https://www.youtube.com/@TheFantasyFootballers", "max_videos": 10}'

# Synchronous (waits for completion)
curl -X POST "http://localhost:8000/summarize-channel-sync" \
     -H "Content-Type: application/json" \
     -d '{"channel_url": "https://www.youtube.com/@TheFantasyFootballers", "max_videos": 5}'
```

### Output

Results are saved to `services/api/pipelines/data/ff_lesson.md` by default.

### Prompts

Pipeline prompts are located in `services/api/pipelines/prompts/` for easy customization.

## Other Pipelines

- `fantasy_players.py` - Updates fantasy player data in AWS S3
- `fantasycalc.py` - Fetches rankings from Fantasy Calc API

