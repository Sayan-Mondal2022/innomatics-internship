from prompts.intent_prompt import intent_prompt
from utils.config import get_llm

llm = get_llm(temperature=0.0)

intent_chain = intent_prompt | llm
