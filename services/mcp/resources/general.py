from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate(
    template="""
        # NFL Season Context:
        - We are in week {week} of the NFL season.

        # General Approach:
        - Managing a fantasy football team is a test of skill, dedication, and ultimately, luck.

        # Separating Real Football from Fantasy Football:
        - ...

        """,
    input_variables=["week"],
)