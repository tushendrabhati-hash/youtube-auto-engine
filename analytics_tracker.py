import json
import os
import time

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

from auto_recovery import safe_run

TOKEN_DIR = "tokens"
STATE_FILE = "state.json"

SCOPES = [
    "https://www.googleapis.com/auth/youtube.readonly"
]

MAX_SAMPLES_PER_HOUR = 20


# ---------------- LOAD STATE ----------------
def load_state():

    if not os.path.exists(STATE_FILE):
        return {}

    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_state(state):

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


# ---------------- GET CLIENT ----------------
def get_youtube(channel):

    token_path = f"{TOKEN_DIR}/{channel}.json"

    creds = Credentials.from_authorized_user_file(
        token_path,
        SCOPES
    )

    # ✅ auto refresh token
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())

        with open(token_path, "w") as f:
            f.write(creds.to_json())

    return build("youtube", "v3", credentials=creds)


# ---------------- FETCH VIEWS ----------------
def fetch_views(channel, video_id):

    youtube = get_youtube(channel)

    def api_call():
        return youtube.videos().list(
            part="statistics",
            id=video_id
        ).execute()

    response = safe_run("analytics_fetch", api_call)

    items = response.get("items", [])

    if not items:
        return 0

    return int(items[0]["statistics"].get("viewCount", 0))


# ---------------- RECORD PERFORMANCE ----------------
# ⚠ NO SLEEP HERE (scheduler handles timing)
def record_performance(channel, video_id):

    views = fetch_views(channel, video_id)

    print(f"📈 Views collected → {views}")

    state = load_state()

    hour = str(int(time.strftime("%H")))

    state.setdefault("upload_stats", {})
    state["upload_stats"].setdefault(channel, {})
    state["upload_stats"][channel].setdefault(hour, [])

    bucket = state["upload_stats"][channel][hour]

    bucket.append(views)

    # prevent infinite growth
    if len(bucket) > MAX_SAMPLES_PER_HOUR:
        bucket.pop(0)

    save_state(state)

    print("🧠 Upload intelligence updated")