import os
import requests
import google.generativeai as genai

NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)

def get_latest_news():
    """ดึงข่าวล่าสุดจาก NewsAPI หัวข้อธุรกิจในไทย"""
    url = f"https://newsapi.org/v2/top-headlines?country=th&category=business&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"❌ Error fetching news: {response.status_code}")
        return None, None

    data = response.json()
    articles = data.get('articles', [])
    if not articles:
        return None, None

    first = articles[0]
    title = first.get('title')
    content = first.get('content') or first.get('description') or ""
    return title, content

def summarize_text(content):
    """สรุปเนื้อหาข่าวด้วย Gemini API"""
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"โปรดสรุปข่าวต่อไปนี้เป็นภาษาไทยสำหรับทำคลิปวิดีโอ 60 วินาที ให้อ่านง่ายและน่าสนใจ: '{content}'"
    response = model.generate_content(prompt)
    return response.text
