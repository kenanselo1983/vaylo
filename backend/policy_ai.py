import requests

OPENROUTER_API_KEY = "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"

def summarize_policy(text):
    if not OPENROUTER_API_KEY:
        return "❌ API key missing."

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
Aşağıdaki metin bir şirketin gizlilik politikasıdır:

{text}

Bu politikayı basit ve maddeler halinde Türkçe olarak özetle.
Ayrıca hangi alanlarda eksik ya da geliştirilmesi gerektiğini de öner.
"""

    data = {
        "model": "mistral/mistral-7b-instruct",
        "prompt": prompt,
        "max_tokens": 512,
        "temperature": 0.7
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["text"]
    except Exception as e:
        return f"❌ GPT Error (completion fallback): {str(e)}"
