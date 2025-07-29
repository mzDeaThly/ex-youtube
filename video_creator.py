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

def create_default_video_if_missing(filename="default.mp4"):
    """ตรวจสอบว่าไฟล์ default.mp4 มีไหม ถ้าไม่มีให้สร้างวิดีโอพื้นหลังพร้อมข้อความง่าย ๆ"""
    if os.path.exists(filename):
        print(f"✅ พบไฟล์ default video: {filename}")
        return filename

    print(f"⚠️ ไม่พบไฟล์ {filename} กำลังสร้างไฟล์ default video อัตโนมัติ...")
    cmd = [
        "ffmpeg",
        "-f", "lavfi",
        "-i", "color=c=black:s=1280x720:d=10",
        "-vf", "drawtext=text='ข่าววันนี้':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2",
        "-c:v", "libx264",
        "-t", "10",
        "-pix_fmt", "yuv420p",
        filename
    ]
    try:
        subprocess.run(cmd, check=True)
        print(f"✅ สร้างไฟล์ default video เสร็จ: {filename}")
        return filename
    except subprocess.CalledProcessError as e:
        print(f"❌ สร้าง default video ล้มเหลว: {e}")
        return None

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
    
    default_file = create_default_video_if_missing()
    return default_file or "default.mp4"

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
