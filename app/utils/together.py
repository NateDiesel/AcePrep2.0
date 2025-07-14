<<<<<<< HEAD
import os
import requests

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
TOGETHER_API_URL = "https://api.together.xyz/v1/completions"  # ✅ Correct endpoint

def chat_completion(prompt):
    if not TOGETHER_API_KEY:
        raise EnvironmentError("❌ TOGETHER_API_KEY is missing or not set.")

    if not prompt or len(prompt.strip()) < 10:
        raise ValueError("❌ Prompt is empty or too short to send to Together.ai.")

    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
=======

import os
import requests

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

def chat_completion(prompt):
    if not OPENROUTER_API_KEY:
        raise EnvironmentError("❌ OPENROUTER_API_KEY is missing or not set.")

    if not prompt or len(prompt.strip()) < 10:
        raise ValueError("❌ Prompt is empty or too short to send to OpenRouter.")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
>>>>>>> 74eb77e (🚀 Initial OpenRouter-powered production release)
        "Content-Type": "application/json"
    }

    payload = {
<<<<<<< HEAD
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",  # ✅ Confirmed model
        "prompt": prompt,
        "max_tokens": 1024,
        "temperature": 0.7
    }

    print("🔁 Sending prompt to Together.ai with payload:", payload)

    response = requests.post(TOGETHER_API_URL, headers=headers, json=payload)
=======
        "model": "mistralai/mixtral-8x7b-instruct",
        "messages": [
            {"role": "system", "content": "You are a helpful interview prep assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    print("🔁 Sending prompt to OpenRouter with payload:", payload)

    response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload)
>>>>>>> 74eb77e (🚀 Initial OpenRouter-powered production release)

    try:
        response.raise_for_status()
    except requests.HTTPError as e:
<<<<<<< HEAD
        print("❌ Error from Together.ai:", response.status_code, response.text)
        raise e

    return response.json().get("choices", [{}])[0].get("text", "⚠️ No response from model.")
=======
        print("❌ Error from OpenRouter:", response.status_code, response.text)
        raise e

    return response.json()["choices"][0]["message"]["content"]
>>>>>>> 74eb77e (🚀 Initial OpenRouter-powered production release)
