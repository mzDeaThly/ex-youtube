import os
from gtts import gTTS
from moviepy.editor import *
import requests

PEXELS_API_KEY = os.environ.get('PEXELS_API_KEY')

def create_audio_from_text(text, filename="temp_audio.mp3"):
    try:
        tts = gTTS(text=text, lang='th')
        tts.save(filename)
        return filename
    except Exception as e:
        print(f"❌ สร้างเสียงล้มเหลว: {e}")
        return None

def download_pexels_video(query, per_page=1):
    headers = {"Authorization": PEXELS_API_KEY}
    url = f"https://api.pexels.com/videos/search?query={query}&per_page={per_page}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"❌ ดึงวิดีโอจาก Pexels ไม่สำเร็จ: {response.status_code}")
        return None

    videos = response.json().get("videos", [])
    if not videos:
        print("❌ ไม่พบวิดีโอจาก Pexels")
        return None

    video_url = videos[0]['video_files'][0]['link']
    filename = "temp_video.mp4"
    video_data = requests.get(video_url)
    with open(filename, 'wb') as f:
        f.write(video_data.content)
    return filename

def create_final_video(audio_path, video_path, title_text, output_filename="final_video.mp4"):
    if not os.path.exists(audio_path) or not os.path.exists(video_path):
        raise FileNotFoundError("ไม่พบไฟล์เสียงหรือวิดีโอ")

    audio_clip = AudioFileClip(audio_path)
    video_clip = VideoFileClip(video_path).subclip(0, audio_clip.duration)

    try:
        txt_clip = TextClip(title_text, fontsize=70, color='white', font='Tahoma-Bold',
                            bg_color='black', size=video_clip.size, method='caption')
        txt_clip = txt_clip.set_pos('center').set_duration(5)
        final_clip = CompositeVideoClip([video_clip, txt_clip])
    except Exception as e:
        print(f"⚠️ ไม่สามารถแสดงข้อความ: {e} — ข้าม overlay ไป")
        final_clip = video_clip

    final_clip.audio = audio_clip
    final_clip.write_videofile(output_filename, codec="libx264", fps=24, audio_codec="aac")
    return output_filename