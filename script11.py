import os
import requests
from dotenv import load_dotenv

load_dotenv()

headers = {"Authorization": f"Bearer {os.getenv('API_KEY')}"}

print("Chat started. Type 'exit' to quit.")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    payload = {
        "reasoning": {"effort": "low"},
        "instructions": "Give a short answer up to 50 words only. Talk like a pirate.",
        "input": user_input
    }

    r = requests.post("https://server.iac.ac.il/api/v1/studentapi/responses",
                      json=payload, headers=headers)

    response_json = r.json()
    bot_reply = response_json.get("output") or response_json.get("answer") or response_json
    print(f"Bot: {bot_reply}\n")