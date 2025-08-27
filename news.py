import os
import requests

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
RECIPIENT_PHONE = os.getenv("RECIPIENT_PHONE")

# 1. Fetch top headlines
# NewsAPI
# def get_news():
#     url = f"https://newsapi.org/v2/top-headlines?country=us&category=general&pageSize=5&apiKey={NEWS_API_KEY}"
#     response = requests.get(url)
#     data = response.json()
#     print("Raw API Response:",data)
#     articles = data.get("articles", [])
#     return [(a["title"], a["url"]) for a in articles[:5]]

# GNews
def get_news():
    url = f"https://gnews.io/api/v4/top-headlines?token={GNEWS_API_KEY}&lang=en&country=in&max=5"
    res = requests.get(url).json()
    print("GNews response:", res)  # Debugging
    articles = res.get("articles", [])
    return [(a.get("title", "No title"), a.get("url", "")) for a in articles]



# 2. Send WhatsApp Template Message
def send_whatsapp_news(news_items):
    components = []
    for title, link in news_items[:5]:  # ensure max 5
        components.append(title)        # headline
        components.append(link)         # url

    # pad missing values if less than 10
    while len(components) < 10:
        components.append("N/A")

    payload = {
        "messaging_product": "whatsapp",
        "to": RECIPIENT_PHONE,
        "type": "template",
        "template": {
            "name": "news",
            "language": {"code": "en_US"},
            "components": [
                {
                    "type": "body",
                    "parameters": [{"type": "text", "text": text} for text in components]
                }
            ]
        }
    }

    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=payload)
    print("API Response:", response.json())


if __name__ == "__main__":
    news_items = get_news()
    if news_items:
        send_whatsapp_news(news_items)
    else:
        print("No news articles found!")
