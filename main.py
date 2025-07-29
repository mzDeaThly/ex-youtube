import os
from news_fetcher import get_latest_news, summarize_text
from video_creator import create_audio_from_text, download_pexels_video, create_final_video
from youtube_uploader import upload_video

CLIENT_SECRET_PATH = "/etc/secrets/client_secret.json"

def prepare_client_secret():
    # ตรวจสอบว่าไฟล์ client_secret.json อยู่ในที่ที่ mount ไว้หรือยัง
    if not os.path.exists(CLIENT_SECRET_PATH):
        raise FileNotFoundError(f"ไม่พบไฟล์ client_secret.json ที่ {CLIENT_SECRET_PATH}")
    else:
        print(f"🔐 ใช้ client_secret.json จาก {CLIENT_SECRET_PATH}")

def process_single_video():
    print("🚀 เริ่มกระบวนการสร้างวิดีโอ...")

    title, content = get_latest_news()
    if not title or not content:
        print("❌ ไม่พบข่าวใหม่")
        return

    print(f"📰 ข่าวที่ดึงมา: {title}")
    summary = summarize_text(content)
    print(f"📝 สรุปข่าว: {summary}")

    audio_file = create_audio_from_text(summary)
    print(f"🔊 สร้างเสียงเสร็จ: {audio_file}")

    keyword = title.split(" ")[0]
    video_file = download_pexels_video(keyword)
    print(f"🎬 วิดีโอที่ใช้: {video_file}")

    final_video_file = create_final_video(audio_file, video_file, title)
    print(f"✅ วิดีโอไฟนอล: {final_video_file}")

    upload_video(
        file=final_video_file,
        title=title,
        description=summary,
        tags=["ข่าว", "สรุปข่าว", "ข่าววันนี้"],
        client_secret_path=CLIENT_SECRET_PATH
    )

    for f in [audio_file, video_file, final_video_file]:
        if os.path.exists(f):
            os.remove(f)
            print(f"🗑️ ลบไฟล์: {f}")

if __name__ == "__main__":
    prepare_client_secret()

    for i in range(5):
        print(f"\n--- ▶️ คลิปที่ {i+1}/5 ---")
        try:
            process_single_video()
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาด: {e}")
