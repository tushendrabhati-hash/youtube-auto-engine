import os
import random

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

from channel_picker import get_random_channel

# =========================
# CONFIG
# =========================

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
VIDEO_FILE = "output.mp4"
CLIENT_SECRET = "client_secret.json"
TOKEN_FOLDER = "tokens"

# =========================
# AUTHENTICATION
# =========================

def authenticate(channel_name):

    os.makedirs(TOKEN_FOLDER, exist_ok=True)

    token_file = f"{TOKEN_FOLDER}/token_{channel_name}.json"

    creds = None

    # Load saved token
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(
            token_file, SCOPES
        )

    # If no token → login required
    if not creds or not creds.valid:

        flow = InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRET,
            SCOPES
        )

        creds = flow.run_local_server(port=0)

        # Save token
        with open(token_file, "w") as token:
            token.write(creds.to_json())

    youtube = build("youtube", "v3", credentials=creds)

    return youtube


# =========================
# METADATA GENERATOR
# =========================

def generate_metadata():

    titles = [
        "🔥 Viral Shorts You Must Watch",
        "😱 This Clip Is Blowing Up",
        "🚀 Trending Short Right Now",
        "💥 Internet Can't Stop Watching",
        "⚡ This Short Is Everywhere",
    ]

    descriptions = [
        "Subscribe for daily viral shorts!",
        "More content coming daily 🚀",
        "Stay tuned for viral moments.",
        "Daily trending content 🔥",
    ]

    return {
        "title": random.choice(titles),
        "description": random.choice(descriptions),
        "tags": ["shorts", "viral", "trending", "reels"],
    }


# =========================
# UPLOAD VIDEO
# =========================

def upload_video():

    if not os.path.exists(VIDEO_FILE):
        print("❌ output.mp4 not found")
        return

    # pick random channel
    channel_name = get_random_channel()
    print(f"🎯 Selected Channel: {channel_name}")

    youtube = authenticate(channel_name)

    meta = generate_metadata()

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

    print("⬆ Uploading video...")

    response = request.execute()

    print("✅ Uploaded Successfully!")
    print("📺 Video ID:", response["id"])
    print("📡 Channel:", channel_name)


# =========================
# RUN
# =========================

if __name__ == "__main__":
    upload_video()
