import json
import os
import time
import random

from auto_heal import is_channel_resting
from shadow_detector import check_shadow_status

STATE_FILE = "state.json"
CHANNEL_FILE = "upload_channels.json"

MIN_UPLOAD_GAP = 4 * 60 * 60   # 4 hours
MAX_UPLOAD_GAP = 5 * 60 * 60   # human random gap


# ---------------- LOAD CHANNELS ----------------
def load_channels():

    if not os.path.exists(CHANNEL_FILE):
        print("⚠ upload_channels.json not found")
        return []

    with open(CHANNEL_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        return data.get("channels", [])

    return []


# ---------------- LOAD STATE ----------------
def load_state():

    if not os.path.exists(STATE_FILE):
        return {}

    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


# ---------------- SAVE STATE ----------------
def save_state(state):

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


# ---------------- FILTER CHANNEL HEALTH ----------------
def filter_channels(channels):

    healthy = []

    for ch in channels:

        # auto heal cooldown check
        if is_channel_resting(ch):
            continue

        # shadowban detection
        if check_shadow_status(ch):
            continue

        healthy.append(ch)

    return healthy


# ---------------- SMART CHANNEL PICKER ----------------
def get_best_channel():

    channels = load_channels()

    if not channels:
        raise Exception("❌ No upload channels configured")

    channels = filter_channels(channels)

    if not channels:
        raise Exception("❌ All channels resting or shadowed")

    state = load_state()
    last_uploads = state.get("channel_last_upload", {})

    # -------- WAIT LOOP (SAFE) --------
    while True:

        now = time.time()
        eligible = []

        for ch in channels:

            last_time = last_uploads.get(ch, 0)

            required_gap = random.randint(
                MIN_UPLOAD_GAP,
                MAX_UPLOAD_GAP
            )

            if now - last_time >= required_gap:
                eligible.append(ch)

        if eligible:
            break

        # calculate minimum wait
        waits = []

        for ch in channels:
            last = last_uploads.get(ch, 0)
            waits.append((last + MIN_UPLOAD_GAP) - now)

        sleep_time = max(60, int(min(waits)))

        print(f"\n⏳ Waiting {sleep_time//60} minutes before next upload...\n")
        time.sleep(sleep_time)

    # -------- SELECT CHANNEL --------
    chosen = random.choice(eligible)

    state.setdefault("channel_last_upload", {})
    state["channel_last_upload"][chosen] = time.time()

    save_state(state)

    print(f"📡 Selected channel → {chosen}")

    return chosen