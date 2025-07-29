import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# ขอบเขตการเข้าถึง YouTube API สำหรับอัปโหลดวิดีโอ
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token_file:
            creds = pickle.load(token_file)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token_file:
            pickle.dump(creds, token_file)
    return build("youtube", "v3", credentials=creds)

def upload_video(file, title, description, tags=None, categoryId="27", privacyStatus="public"):
    """
    อัปโหลดวิดีโอขึ้น YouTube
    categoryId 27 = Education
    privacyStatus: public, private, unlisted
    """
    youtube = get_authenticated_service()

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags or [],
            "categoryId": categoryId,
        },
        "status": {
            "privacyStatus": privacyStatus,
        }
    }

    # เตรียมไฟล์วิดีโอ
    media_body = None
    try:
        from googleapiclient.http import MediaFileUpload
        media_body = MediaFileUpload(file, chunksize=-1, resumable=True, mimetype="video/*")
    except ImportError as e:
        print("❌ ต้องติดตั้ง google-api-python-client และ google-auth")

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media_body
    )

    response = None
    try:
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"⏳ อัปโหลดไปแล้ว {int(status.progress() * 100)}%")
        print(f"✅ อัปโหลดสำเร็จ: https://youtu.be/{response['id']}")
        return response
    except Exception as e:
        print(f"❌ อัปโหลดล้มเหลว: {e}")
        return None
