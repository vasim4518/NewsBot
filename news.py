import requests, os

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
RECIPIENT_PHONE = os.getenv("RECIPIENT_PHONE")

# --- Get Top 5 News ---
url = f"https://newsapi.org/v2/top-headlines?language=en&pageSize=5&apiKey={NEWS_API_KEY}"
articles = requests.get(url).json().get("articles", [])
news_text = "🌍 Top 5 News Today:\n" + "\n".join(
    [f"{i+1}. {a['title']}" for i,a in enumerate(articles)]
)

# --- Send to WhatsApp ---
send_url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
headers = {
    "Authorization": f"Bearer {WHATSAPP_TOKEN}",
    "Content-Type": "application/json"
}
payload = {
    "messaging_product": "whatsapp",
    "to": RECIPIENT_PHONE,
    "type": "text",
    "text": {"body": news_text}
}

res = requests.post(send_url, headers=headers, json=payload)
print("WhatsApp response:", res.json())
