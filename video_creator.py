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
    headers = {"Authorization": PEXELS_API_KEY}
    url = f"https://api.pexels.com/videos/search?query={query}&per_page={per_page}"
    response = requests.get(url, headers=headers)
    data = response.json()

    if 'videos' in data and data['videos']:
        video_url = data['videos'][0]['video_files'][0]['link']
        video_path = "temp_video.mp4"
        video_data = requests.get(video_url)
        with open(video_path, 'wb') as f:
            f.write(video_data.content)
        return video_path
    else:
        print(f"❌ ไม่พบวิดีโอสำหรับ keyword: {query}")
        return None

def create_final_video(audio_path, video_path, title_text, output_filename="final_video.mp4"):
    cmd = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-i", audio_path,
        "-vf", f"drawtext=fontfile=/usr/share/fonts/truetype/thai/THSarabunNew.ttf:text='{title_text}':fontcolor=white:fontsize=30:x=(w-text_w)/2:y=50:box=1:boxcolor=black@0.5",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-shortest",
        output_filename
    ]
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ ffmpeg error: {e}")
        return None
    return output_filename

