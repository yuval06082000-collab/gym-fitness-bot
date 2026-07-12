import requests
url = "https://server.iac.ac.il/api/v1/studentapi/generate_key"
payload = {"id": "123456789", "password": "Maho8135"}
print(requests.post(url, json=payload).json())
