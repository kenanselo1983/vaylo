import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

def ask_chatbot(context, question):
    if not API_KEY:
        return "❌ API key missing."

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": f"You are a helpful compliance assistant AI. Below is a privacy policy or legal text:\n{context}"
            },
            {
                "role": "user",
                "content": question
            }
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    except requests.exceptions.HTTPError as e:
        return f"❌ Chatbot Error: {e.response.status_code} - {e.response.text}"

    except Exception as e:
        return f"❌ Unexpected Chatbot Error: {str(e)}"
