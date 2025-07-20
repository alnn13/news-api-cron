import requests
from datetime import datetime

API_TOKEN = "1urHU2kMsKgvEl1PJ1dZJPYADozt1Fwf8pl80NHd"  
URL = f"https://api.marketaux.com/v1/news/all?api_token={API_TOKEN}&limit=5"

response = requests.get(URL)
data = response.json()

print(f"🧠 Economic Brief – {datetime.now().strftime('%d %B %Y - %H:%M')}\n")

for i, article in enumerate(data.get("data", []), 1):
    print(f"{i}. {article['title']}")
    print(f"   Source: {article['source']}")
    print(f"   Date: {article['published_at']}")
    print(f"   Link: {article['url']}\n")
