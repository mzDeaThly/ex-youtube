# tts_generator.py
import os
import requests

HF_API_KEY = os.getenv("HF_API_KEY")

def generate_voice(text, output_file="temp_audio.wav"):
    """ใช้ Hugging Face TTS API (facebook/fastspeech2-en-ljspeech)"""
    payload = {
        "inputs": text
    }
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        "https://api-inference.huggingface.co/models/suno/bark",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        with open(output_file, "wb") as f:
            f.write(response.content)
        return output_file
    else:
        raise Exception(f"🛑 HuggingFace TTS Failed: {response.status_code} - {response.text}")
