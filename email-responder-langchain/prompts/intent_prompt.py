from langchain_core.prompts import PromptTemplate

intent_prompt = PromptTemplate(
    input_variables=["email"],
    template="""
You are an email classifier.

Classify into ONE:
complaint | inquiry | support | feedback

Email:
{email}

Return only one word.
""",
)
