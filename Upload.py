import os
import random
import json

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

from channel_picker import get_random_channel

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

VIDEO_FILE = "output.mp4"
TOKEN_PATH = "tokens/token.json"
CLIENT_SECRET = "client_secret.json"


# =============================
# AUTH SYSTEM (PERMANENT LOGIN)
# =============================
def authenticate():

    creds = None

    # load saved token
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(
            TOKEN_PATH, SCOPES
        )

    # refresh or login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET, SCOPES
            )
            creds = flow.run_local_server(port=0)

        # save token
        os.makedirs("tokens", exist_ok=True)
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())

    return build("youtube", "v3", credentials=creds)


# =============================
# METADATA GENERATOR
# =============================
def generate_metadata():

    titles = [
        "🔥 Viral Shorts You Must Watch",
        "😱 This Clip Is Blowing Up",
        "🚀 Trending Short Right Now",
        "💥 Internet Can't Stop Watching",
    ]

    descriptions = [
        "Subscribe for daily viral shorts!",
        "More content coming daily 🚀",
        "Stay tuned for viral moments.",
    ]

    return {
        "title": random.choice(titles),
        "description": random.choice(descriptions),
        "tags": ["shorts", "viral", "trending"],
    }


# =============================
# UPLOAD ENGINE
# =============================
def upload_video():

    if not os.path.exists(VIDEO_FILE):
        print("❌ output.mp4 not found")
        return

    youtube = authenticate()

    meta = generate_metadata()
    channel_name = get_random_channel()

    body = {
        "snippet": {
            "title": meta["title"],
            "description": meta["description"],
            "tags": meta["tags"],
            "categoryId": "22"
        },
        "status": {
            "privacyStatus": "public"
        }
    }

    media = MediaFileUpload(
        VIDEO_FILE,
        chunksize=-1,
        resumable=True
    )

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = request.execute()

    print("\n✅ UPLOAD SUCCESS")
    print("Video ID:", response["id"])
    print("Channel:", channel_name)


# =============================
if __name__ == "__main__":
    upload_video()
