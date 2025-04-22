import requests
import os

API_KEY = os.getenv("OPENROUTER_API_KEY")

def calculate_risk_score(text):
    if not API_KEY:
        return 0

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""Analyze this policy for data privacy compliance. Score the overall risk from 0 (no risk) to 100 (very high risk), and return only the number.

Policy:
{text}"""

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    response.raise_for_status()

    score_str = response.json()["choices"][0]["message"]["content"]
    try:
        return int("".join(filter(str.isdigit, score_str.strip())))
    except:
        return 0
