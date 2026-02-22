import os
import random
from datetime import datetime

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from channel_picker import get_random_channel

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

VIDEO_FILE = "output.mp4"

def authenticate():
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secret.json", SCOPES
    )
    creds = flow.run_local_server(port=0)
    return build("youtube", "v3", credentials=creds)


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


def upload_video():
    if not os.path.exists(VIDEO_FILE):
        print("❌ output.mp4 not found")
        return

    youtube = authenticate()

    meta = generate_metadata()
    channel_id = get_random_channel()

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

    print("✅ Uploaded Successfully")
    print("Video ID:", response["id"])
    print("Channel:", channel_id)


if __name__ == "__main__":
    upload_video()
