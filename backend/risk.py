import os
import requests
import streamlit as st

OPENROUTER_API_KEY = st.secrets.get("OPENROUTER_API_KEY")

def calculate_risk_score(violations):
    base_score = 100
    for v in violations:
        severity = v.get("severity", "medium").lower()
        if severity == "high":
            base_score -= 20
        elif severity == "medium":
            base_score -= 10
        else:
            base_score -= 5

    score = max(0, base_score)
    return score

def explain_risk_with_ai(score, violations):
    if not OPENROUTER_API_KEY:
        return "❌ API key missing."

    description = "Here are the detected violations:\n"
    for v in violations:
        description += f"- {v.get('description')}\n"

    prompt = f"""
The compliance scan returned a risk score of {score}/100.
{description}
Based on this, write a short plain-language explanation of why this score was assigned and what the company should prioritize.
Keep it clear and helpful.
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

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
        return f"❌ Risk explanation error: {str(e)}"
