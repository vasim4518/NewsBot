import requests
import os

NEWS_API_KEY = os.environ["NEWS_API_KEY"]
WHATSAPP_TOKEN = os.environ["WHATSAPP_TOKEN"]
PHONE_NUMBER_ID = os.environ["PHONE_NUMBER_ID"]
RECIPIENT_PHONE = os.environ["RECIPIENT_PHONE"]

# Step 1: Fetch top headlines
url = f"https://newsapi.org/v2/top-headlines?country=us&pageSize=5&apiKey={NEWS_API_KEY}"
response = requests.get(url)
articles = response.json().get("articles", [])[:5]

# Step 2: Build template parameters (headline, url, description for each article)
parameters = []
for a in articles:
    title = a.get("title", "No title")
    url = a.get("url", "No link")
    desc = a.get("description", "No description available")
    parameters.extend([
        {"type": "text", "text": title[:200]},  # keep short
        {"type": "text", "text": url[:200]},    # avoid too long links
        {"type": "text", "text": desc[:200]}    # short description
    ])

# Step 3: WhatsApp API call
payload = {
    "messaging_product": "whatsapp",
    "to": RECIPIENT_PHONE,
    "type": "template",
    "template": {
        "name": "news",   # 🔹 Use the NEW template name you created
        "language": {"code": "en_US"},
        "components": [
            {
                "type": "body",
                "parameters": parameters
            }
        ]
    }
}

headers = {
    "Authorization": f"Bearer {WHATSAPP_TOKEN}",
    "Content-Type": "application/json"
}

send = requests.post(
    f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages",
    headers=headers,
    json=payload
)

print("API Response:", send.json())
