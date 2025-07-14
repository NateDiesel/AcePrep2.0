import os
import requests

def push_to_github():
    token = os.getenv("GH_PAT")
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get("https://api.github.com/user", headers=headers)
    print(res.json())
