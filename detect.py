import feedparser
import json
import os

# ===== SOURCE CHANNELS =====
SOURCE_CHANNELS = [
    "UCFLrwzF6qPrj3J3G5c9bmmA",
    "UCVLWtYLZKAdcInt3xXw4oVA",
    "UCZi87CfJkSMaRGBV73od5Vg",
    "UCGu2HSFJf1ZwPgwvOVmVNSQ",
    "UCp-AoFVXhWtJbfjKi7mi8Hw",
    "UCkaIQsmRkSHWJbJbJ0wh9piDw"
]

# ===== YOUR TARGET CHANNELS =====
TARGET_CHANNELS = [
    "CharsiShorts1",
    "ReactBites",
    "Viral_content_reacts",
    "YummyVibes_Only"
]

STATE_FILE = "state.json"


# ---------- STATE ----------
def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"videos": {}, "rotation": 0}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


# ---------- ROTATION ----------
def get_next_channel(state):
    index = state["rotation"] % len(TARGET_CHANNELS)
    channel = TARGET_CHANNELS[index]
    state["rotation"] += 1
    return channel


# ---------- DETECTION ----------
def check_channel(channel_id, state):

    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    feed = feedparser.parse(url)

    latest = feed.entries[0]
    video_id = latest.yt_videoid

    if state["videos"].get(channel_id) == video_id:
        return None

    state["videos"][channel_id] = video_id

    upload_channel = get_next_channel(state)

    print(
        f"NEW_VIDEO::{video_id}::UPLOAD_TO::{upload_channel}"
    )

    return video_id


# ---------- MAIN ----------
def main():

    state = load_state()

    for ch in SOURCE_CHANNELS:
        check_channel(ch, state)

    save_state(state)


if __name__ == "__main__":
    main()
    
with open("detect.log", "a") as f:
    f.write("RUN COMPLETE\n")
