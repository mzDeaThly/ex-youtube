import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service(client_secret_path="client_secret.json"):
    creds = None
    token_path = "token.pickle"
    if os.path.exists(token_path):
        with open(token_path, "rb") as token_file:
            creds = pickle.load(token_file)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secret_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, "wb") as token_file:
            pickle.dump(creds, token_file)
    return build("youtube", "v3", credentials=creds)

def upload_video(file, title, description, tags=None, categoryId="27", privacyStatus="public", client_secret_path="client_secret.json"):
    """
    อัปโหลดวิดีโอขึ้น YouTube
    """
    youtube = get_authenticated_service(client_secret_path)

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

    from googleapiclient.http import MediaFileUpload
    media_body = MediaFileUpload(file, chunksize=-1, resumable=True, mimetype="video/*")

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media_body
    )

    response = None
    try:
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"⏳ อัปโหลดไปแล้ว {int(status.progress() * 100)}%")
        print(f"✅ อัปโหลดสำเร็จ: https://youtu.be/{response['id']}")
        return response
    except Exception as e:
        print(f"❌ อัปโหลดล้มเหลว: {e}")
        return None
