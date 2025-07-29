import os
import requests

NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
HF_API_TOKEN = os.environ.get("HF_API_TOKEN")

def get_latest_news():
    """ดึงข่าวล่าสุดจาก NewsAPI หมวด general ประเทศไทย"""
    url = f"https://newsapi.org/v2/top-headlines?country=th&category=general&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"❌ Error fetching news: {response.status_code}")
        return None, None

    data = response.json()
    articles = data.get("articles", [])
    if not articles:
        return None, None

    first = articles[0]
    title = first.get("title")
    content = first.get("content") or first.get("description") or ""
    return title, content

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
