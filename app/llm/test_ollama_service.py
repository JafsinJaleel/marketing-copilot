from app.llm.ollama_service import generate_text


system_prompt = """
You are a marketing assistant.

Generate only the requested marketing content.
Do not explain your reasoning.
Do not add notes about why the content works.
"""


user_prompt = """
Create one short marketing headline for the SmartFit Watch.
"""


response = generate_text(
    system_prompt=system_prompt,
    user_prompt=user_prompt,
)


print("\nOllama Service Test")
print("-------------------")
print(response)