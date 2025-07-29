# text_to_script.py
import os
import requests

HF_API_KEY = os.getenv("HF_API_KEY")

def generate_script(summary_text):
    """ใช้ Hugging Face Text Generation (เช่น google/flan-t5) เพื่อแต่งสคริปต์แนว TikTok"""
    prompt = f"สรุปข่าวด้านล่างนี้ให้เหมาะกับคลิป TikTok สนุกๆ 1-2 นาที โดยใช้โทนเสียงผู้หญิงจริงจัง พร้อมมีปฏิสัมพันธ์:\n\n{summary_text}\n\nสคริปต์:"
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 300, "temperature": 0.9},
    }

    response = requests.post(
        "https://api-inference.huggingface.co/models/google/flan-t5-large",
        headers={"Authorization": f"Bearer {HF_API_KEY}"},
        json=payload
    )
    if response.status_code != 200:
        raise Exception(f"🛑 HuggingFace Error: {response.status_code} - {response.text}")

    result = response.json()
    return result[0]["generated_text"] if isinstance(result, list) else result
