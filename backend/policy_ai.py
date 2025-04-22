import os
import requests
import streamlit as st

OPENROUTER_API_KEY = st.secrets.get("OPENROUTER_API_KEY")

def summarize_policy(text):
    if not OPENROUTER_API_KEY:
        return "❌ API key missing."

    headers = {
        "Authorization": f"Bearer ",
        "Content-Type": "application/json"
    }

    prompt = f"""
A company uploaded this privacy policy:

{text}

Summarize it clearly in Turkish. Highlight key points. Then give bullet-pointed suggestions to make it more compliant with KVKK and GDPR.
"""

    data = {
        "model": "anthropic/claude-3-sonnet-20240229",
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ GPT Error: {str(e)}"
