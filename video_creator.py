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
    """ดาวน์โหลดวิดีโอจาก Pexels API"""
    headers = {"Authorization": PEXELS_API_KEY}
    url = f"https://api.pexels.com/videos/search?query={query}&per_page={per_page}"
    response = requests.get(url, headers=headers)
    data = response.json()
    if data['videos']:
        video_url = data['videos'][0]['video_files'][0]['link']  # เลือกคุณภาพไฟล์แรก
        video_path = "temp_video.mp4"
        video_data = requests.get(video_url)
        with open(video_path, 'wb') as f:
            f.write(video_data.content)
        return video_path
    else:
        raise Exception("ไม่พบวิดีโอจาก Pexels")

def create_final_video(audio_path, video_path, title_text, output_filename="final_video.mp4"):
    """ประกอบวิดีโอและเสียง พร้อมใส่ข้อความ overlay ด้วย ffmpeg CLI"""
    # ใส่ข้อความ overlay ด้วย drawtext filter (ต้องติดตั้ง fonts ภาษาไทยใน OS/Docker)
    cmd = [
        "ffmpeg",
        "-y",  # ลบไฟล์เก่าถ้ามี
        "-i", video_path,
        "-i", audio_path,
        "-vf", f"drawtext=text='{title_text}':fontcolor=white:fontsize=30:x=(w-text_w)/2:y=50:box=1:boxcolor=black@0.5",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-shortest",
        output_filename
    ]
    subprocess.run(cmd, check=True)
    return output_filename
