import os
import requests

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
RECIPIENT_PHONE = os.getenv("RECIPIENT_PHONE")

def get_top_news():
    url = f"https://newsapi.org/v2/top-headlines?language=en&pageSize=5&apiKey={NEWS_API_KEY}"
    res = requests.get(url)
    data = res.json()

    if data.get("status") != "ok":
        return ["Failed to fetch news"]

    headlines = []
    for i, article in enumerate(data.get("articles", []), start=1):
        title = article.get("title", "No title")
        url = article.get("url", "")
        headlines.append(f"{i}. {title}\n{url}")
    return headlines

def send_whatsapp_message(message):
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": RECIPIENT_PHONE,
        "type": "text",
        "text": {"body": message}
    }
    response = requests.post(url, headers=headers, json=payload)
    print(response.json())

if __name__ == "__main__":
    news_list = get_top_news()
    news_message = "📰 Top 5 World News for Today:\n\n" + "\n\n".join(news_list)
    send_whatsapp_message(news_message)
