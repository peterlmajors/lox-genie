"""
Prompt for YouTube Fantasy Football Wisdom Extractor

This prompt is used to extract general fantasy football advice from video
transcripts, filtering out player-specific and team-specific content.
"""

FANTASY_ADVICE_PROMPT = """
    <role>
    You are an expert fantasy football analyst.
    </role>

    <task>
    Analyze the following video transcript and extract ONLY general fantasy football advice, strategies, and principles that are NOT tied to specific players or teams.
    </task>

    <focus>
    Focus on:
- Draft strategies and general positional value
- Trade principles and valuation concepts
- Waiver wire strategies
- Lineup decision frameworks
- General player evaluation criteria
- League format considerations (PPR, Dynasty, etc.)
- Risk management and diversification strategies
- General trends and patterns in fantasy football
    </focus>

    <do_not_include>
DO NOT include:
- Specific player recommendations or analysis
- Team-specific advice
- Week-specific predictions
- Injury updates about specific players
    </do_not_include>

    <video_title>
    Video Title: {title}
    </video_title>

    <transcript>
    Transcript:
    {transcript}
    </transcript>

    <output_format>
    Provide a concise synopsis (3-5 sentences) of the general fantasy football wisdom from this video. If there is no general advice (only player-specific content), respond with "No general advice found."
    </output_format>
"""

