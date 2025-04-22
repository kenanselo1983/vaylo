import requests
import os

API_KEY = os.getenv("OPENROUTER_API_KEY")

def suggest_fixes(text):
    if not API_KEY:
        return ["❌ API key missing."]

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a policy compliance expert. Give short bullet-point suggestions to improve this policy:"},
            {"role": "user", "content": text}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    response.raise_for_status()

    suggestions = response.json()["choices"][0]["message"]["content"]
    return suggestions.strip().split("\n")
