import os
import subprocess
from gtts import gTTS
import requests

PEXELS_API_KEY = os.environ.get('PEXELS_API_KEY')

def create_audio_from_text(text, filename="temp_audio.mp3"):
    """สร้างไฟล์เสียงพากย์ภาษาไทยด้วย gTTS"""
    tts = gTTS(text=text, lang='th')
    tts.save(filename)
    return filename

def download_pexels_video(query, per_page=1):
    """ดาวน์โหลดวิดีโอจาก Pexels API พร้อม fallback"""
    headers = {"Authorization": PEXELS_API_KEY}
    url = f"https://api.pexels.com/videos/search?query={query}&per_page={per_page}"
    response = requests.get(url, headers=headers)
    print(f"📡 Fetching query: {query}")
    print(f"📡 Status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        videos = data.get('videos', [])
        if videos:
            video_files = videos[0].get('video_files', [])
            if video_files:
                video_url = video_files[0]['link']
                video_path = "temp_video.mp4"
                video_data = requests.get(video_url)
                with open(video_path, 'wb') as f:
                    f.write(video_data.content)
                return video_path

    # Fallback
    print(f"⚠️ ไม่พบวิดีโอจาก Pexels สำหรับ keyword: {query} → ใช้ default.mp4")
    return "default.mp4"  # ต้องมีไฟล์นี้อยู่ในโปรเจกต์

def create_final_video(audio_path, video_path, title_text, output_filename="final_video.mp4"):
    """ประกอบวิดีโอและเสียง พร้อมใส่ข้อความ overlay ด้วย ffmpeg CLI"""
    cmd = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-i", audio_path,
        "-vf", f"drawtext=text='{title_text}':fontcolor=white:fontsize=30:x=(w-text_w)/2:y=50:box=1:boxcolor=black@0.5:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-shortest",
        output_filename
    ]
    subprocess.run(cmd, check=True)
    return output_filename
