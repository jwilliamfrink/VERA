# queryPlainText.py
from openai import OpenAI

# Path to your plaintext document
VALUES_PATH = "/mnt/c/Users/jfrin/Documents/projects/AI/VERA/veraPlainTextValues.txt"

# Load values from text file
with open(VALUES_PATH, "r", encoding="utf-8") as f:
    vera_values_text = f.read()

# OpenAI client (uses OPENAI_API_KEY env var)
openai_client = OpenAI()

# === Prompt Loop ===
while True:
    query = input("\nAsk a question (or 'exit'): ").strip()
    if query.lower() == "exit":
        break

    messages = [
        {"role": "system", "content": "You are a helpful assistant grounded in ethical principles."},
        {
            "role": "user",
            "content": (
                f"Refer to the following list of ethical principles:\n\n{vera_values_text}\n\n"
                f"Given the above, answer this question:\n{query}"
                f"Be sure to cite which portions of the text influenced your answer."
            )
        }
    ]

    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.4
    )

    print("\n🧠 GPT Response:\n", response.choices[0].message.content.strip())
