import os
import requests
from dotenv import load_dotenv

load_dotenv()

headers = {"Authorization": f"Bearer {os.getenv('API_KEY')}"}
messages = []

print("Chat started. Type 'exit' to quit.")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    messages.append({"role": "user", "content": user_input})
    payload = {
        "messages": messages,
        "max_completion_tokens": 500
    }

    r = requests.post("https://server.iac.ac.il/api/v1/studentapi/chat/completions",
                      json=payload, headers=headers)

    response_json = r.json()
    bot_reply = response_json["choices"][0]["message"]["content"]
    print(f"Bot: {bot_reply}\n")

    messages.append({"role": "assistant", "content": bot_reply})