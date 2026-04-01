from ddgs import DDGS
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

os.makedirs("data/bronze", exist_ok=True)

articles = []

print("💰 Searching for financial news...")

query = "2026 financial news OR stock market OR economy OR finance"

with DDGS() as ddgs:
    results = ddgs.news(query, max_results=20)

    for r in results:
        url = r["url"]
        source = r.get("source", "")
        date = r.get("date", "")

        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            title = soup.title.string if soup.title else "No title"

            paragraphs = soup.find_all("p")
            content = " ".join([p.get_text() for p in paragraphs])

            # softer filter
         

df = pd.DataFrame(articles)

if df.empty:
    print("❌ Still no data → tell me")
else:
    df.to_csv("data/bronze/news.csv", index=False)
    print(f"✅ Saved {len(df)} articles")
