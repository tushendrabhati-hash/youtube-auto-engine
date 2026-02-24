import json
import os
import time

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

from auto_recovery import safe_run

STATE_FILE = "state.json"
TOKEN_DIR = "tokens"

SCOPES = [
    "https://www.googleapis.com/auth/youtube.readonly"
]

MAX_SAMPLES_PER_HOUR = 20


# ---------- STATE ----------
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


# ---------- YOUTUBE CLIENT ----------
def get_youtube(channel):

    token = f"{TOKEN_DIR}/{channel}.json"

    creds = Credentials.from_authorized_user_file(
        token,
        SCOPES
    )

    # ✅ AUTO TOKEN REFRESH
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())

        with open(token, "w") as f:
            f.write(creds.to_json())

    return build("youtube", "v3", credentials=creds)


# ---------- ADD JOB ----------
def schedule_analytics(channel, video_id):

    state = load_state()

    state.setdefault("pending_analytics", [])

    # ✅ prevent duplicate jobs
    for job in state["pending_analytics"]:
        if job["video_id"] == video_id:
            return

    state["pending_analytics"].append({
        "channel": channel,
        "video_id": video_id,
        "check_after": int(time.time()) + (3 * 60 * 60)
    })

    save_state(state)

    print("📊 Analytics check scheduled")


# ---------- FETCH VIEWS ----------
def fetch_views(channel, video_id):

    yt = get_youtube(channel)

    def api_call():
        return yt.videos().list(
            part="statistics",
            id=video_id
        ).execute()

    res = safe_run("analytics_fetch", api_call)

    items = res.get("items", [])

    if not items:
        return 0

    return int(items[0]["statistics"].get("viewCount", 0))


# ---------- PROCESS JOBS ----------
def run_pending_checks():

    state = load_state()

    jobs = state.get("pending_analytics", [])

    if not jobs:
        return

    remaining = []
    now = int(time.time())

    for job in jobs:

        if now < job["check_after"]:
            remaining.append(job)
            continue

        channel = job["channel"]
        video_id = job["video_id"]

        try:
            views = fetch_views(channel, video_id)

            print(f"📈 Views ({video_id}) → {views}")

            hour = str(int(time.strftime("%H")))

            state.setdefault("upload_stats", {})
            state["upload_stats"].setdefault(channel, {})
            state["upload_stats"][channel].setdefault(hour, [])

            bucket = state["upload_stats"][channel][hour]

            bucket.append(views)

            # ✅ prevent infinite growth
            if len(bucket) > MAX_SAMPLES_PER_HOUR:
                bucket.pop(0)

        except Exception as e:
            print("Analytics fetch failed:", e)
            remaining.append(job)

    state["pending_analytics"] = remaining

    save_state(state)