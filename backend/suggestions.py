import os
import requests
import streamlit as st

OPENROUTER_API_KEY = st.secrets.get("OPENROUTER_API_KEY")

def suggest_fixes(violations):
    if not OPENROUTER_API_KEY:
        return "❌ API key missing."

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    content = "These are the KVKK/GDPR violations:\n"
    for v in violations:
        content += f"- {v.get('description')}\n"

    content += "\nSuggest improvements, missing policies, and data protection measures in simple bullet points."

    data = {
        "model": "anthropic/claude-3-sonnet-20240229",
        "messages": [
            {"role": "user", "content": content}
        ],
        "stream": False
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Suggestion Error: {str(e)}"
