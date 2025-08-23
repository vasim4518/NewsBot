
import requests
import os

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
RECIPIENT_PHONE = os.getenv("RECIPIENT_PHONE")

# 1️⃣ Fetch top 5 news
news_url = f"https://newsapi.org/v2/top-headlines?language=en&pageSize=5&apiKey={NEWS_API_KEY}"
articles = requests.get(news_url).json().get("articles", [])
headlines = [a['title'] for a in articles]

# 2️⃣ Send via WhatsApp Cloud API
url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
headers = {
    "Authorization": f"Bearer {WHATSAPP_TOKEN}",
    "Content-Type": "application/json"
}

data = {
    "messaging_product": "whatsapp",
    "to": RECIPIENT_PHONE,
    "type": "template",
    "template": {
        "name": "daily_news",
        "language": {"code": "en_US"},
        "components": [
            {"type": "body", "parameters": [{"type": "text", "text": h} for h in headlines]}
        ]
    }
}

resp = requests.post(url, headers=headers, json=data)
print(resp.status_code, resp.text)
