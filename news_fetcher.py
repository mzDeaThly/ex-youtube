import os
import openai
import requests

# สำหรับ OpenRouter หรือ API ที่ compatible กับ OpenAI
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

openai.api_key = OPENROUTER_API_KEY
openai.api_base = "https://openrouter.ai/api/v1"  # เปลี่ยน endpoint ให้ตรงกับผู้ให้บริการ

def get_latest_news():
    """ดึงข่าวทั่วไปโดยใช้คำค้น (query)"""
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    queries = ["ข่าว", "ประเทศไทย", "เศรษฐกิจ", "การเมือง"]

    for query in queries:
        url = f"https://newsapi.org/v2/everything?q={query}&language=th&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
        response = requests.get(url)
        print(f"📡 Fetching query: {query} | Status: {response.status_code}")

        if response.status_code != 200:
            continue

        articles = response.json().get("articles", [])
        if not articles:
            continue

        first = articles[0]
        title = first.get("title")
        content = first.get("content") or first.get("description") or ""
        print(f"✅ พบข่าว: {title}")
        return title, content

    print("❌ ไม่พบข่าวใหม่")
    return None, None


def summarize_text(content):
    """สรุปข่าวโดยใช้ GPT-4 ผ่าน OpenRouter"""
    try:
        response = openai.ChatCompletion.create(
            model="openai/gpt-4",  # หรือ gpt-3.5-turbo ได้เช่นกัน
            messages=[
                {"role": "system", "content": "คุณคือผู้สรุปข่าวภาษาไทย สำหรับคลิปวิดีโอ 60 วินาที"},
                {"role": "user", "content": f"สรุปข่าวต่อไปนี้ให้น่าสนใจ เข้าใจง่าย และกระชับ: \n\n{content}"}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ สรุปข่าวล้มเหลว: {e}")
        return content[:300] + "..."  # fallback
