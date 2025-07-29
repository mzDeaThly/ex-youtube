import os
import requests
import google.generativeai as genai

NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

def get_latest_news():
    url = f"https://newsapi.org/v2/top-headlines?country=th&category=business&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"❌ ดึงข่าวล้มเหลว: {response.status_code}")
        return None, None

    articles = response.json().get('articles', [])
    if articles:
        first = articles[0]
        content = first.get('content') or first.get('description') or first.get('title')
        return first['title'], content
    return None, None

def summarize_text(content):
    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = (
            "โปรดสรุปข่าวต่อไปนี้เป็นภาษาไทยสำหรับทำคลิปวิดีโอ 60 วินาที "
            "ให้อ่านง่าย กระชับ และน่าสนใจ:\n\n"
            f"{content}"
        )
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"❌ สรุปข่าวล้มเหลว: {e}")
        return None