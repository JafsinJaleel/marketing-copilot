import ollama


response = ollama.chat(
    model="qwen3:4b",
    messages=[
        {
            "role": "user",
            "content": "Create one short marketing headline for a fitness watch.",
        }
    ],
)


print("\nOllama Response")
print("----------------")
print(response["message"]["content"])