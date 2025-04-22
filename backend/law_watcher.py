import requests
import os

API_KEY = os.getenv("OPENROUTER_API_KEY")

def summarize(text):
    if not API_KEY:
        return "❌ API key missing."

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "Summarize the following Turkish legal document in simple bullet points."},
            {"role": "user", "content": text}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    except requests.exceptions.HTTPError as e:
        return f"❌ GPT Error: {e.response.status_code} - {e.response.text}"

    except Exception as e:
        return f"❌ Unexpected Error: {str(e)}"
