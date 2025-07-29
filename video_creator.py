import os
from gtts import gTTS
from moviepy.editor import *
import requests # สำหรับ Pexels

PEXELS_API_KEY = os.environ.get('PEXELS_API_KEY')

def create_audio_from_text(text, filename="temp_audio.mp3"):
    """สร้างไฟล์เสียงพากย์ภาษาไทย"""
    tts = gTTS(text=text, lang='th')
    tts.save(filename)
    return filename

def download_pexels_video(query, per_page=1):
    """ดาวน์โหลดวิดีโอจาก Pexels"""
    headers = {"Authorization": PEXELS_API_KEY}
    url = f"https://api.pexels.com/videos/search?query={query}&per_page={per_page}"
    response = requests.get(url, headers=headers)
    # (โค้ดส่วนดาวน์โหลดไฟล์วิดีโอจริง) ...
    # สมมติว่าดาวน์โหลดมาแล้วชื่อ "temp_video.mp4"
    return "temp_video.mp4"

def create_final_video(audio_path, video_path, title_text, output_filename="final_video.mp4"):
    """ประกอบร่างวิดีโอด้วย MoviePy"""
    audio_clip = AudioFileClip(audio_path)
    video_clip = VideoFileClip(video_path).subclip(0, audio_clip.duration) # ตัดวิดีโอให้ยาวเท่าเสียง

    # สร้าง Text Overlay
    txt_clip = TextClip(title_text, fontsize=70, color='white', font='Tahoma-Bold',
                        bg_color='black', size=video_clip.size)
    txt_clip = txt_clip.set_pos('center').set_duration(5) # แสดงหัวข้อ 5 วินาทีแรก

    # รวมทุกอย่างเข้าด้วยกัน
    final_clip = CompositeVideoClip([video_clip, txt_clip])
    final_clip.audio = audio_clip
    final_clip.write_videofile(output_filename, codec="libx264", fps=24)
    
    return output_filename