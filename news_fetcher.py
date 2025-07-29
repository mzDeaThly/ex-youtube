import os
import requests

NEWS_API_KEY = os.environ.get('NEWS_API_KEY', '')

def get_latest_news(queries=None):
    """ดึงข่าวล่าสุดจาก NewsAPI โดยใช้หลายคำค้นหา fallback"""
    if queries is None:
        queries = ["ข่าว", "ประเทศไทย", "เศรษฐกิจ"]

    for query in queries:
        url = f"https://newsapi.org/v2/everything?q={query}&language=th&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
        response = requests.get(url)
        print(f"📡 Fetching query: {query} | Status: {response.status_code}")
        if response.status_code != 200:
            continue
        data = response.json()
        articles = data.get('articles', [])
        if articles:
            first = articles[0]
            title = first.get('title')
            content = first.get('content') or first.get('description') or ""
            return title, content
    return None, None

def summarize_text(text):
    """สรุปข้อความง่าย ๆ (ฟรี) โดยตัดความยาวให้พอดีสำหรับคลิป 1-2 นาที"""
    # ตัดข้อความไม่เกิน 400 ตัวอักษร
    if len(text) > 400:
        text = text[:400] + "..."
    return text
