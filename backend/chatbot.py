import requests
import streamlit as st

API_KEY = st.secrets.get("OPENROUTER_API_KEY")

if not API_KEY:
    raise ValueError("❌ GPT Error: API key missing. Please set it in .streamlit/secrets.toml")

def ask_chatbot(messages):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",  # or change to your preferred model
        "messages": messages
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
