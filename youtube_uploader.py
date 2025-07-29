import os
import pickle
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
CLIENT_SECRET_FILE = os.environ.get('CLIENT_SECRET_FILE', 'client_secret.json')
TOKEN_PICKLE = "token.pickle"

def get_authenticated_service():
    creds = None
    # โหลด token.pickle ถ้ามี
    if os.path.exists(TOKEN_PICKLE):
        with open(TOKEN_PICKLE, "rb") as token:
            creds = pickle.load(token)
    # ถ้า token ไม่ถูกต้องหรือไม่มี ให้ล็อกอินใหม่
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_console()
        # บันทึก token ใหม่
        with open(TOKEN_PICKLE, "wb") as token:
            pickle.dump(creds, token)

    return googleapiclient.discovery.build("youtube", "v3", credentials=creds)

def upload_video(file, title, description="", tags=None, categoryId="22", privacyStatus="public"):
    """
    อัปโหลดวิดีโอขึ้น YouTube
    :param file: path ไฟล์วิดีโอ (mp4)
    :param title: ชื่อวิดีโอ
    :param description: คำอธิบายวิดีโอ
    :param tags: list ของ tags (เช่น ["ข่าว", "AI"])
    :param categoryId: รหัสหมวดหมู่ YouTube (22 = People & Blogs)
    :param privacyStatus: "public", "private", หรือ "unlisted"
    """
    youtube = get_authenticated_service()

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags or [],
            "categoryId": categoryId
        },
        "status": {
            "privacyStatus": privacyStatus
        }
    }

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=file
    )

    print(f"⬆️ กำลังอัปโหลดวิดีโอ: {file} ...")
    response = request.execute()
    print("✅ อัปโหลดสำเร็จ!")
    print(f"URL: https://www.youtube.com/watch?v={response['id']}")

    return response['id']

if __name__ == "__main__":
    # ทดสอบอัปโหลดไฟล์ตัวอย่าง (แก้ path เป็นไฟล์ของคุณ)
    upload_video(
        file="final_video.mp4",
        title="ทดสอบอัปโหลดวิดีโอ AI News",
        description="ทดสอบอัปโหลดวิดีโอด้วย YouTube API",
        tags=["ข่าว", "AI", "ทดสอบ"],
        privacyStatus="private"
    )
