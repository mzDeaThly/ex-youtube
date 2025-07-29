import os
import requests

NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
HF_API_TOKEN = os.environ.get("HF_API_TOKEN")


def get_latest_news(keywords=["ข่าว", "ประเทศไทย", "เศรษฐกิจ"]):
    """ดึงข่าวจากหลาย keyword จนกว่าจะเจอ"""
    for keyword in keywords:
        print(f"📡 Fetching query: {keyword}")
        url = f"https://newsapi.org/v2/everything?q={keyword}&language=th&pageSize=5&apiKey={NEWS_API_KEY}"
        response = requests.get(url)
        print(f"📡 Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if data.get("articles"):
                article = data["articles"][0]
                return article["title"], article["description"] or article["content"]
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
