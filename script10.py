import requests

headers = {"Authorization": "Bearer sk-std-20-L0wIuLBlYzncmfBoYPYQGZHRkG9X3iD7LzglfMkY"}
payload = {
    "messages": [
        {
            "role": "user",
            "content": "what is better a cat or a dog? give a short, up to 50 words answer."
        }
    ],
    "max_completion_tokens": 500
}

r = requests.post("https://server.iac.ac.il/api/v1/studentapi/chat/completions",
                  json=payload, headers=headers)
print(r.json())

