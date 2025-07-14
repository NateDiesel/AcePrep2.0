import os
import requests

API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openrouter/mistralai/mixtral-8x7b"
API_KEY = os.getenv("OPENROUTER_API_KEY")


def chat_completion(prompt: str) -> str:
    """Send a prompt to OpenRouter and return the response text."""
    if not API_KEY:
        raise EnvironmentError("OPENROUTER_API_KEY is missing or not set.")

    if not prompt or len(prompt.strip()) < 1:
        raise ValueError("Prompt is empty or invalid.")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()

    data = response.json()
    return data["choices"][0]["message"]["content"]
