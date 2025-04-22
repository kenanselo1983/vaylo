import requests
from bs4 import BeautifulSoup

def fetch_kvkk_updates():
    url = "https://www.kvkk.gov.tr/Icerik/6639/KVKK-Hakkinda"
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.content, "html.parser")

    content_div = soup.find("div", class_="icerik")
    if not content_div:
        return "❌ Failed to find content on KVKK site."

    paragraphs = content_div.find_all("p")
    text = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

    return text or "❌ No content extracted."
