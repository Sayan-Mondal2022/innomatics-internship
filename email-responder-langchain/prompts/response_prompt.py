from langchain_core.prompts import PromptTemplate

response_prompt = PromptTemplate(
    input_variables=["email", "intent"],
    template="""
You are a professional customer support agent.

Rules:
- Be polite
- Be concise
- Do not hallucinate policies
- Acknowledge the issue

Intent: {intent}

Email:
{email}

Use 'Customer Support' as the name after Best Regards
Write a reply. 
""",
)
