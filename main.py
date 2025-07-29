import os
from news_fetcher import get_latest_news, summarize_text
from video_creator import create_audio_from_text, download_pexels_video, create_final_video
from youtube_uploader import upload_video

def process_single_video():
    print("🚀 เริ่มกระบวนการสร้างวิดีโอ...")
    
    # 1. ดึงและสรุปข่าว
    title, content = get_latest_news()
    if not title:
        print("ไม่พบข่าวใหม่")
        return
    
    print(f"ข่าวที่ได้: {title}")
    summary = summarize_text(content)
    if not summary:
        print("สรุปข่าวไม่สำเร็จ")
        return

    # 2. สร้างเสียงและวิดีโอ
    audio_file = create_audio_from_text(summary)
    video_keyword = title.split(" ")[0]
    video_file = download_pexels_video(video_keyword)
    if not audio_file or not video_file:
        print("❌ ไม่สามารถสร้างไฟล์เสียงหรือวิดีโอได้")
        return

    final_video_file = create_final_video(audio_file, video_file, title)
    print(f"✅ สร้างวิดีโอสำเร็จ: {final_video_file}")
    
    # 3. อัปโหลดไป YouTube
    upload_video(
        file=final_video_file,
        title=title,
        description=summary,
        tags=["ข่าว", "สรุปข่าว", "ข่าววันนี้"]
    )
    print(f"📤 อัปโหลดวิดีโอ '{title}' เรียบร้อยแล้ว")

    # 4. ลบไฟล์ชั่วคราว
    os.remove(audio_file)
    os.remove(video_file)
    os.remove(final_video_file)
    print("🗑️ ลบไฟล์ชั่วคราวเรียบร้อย")

if __name__ == "__main__":
    for i in range(5):
        print(f"\n--- คลิปที่ {i+1}/5 ---")
        try:
            process_single_video()
        except Exception as e:
            print(f"เกิดข้อผิดพลาด: {e}")