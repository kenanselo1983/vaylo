import requests
import streamlit as st

OPENROUTER_API_KEY = st.secrets.get("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("❌ GPT Error: API key missing. Please check your Streamlit secrets.")

def ask_chatbot(context, question):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistral/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": context},
            {"role": "user", "content": question}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
