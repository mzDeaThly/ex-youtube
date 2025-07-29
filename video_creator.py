# video_creator.py
import os
import subprocess
import textwrap

def ensure_default_video():
    if not os.path.exists("assets/default.mp4"):
        print("⚠️ กำลังสร้าง default.mp4 (background วิดีโอ)...")
        os.makedirs("assets", exist_ok=True)
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=black:s=720x1280:d=120",
            "assets/default.mp4"
        ], check=True)
        print("✅ default.mp4 สร้างเสร็จ")

def format_subtitle(text, width=30):
    return textwrap.fill(text, width=width).replace("\n", "\\n")

def create_video_with_audio_subtitle(audio_path, text, output_file="final_video.mp4"):
    ensure_default_video()
    subtitle = format_subtitle(text)
    cmd = [
        "ffmpeg",
        "-y",
        "-i", "assets/default.mp4",
        "-i", audio_path,
        "-vf", f"drawtext=text='{subtitle}':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:fontcolor=white:fontsize=40:x=(w-text_w)/2:y=h-200:box=1:boxcolor=black@0.5",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        output_file
    ]
    subprocess.run(cmd, check=True)
    return output_file
