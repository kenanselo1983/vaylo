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
        "model": "anthropic/claude-3-sonnet-20240229",
        "messages": [
            {"role": "user", "content": "Summarize the following Turkish legal document in simple bullet points:\n\n" + text}
        ],
        "stream": False
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Error from AI: {str(e)}"
