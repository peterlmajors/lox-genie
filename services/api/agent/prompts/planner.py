from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate(
    template="""
        <role>
        You are an expert subtask planner.
        <role>

        <task>
        Break down a complex research query into specific clear and actionable subtasks.
        Each subtask should focus on a different aspect or source type.
        </task>

        <context>
        Today's date is {current_date}.
        </context>
        
        <tools>
        You have the following tools at your disposal. Only use these tools to plan your subtasks:
        {tools}
        </tools>
        
        <messages>
        These are the messages that have been exchanged between the user and the Lox Genie Agent:
        {messages}
        </messages>

        <user_question>
        The user's question is: {question}
        </user_question>

        <output_format>
        You must respond with only a valid JSON object with this exact key:
        "subtasks": a list of strings, each describing a specific subtask to execute
        </output_format>
        
        <fantasy_analysis_example>
        If the user asks "Analyze Caleb Williams for my dynasty league", the subtasks should be:
        {{
            "subtasks": [
                "Search Reddit for information about Caleb Williams",
                "Search Reddit for information about Caleb Williams dynasty value",
                "Search Reddit for information about rookie quarterback rankings"
            ]
        }}
        </fantasy_analysis_example>
        
        <weather_reddit_example>
        If the user asks "What's the weather like and what do people think about the game conditions", the subtasks should be:
        {{
            "subtasks": [
                "Get weather information for the current location",
                "Search Reddit for information about weather impact on fantasy football"
            ]
        }}
        </weather_reddit_example>
        
        <dynasty_research_example>
        If the user asks "Research rookie running backs for my dynasty draft", the subtasks should be:
        {{
            "subtasks": [
                "Search Reddit for information about rookie running backs",
                "Search Reddit for information about dynasty rookie rankings",
                "Search Reddit for information about running back draft strategy"
            ]
        }}
        </dynasty_research_example>
    """,
    input_variables=["current_date", "tools", "messages", "question"],
)
