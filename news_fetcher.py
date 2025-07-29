import os
import requests
import google.generativeai as genai

NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)

def get_latest_news():
    print(f"DEBUG: NEWS_API_KEY = {NEWS_API_KEY}")
    url = f"https://newsapi.org/v2/top-headlines?country=th&category=business&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    print(f"DEBUG: Status code = {response.status_code}")
    print(f"DEBUG: Response = {response.text[:500]}")  # แสดง response แค่ 500 ตัวแรก
    if response.status_code != 200:
        print(f"❌ Error fetching news: {response.status_code}")
        return None, None

    data = response.json()
    articles = data.get('articles', [])
    if not articles:
        print("❌ No articles found in response")
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
