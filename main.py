import os
from news_fetcher import get_latest_news, summarize_text
from video_creator import create_audio_from_text, download_pexels_video, create_final_video
from youtube_uploader import upload_video

CLIENT_SECRET_PATH = "/etc/secrets/client_secret.json"
DEFAULT_VIDEO_PATH = "default.mp4"  # fallback วิดีโอ

def prepare_client_secret():
    if not os.path.exists(CLIENT_SECRET_PATH):
        raise FileNotFoundError(f"❌ ไม่พบ client_secret.json ที่ {CLIENT_SECRET_PATH}")
    print(f"🔐 ใช้ client_secret.json จาก {CLIENT_SECRET_PATH}")

def process_single_video():
    print("🚀 เริ่มกระบวนการสร้างวิดีโอ...")

    title, content = get_latest_news()
    if not title or not content:
        print("❌ ไม่พบข่าวใหม่")
        return

    print(f"📰 ข่าวที่ดึงมา: {title}")
    try:
        summary = summarize_text(content)
        print(f"📝 สรุปข่าว: {summary}")
    except Exception as e:
        print(f"❌ สรุปข่าวล้มเหลว: {e}")
        return

    if not summary or not summary.strip():
        print("❌ ไม่มีเนื้อหาสำหรับสร้างเสียง")
        return

    try:
        audio_file = create_audio_from_text(summary)
        print(f"🔊 สร้างเสียงเสร็จ: {audio_file}")
    except Exception as e:
        print(f"❌ สร้างเสียงล้มเหลว: {e}")
        return

    try:
        keyword = title.split(" ")[0]
        video_file = download_pexels_video(keyword)
        print(f"🎬 วิดีโอที่ใช้: {video_file}")
    except Exception as e:
        print(f"⚠️ ไม่พบวิดีโอจาก Pexels: {e}")
        if os.path.exists(DEFAULT_VIDEO_PATH):
            video_file = DEFAULT_VIDEO_PATH
            print(f"🎬 ใช้วิดีโอ fallback: {DEFAULT_VIDEO_PATH}")
        else:
            print("❌ ไม่มีวิดีโอให้ใช้แม้ fallback")
            return

    try:
        final_video_file = create_final_video(audio_file, video_file, title)
        print(f"✅ วิดีโอไฟนอล: {final_video_file}")
    except Exception as e:
        print(f"❌ ผสมวิดีโอล้มเหลว: {e}")
        return

    try:
        upload_video(
            file=final_video_file,
            title=title,
            description=summary,
            tags=["ข่าว", "สรุปข่าว", "ข่าววันนี้"],
            client_secret_path=CLIENT_SECRET_PATH
        )
    except Exception as e:
        print(f"❌ อัปโหลดวิดีโอล้มเหลว: {e}")

    # ล้างไฟล์ชั่วคราว
    for f in [audio_file, video_file, final_video_file]:
        if os.path.exists(f) and "default" not in f:
            os.remove(f)
            print(f"🗑️ ลบไฟล์: {f}")

if __name__ == "__main__":
    prepare_client_secret()

    for i in range(5):
        print(f"\n--- ▶️ คลิปที่ {i+1}/5 ---")
        try:
            process_single_video()
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาดรอบหลัก: {e}")
