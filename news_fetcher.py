import os
import requests
import google.generativeai as genai

NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)

# สามารถตั้งค่าคีย์เวิร์ดที่ต้องการค้นหาเพิ่มเติมได้
QUERY_KEYWORDS = ["ข่าว", "เศรษฐกิจ", "การเมือง", "เทคโนโลยี", "บันเทิง"]

def get_latest_news():
    """พยายามดึงข่าวจากคำค้นหาต่าง ๆ จนกว่าจะเจอ"""
    for query in QUERY_KEYWORDS:
        url = f"https://newsapi.org/v2/everything?q={query}&language=th&pageSize=3&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
        try:
            response = requests.get(url)
            print(f"📡 Fetching query: {query} | Status: {response.status_code}")
            if response.status_code != 200:
                continue
            data = response.json()
            articles = data.get("articles", [])
            if articles:
                first = articles[0]
                title = first.get("title", "").strip()
                content = (
                    first.get("content")
                    or first.get("description")
                    or first.get("title")
                )
                print(f"✅ พบข่าว: {title[:50]}")
                return title, content
        except Exception as e:
            print(f"❌ Error fetching news: {e}")
    print("❌ ไม่พบข่าวในหมวดหมู่ที่กำหนด")
    return None, None

def summarize_text(content):
    try:
        model = genai.GenerativeModel("gemini-pro")
        prompt = (
            "โปรดสรุปข่าวต่อไปนี้เป็นภาษาไทยสำหรับทำคลิปวิดีโอ 60 วินาที:\n\n"
            f"{content}"
        )
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดจาก Gemini API: {e}")
        print("🧩 ใช้ fallback summary แทน")
        return content[:300] + "..."  # fallback summary
