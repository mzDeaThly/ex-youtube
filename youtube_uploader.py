import os
import pickle
import google.auth.transport.requests
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
CLIENT_SECRETS_FILE = "client_secret.json"
TOKEN_FILE = "token.json"

def get_authenticated_service():
    credentials = None

    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            credentials = pickle.load(token)

    # หากยังไม่มี token หรือหมดอายุ
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(google.auth.transport.requests.Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            credentials = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(credentials, token)

    return build("youtube", "v3", credentials=credentials)

def upload_video(file, title, description, tags=None, categoryId="25", privacyStatus="public"):
    """อัปโหลดวิดีโอไปยัง YouTube"""
    youtube = get_authenticated_service()

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags or [],
            "categoryId": categoryId
        },
        "status": {
            "privacyStatus": privacyStatus,
        }
    }

    media = MediaFileUpload(file, chunksize=-1, resumable=True, mimetype="video/*")
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    print("📤 กำลังอัปโหลดวิดีโอไปยัง YouTube...")
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"⬆️ ความคืบหน้า: {int(status.progress() * 100)}%")

    print(f"✅ อัปโหลดสำเร็จ: https://www.youtube.com/watch?v={response['id']}")
    return response["id"]
