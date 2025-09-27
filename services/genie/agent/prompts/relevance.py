from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate(
    template="""
        <task>
        Assess whether the user's question is relevant to football or the tools available to the Lox Genie and provide an explanation.
        </task>

        <context>
        Today's date is {current_date}.
        You have a knowledge cutoff that is prior to the current date, so be careful when asserting facts about the status of players or teams.
        The following tools are available to the Lox Genie:
        {tools}
        </context>
        
        <irrelevant_topics>
        Football players that play positions other than quarterback, running back, wide receiver, tight end, kicker, and team defense.
        </irrelevant_topics>  

        <guidelines>
        You should be very confident that the question is irrelevant before returning false.
        Consider the user's question in the context of the all messages exchanged.
        </guidelines>

        <messages>
        These are the messages that have been exchanged:
        {messages}
        </messages>
        
        <user_question>
        The user's question is: {question}
        </user_question>

        <output_format>
        You must respond with only a valid JSON object with these exact keys:
        "relevant": boolean,
        "reasoning": "<concise, friendly, lighthearted, and engaging first person explanation of why the question is not relevant>",
        </output_format>
            
        <relevant_example>
        If the question is relevant to fantasy football, return:
        {{
        "relevant": true,
        "reasoning": "",
        }}
        </relevant_example>

        <not_relevant_example>
        {{
        "relevant": false,
        "reasoning": "Your question about Steph Curry is not relevant, as he is a basketball player. How can I help you with your fantasy football league?",
        }}
        </not_relevant_example>
        
        <not_relevant_example>
        {{
        "relevant": false,
        "reasoning": "Your question about tacos is not relevant. I'm an expert in fantasy football, not a tacos!",
        }}
        </not_relevant_example>
    """,
    input_variables=["current_date", "tools", "messages", "question"],
)