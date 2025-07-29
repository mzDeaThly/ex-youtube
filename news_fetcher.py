import os
import requests
import random
import google.generativeai as genai

NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# ตั้งค่าคีย์สำหรับ Gemini
genai.configure(api_key=GEMINI_API_KEY)

# หมวดหมู่ข่าวที่รองรับ
CATEGORIES = ["general", "business", "entertainment", "health", "science", "sports", "technology"]

def get_latest_news(categories=CATEGORIES, country="th"):
    """
    ดึงข่าวล่าสุดจากหลายหมวดหมู่ของ NewsAPI
    """
    random.shuffle(categories)  # สุ่มหมวด เพื่อให้ข่าวหลากหลาย
    for category in categories:
        url = f"https://newsapi.org/v2/top-headlines?country={country}&category={category}&apiKey={NEWS_API_KEY}"
        response = requests.get(url)
        print(f"📡 Fetching news: {category} | Status: {response.status_code}")
        
        if response.status_code != 200:
            continue

        data = response.json()
        articles = data.get("articles", [])
        if articles:
            for article in articles:
                title = article.get("title", "")
                content = article.get("content") or article.get("description") or ""
                if title and content:
                    print(f"✅ พบข่าวจากหมวด: {category}")
                    return title, content
    print("❌ ไม่พบข่าวในหมวดหมู่ที่กำหนด")
    return None, None

def summarize_text(content):
    """
    สรุปข่าวด้วย Gemini AI
    """
    try:
        model = genai.GenerativeModel("gemini-pro")
        prompt = f"สรุปข่าวนี้เป็นภาษาไทย ภายใน 60 วินาที อ่านเข้าใจง่ายและน่าสนใจ:\n\n{content}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"❌ สรุปข่าวล้มเหลว: {e}")
        return content
