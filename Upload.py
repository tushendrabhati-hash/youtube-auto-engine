import os
import json
import random
import sys

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

from humanizer import human_delay, thinking_pause
from smart_channel_picker import get_best_channel


# =============================
# CONFIG
# =============================
SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly"
]

TOKEN_DIR = "tokens"
CLIENT_SECRET = "client_secret.json"


# =============================
# JOB INPUT
# =============================
if len(sys.argv) < 2:
    raise Exception("Usage: Upload.py <job_folder>")

JOB_FOLDER = sys.argv[1]

VIDEO_FILE = os.path.join(JOB_FOLDER, "002_edit.mp4")
META_FILE = os.path.join(JOB_FOLDER, "metadata.json")
THUMB_FILE = os.path.join(JOB_FOLDER, "thumbnail.jpg")

if not os.path.exists(VIDEO_FILE):
    raise FileNotFoundError("002_edit.mp4 not found in job folder")


# =============================
# AUTH
# =============================
def authenticate(channel_name):

    token_path = f"{TOKEN_DIR}/{channel_name}.json"
    creds = None

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(
            token_path,
            SCOPES
        )

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(token_path, "w") as token:
            token.write(creds.to_json())

    if not creds or not creds.valid:

        flow = InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRET,
            SCOPES
        )

        creds = flow.run_local_server(port=0)

        os.makedirs(TOKEN_DIR, exist_ok=True)

        with open(token_path, "w") as token:
            token.write(creds.to_json())

        print(f"✅ Token saved for {channel_name}")

    return build("youtube", "v3", credentials=creds)


# =============================
# FALLBACK METADATA
# =============================
def fallback_metadata():

    return {
        "title": "🔥 Viral Shorts You Must Watch",
        "description": "Subscribe for daily viral shorts!",
        "tags": ["shorts", "viral", "trending"]
    }


def load_metadata():

    if not os.path.exists(META_FILE):
        print("⚠ metadata.json missing → fallback")
        return fallback_metadata()

    try:
        with open(META_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return fallback_metadata()


# =============================
# UPLOAD
# =============================
def upload_video():

    # authenticate FIRST (fast failure)
    channel_name = get_best_channel()
    youtube = authenticate(channel_name)

    print(f"🚀 Uploading → {channel_name}")

    thinking_pause()
    human_delay(8, 20)

    meta = load_metadata()

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
        chunksize=8 * 1024 * 1024,
        resumable=True
    )

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    # IMPORTANT: do NOT wrap with safe_run
    response = request.execute()

    print("✅ Uploaded Successfully")
    print("Video ID:", response["id"])

    # ---------- ANALYTICS ----------
    from analytics_scheduler import schedule_analytics
    schedule_analytics(channel_name, response["id"])

    from analytics_tracker import record_performance
    record_performance(channel_name, response["id"])

    from upload_intelligence import record_upload
    record_upload(channel_name)

    # ---------- THUMBNAIL ----------
    if os.path.exists(THUMB_FILE):

        youtube.thumbnails().set(
            videoId=response["id"],
            media_body=THUMB_FILE
        ).execute()

        print("🖼 Thumbnail Uploaded Successfully")

    else:
        print("⚠ Thumbnail not found — skipped")


# =============================
if __name__ == "__main__":
    upload_video()