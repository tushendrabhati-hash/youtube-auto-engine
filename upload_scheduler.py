import json
import os
import time
import random

STATE_FILE = "state.json"
CHANNEL_FILE = "upload_channels.json"

# 4–5 hour gap (human behavior)
MIN_GAP = 4 * 60 * 60
MAX_GAP = 5 * 60 * 60


# ---------------- JSON HELPERS ----------------
def load_json(path, default):
    if not os.path.exists(path):
        return default

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# ---------------- CHANNEL LIST ----------------
def load_channels():

    data = load_json(CHANNEL_FILE, {"channels": []})

    # support list OR dict format
    if isinstance(data, list):
        return data

    return data.get("channels", [])


# ---------------- MAIN SCHEDULER ----------------
def get_next_channel():

    state = load_json(STATE_FILE, {})
    channels = load_channels()

    if not channels:
        raise Exception("No upload channels found")

    now = time.time()
    last_uploads = state.get("channel_last_upload", {})

    eligible = []

    for ch in channels:
        last = last_uploads.get(ch, 0)
        gap = random.randint(MIN_GAP, MAX_GAP)

        if now - last >= gap:
            eligible.append(ch)

    # NONE READY → WAIT
    if not eligible:

        waits = []

        for ch in channels:
            last = last_uploads.get(ch, 0)
            waits.append((last + MIN_GAP) - now)

        sleep_time = max(60, int(min(waits)))

        print(f"\n⏳ Waiting {sleep_time//60} minutes before next upload...\n")
        time.sleep(sleep_time)

        return get_next_channel()

    chosen = random.choice(eligible)

    # SAVE TIME
    state.setdefault("channel_last_upload", {})
    state["channel_last_upload"][chosen] = now

    save_json(STATE_FILE, state)

    return chosen