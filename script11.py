import requests

headers = {"Authorization": "Bearer sk-std-20-L0wIuLBlYzncmfBoYPYQGZHRkG9X3iD7LzglfMkY"}
payload = {
    "reasoning": {"effort": "low"},
    "instructions": "Give a short answer up to 50 words only. Talk like a pirate.",
    "input": "Are semicolons optional in JavaScript?"
}

r = requests.post("https://server.iac.ac.il/api/v1/studentapi/responses", 
                  json=payload, headers=headers)
print(r.json())