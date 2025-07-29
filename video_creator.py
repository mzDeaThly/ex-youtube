import os
import subprocess
import requests
from gtts import gTTS

PEXELS_API_KEY = os.environ.get('PEXELS_API_KEY', '')
BGM_FILE = "bgm.mp3"
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"  # ปรับตาม OS คุณ

def create_audio_from_text(text, filename="temp_audio.mp3"):
    """สร้างไฟล์เสียงพากย์ภาษาไทยด้วย gTTS"""
    tts = gTTS(text=text, lang='th')
    tts.save(filename)
    return filename

def create_default_video_if_missing(filename="default.mp4"):
    """สร้างวิดีโอพื้นหลังสีดำ พร้อมข้อความง่าย ๆ กรณีไม่เจอวิดีโอ"""
    if os.path.exists(filename):
        print(f"✅ พบไฟล์ default video: {filename}")
        return filename

    print(f"⚠️ ไม่พบไฟล์ {filename} สร้างใหม่อัตโนมัติ...")
    cmd = [
        "ffmpeg",
        "-f", "lavfi",
        "-i", "color=c=black:s=1080x1920:d=15",
        "-vf", "drawtext=text='ข่าววันนี้':fontsize=64:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2",
        "-c:v", "libx264",
        "-t", "15",
        "-pix_fmt", "yuv420p",
        filename
    ]
    subprocess.run(cmd, check=True)
    print(f"✅ สร้าง default video เสร็จ: {filename}")
    return filename

def download_pexels_video(query, per_page=1):
    """ดาวน์โหลดวิดีโอแนวตั้ง (1080x1920) จาก Pexels API พร้อม fallback"""
    headers = {"Authorization": PEXELS_API_KEY}
    url = f"https://api.pexels.com/videos/search?query={query}&per_page={per_page}"
    response = requests.get(url, headers=headers)
    print(f"📡 Fetching query: {query}")
    print(f"📡 Status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        videos = data.get('videos', [])
        # หา video แนวตั้งที่ใกล้เคียง 1080x1920
        for vid in videos:
            for vf in vid.get('video_files', []):
                if vf['width'] == 1080 and vf['height'] == 1920:
                    video_url = vf['link']
                    video_path = "temp_video.mp4"
                    video_data = requests.get(video_url)
                    with open(video_path, 'wb') as f:
                        f.write(video_data.content)
                    return video_path

    print(f"⚠️ ไม่พบวิดีโอแนวตั้งจาก Pexels สำหรับ keyword: {query} → ใช้ default.mp4")
    return create_default_video_if_missing()

def create_final_video(audio_path, video_path, title_text, output_filename="final_video.mp4"):
    """ประกอบวิดีโอและเสียง พร้อมใส่ข้อความ overlay subtitle และ BGM"""
    # ใส่ซับไตเติ้ล (ข้อความข่าว) ที่ด้านล่างวิดีโอ และ zoom in motion effect
    cmd = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-i", audio_path,
        "-i", BGM_FILE,
        "-filter_complex",
        # zoom in slow, overlay text (subtitle), mix เสียงพูด + BGM ลดเสียง bgm ลง 20dB
        f"[0:v]zoompan=z='min(zoom+0.0005,1.05)':d=125,drawtext=fontfile={FONT_PATH}:text='{title_text}':fontcolor=white:fontsize=36:x=(w-text_w)/2:y=h-100:box=1:boxcolor=black@0.6:boxborderw=5[v];" +
        "[1:a]volume=1[a1];" +
        "[2:a]volume=0.2[a2];" +
        "[a1][a2]amix=inputs=2:duration=first:dropout_transition=3[a]",
        "-map", "[v]",
        "-map", "[a]",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        "-pix_fmt", "yuv420p",
        "-s", "1080x1920",
        output_filename
    ]
    subprocess.run(cmd, check=True)
    return output_filename
