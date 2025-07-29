import os
import requests

NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
HF_API_TOKEN = os.environ.get("HF_API_TOKEN")

# ใช้คำค้นหลายแบบ เพื่อ fallback หากอันใดอันหนึ่งไม่เจอข่าว
SEARCH_QUERIES = ["ข่าว", "ประเทศไทย", "เศรษฐกิจ", "การเมือง", "นโยบายรัฐ", "ผู้บริโภค"]

def get_latest_news():
    for query in SEARCH_QUERIES:
        print(f"📡 Fetching query: {query}")
        url = f"https://newsapi.org/v2/everything?q={query}&language=th&pageSize=5&apiKey={NEWS_API_KEY}"
        response = requests.get(url)
        print(f"📡 Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ Error from NewsAPI: {response.status_code} -> {response.text}")
            continue

        data = response.json()
        articles = data.get("articles", [])
        if not articles:
            continue

        # หาอันแรกที่มี title และ content
        for article in articles:
            title = article.get("title", "").strip()
            content = article.get("content") or article.get("description") or ""
            if title and content:
                print(f"✅ พบข่าว: {title[:50]}")
                return title, content

    print("❌ ไม่พบข่าวในหมวดหมู่ที่กำหนด")
    return None, None


def summarize_text(text):
    """สรุปข้อความด้วย Hugging Face Inference API"""
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    payload = {
        "inputs": text,
        "parameters": {"max_length": 150, "min_length": 40, "do_sample": False}
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        try:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get("summary_text", "")
            else:
                print("❌ Response JSON structure unexpected:", result)
                return ""
        except Exception as e:
            print("❌ Error parsing summary response:", e)
            return ""
    else:
        print(f"❌ Hugging Face API error {response.status_code}: {response.text}")
        return ""
