# main.py
import os
from dotenv import load_dotenv

from news_fetcher import get_latest_news
from text_to_script import generate_script
from tts_generator import generate_voice
from video_creator import create_video_with_audio_subtitle

load_dotenv()

def generate_tiktok_clip():
    print("🚀 เริ่มสร้างคลิปแนว TikTok")

    title, summary = get_latest_news()
    if not title or not summary:
        print("❌ ไม่พบข่าวใหม่")
        return

    print(f"📰 หัวข้อข่าว: {title}")
    print(f"📄 สรุปข่าว: {summary}")

    script = generate_script(summary)
    print(f"🗣️ สคริปต์ที่สร้าง: {script[:200]}...")

    audio_path = generate_voice(script)
    print(f"🔊 สร้างเสียงเสร็จ: {audio_path}")

    final_video = create_video_with_audio_subtitle(audio_path, script)
    print(f"🎬 วิดีโอสร้างเสร็จ: {final_video}")

if __name__ == "__main__":
    generate_tiktok_clip()
