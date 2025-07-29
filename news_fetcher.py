import os
import requests
import google.generativeai as genai

NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)

def get_latest_news():
    """
    ดึงข่าวจาก NewsAPI แบบไม่มี country restriction โดยใช้ endpoint everything
    """
    queries = ["ข่าว", "เศรษฐกิจ", "ประเทศไทย", "breaking news", "ข่าววันนี้"]
    for query in queries:
        url = (
            f"https://newsapi.org/v2/everything?"
            f"q={query}&language=th&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
        )
        response = requests.get(url)
        print(f"📡 Fetching query: {query} | Status: {response.status_code}")
        
        if response.status_code != 200:
            continue

        data = response.json()
        articles = data.get("articles", [])
        if articles:
            for article in articles:
                title = article.get("title", "")
                content = article.get("content") or article.get("description") or ""
                if title and content:
                    print(f"✅ พบข่าว: {title[:60]}")
                    return title, content

    print("❌ ไม่พบข่าวในคำค้นที่กำหนด")
    return None, None

def summarize_text(content):
    """สรุปเนื้อหาข่าวด้วย Gemini API"""
    try:
        model = genai.GenerativeModel(model_name="models/gemini-pro")
        prompt = (
            "โปรดสรุปข่าวต่อไปนี้เป็นภาษาไทยสำหรับทำคลิปวิดีโอ 60 วินาที "
            "ให้อ่านง่ายและน่าสนใจ:\n\n"
            f"{content}"
        )
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดจาก Gemini API: {e}")
        return ""

