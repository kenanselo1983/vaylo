import requests
from bs4 import BeautifulSoup

def fetch_kvkk_updates():
    url = "https://www.kvkk.gov.tr/"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        text_blocks = soup.find_all("p")
        raw_text = " ".join(p.get_text(strip=True) for p in text_blocks)
        return raw_text[:3000]
    except Exception:
        return "Failed to fetch content."

def summarize(text):
    return "[MOCK SUMMARY] This is a simulated summary of KVKK legal updates. Replace with GPT later."
