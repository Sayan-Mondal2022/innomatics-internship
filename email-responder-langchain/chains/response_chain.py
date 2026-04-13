from prompts.response_prompt import response_prompt
from utils.config import get_llm

llm = get_llm(temperature=0.3)

response_chain = response_prompt | llm
