
import os
import requests

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
TOGETHER_MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"

def generate_questions_from_context(context_text: str) -> list:
    if not TOGETHER_API_KEY:
        return ["Missing Together API key."]

    prompt = f"""
    You're an expert interview coach. Based on the following resume and job context, generate:
    1. 15–20 tailored interview questions the candidate may be asked.
    2. Suggested questions they can ask the interviewer (HR, Manager, CEO).

    Context:
    {context_text}

    Format:
    Interview Questions:
    - ...

    HR Questions:
    - ...

    Manager Questions:
    - ...

    CEO Questions:
    - ...
    """

    response = requests.post(
        "https://api.together.xyz/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": TOGETHER_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 1024
        }
    )

    if response.status_code != 200:
        return [f"Error: {response.text}"]

    content = response.json()["choices"][0]["message"]["content"]
    return content.strip().split("\n")
