import ollama


MODEL_NAME = "qwen3:4b"


def generate_text(
    system_prompt: str,
    user_prompt: str,
) -> str:

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
    )

    return response["message"]["content"].strip()