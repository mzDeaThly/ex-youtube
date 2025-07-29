import os
import base64
import json
import pickle
import datetime

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# ----------------- 1. โหลด client_secret.json จาก ENV -----------------
def prepare_client_secret():
    secret = os.environ.get("CLIENT_SECRET_JSON")
    if secret and not os.path.exists("client_secret.json"):
        with open("client_secret.json", "w") as f:
            f.write(base64.b64decode(secret).decode())

# ----------------- 2. ฟังก์ชันอัปโหลด YouTube -----------------
def upload_video(file, title, description, tags=[]):
    """อัปโหลดวิดีโอขึ้น YouTube"""
    prepare_client_secret()

    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
    creds = None

    # โหลด token.json ถ้ามี
    if os.path.exists("token.json"):
        with open("token.json", "rb") as token:
            creds = pickle.load(token)

    # ถ้าไม่มี token หรือหมดอายุ
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # บันทึก token ใหม่
        with open("token.json", "wb") as token:
            pickle.dump(creds, token)

    # สร้างบริการ YouTube API
    youtube = build("youtube", "v3", credentials=creds)

    # ตั้งค่าข้อมูลวิดีโอ
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "25",  # News & Politics
        },
        "status": {
            "privacyStatus": "public",  # public | unlisted | private
        },
    }

    media = MediaFileUpload(file, chunksize=-1, resumable=True, mimetype="video/*")
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    print("📤 กำลังอัปโหลดวิดีโอ...")
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"📶 อัปโหลด: {int(status.progress() * 100)}%")

    print(f"✅ อัปโหลดเสร็จสมบูรณ์: https://www.youtube.com/watch?v={response['id']}")
    return response["id"]
