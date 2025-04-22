import requests
import os

API_KEY = os.getenv("OPENROUTER_API_KEY")

def ask_chatbot(context, question):
    if not API_KEY:
        raise Exception("❌ API key missing.")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": f"You are a compliance assistant. This is the policy:\n{context}"},
            {"role": "user", "content": question}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]
