import os
import requests

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "mistralai/mixtral-8x7b-instruct"

def chat_completion(prompt):
    if not OPENROUTER_API_KEY:
        raise EnvironmentError("❌ OPENROUTER_API_KEY is missing or not set.")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://yourdomain.com",  # ✅ Customize if needed
        "X-Title": "AcePrep2.0"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are an expert technical interview coach."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1024
    }

    response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload)
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]
