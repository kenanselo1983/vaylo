import os
import requests
import streamlit as st

OPENROUTER_API_KEY = st.secrets.get("OPENROUTER_API_KEY")

def summarize(text):
    if not OPENROUTER_API_KEY:
        return "❌ API key missing. Please check your Streamlit secrets."

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistral/mixtral-8x7b-instruct",
        "messages": [
            {"role": "system", "content": "Summarize the following Turkish legal document in simple bullet points."},
            {"role": "user", "content": text}
        ]
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data
    )

    result = response.json()
    return result["choices"][0]["message"]["content"]
