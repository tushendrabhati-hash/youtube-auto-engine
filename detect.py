import requests
import os
import subprocess
import json
import xml.etree.ElementTree as ET

CHANNEL_FILE = "source_channels.json"
VIDEO_FILE = "videos.txt"

# ⭐ IMPORTANT SAFETY
# detect only latest uploads per channel
LATEST_CHECK_LIMIT = 2


# -----------------------------
# LOAD CHANNEL IDS
# -----------------------------
def load_channels():

    if not os.path.exists(CHANNEL_FILE):
        print("❌ source_channels.json not found")
        return []

    with open(CHANNEL_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data.get("channels", [])


# -----------------------------
# LOAD EXISTING IDS
# -----------------------------
def existing_ids():

    ids = set()

    if not os.path.exists(VIDEO_FILE):
        return ids

    with open(VIDEO_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if "NEW_VIDEO::" in line:
                ids.add(line.strip().split("::")[1])

    return ids


# -----------------------------
# FALLBACK SHORT CHECK
# -----------------------------
def is_short(video_id):

    try:
        cmd = [
            "yt-dlp",
            "--dump-json",
            "--skip-download",
            f"https://www.youtube.com/watch?v={video_id}"
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=12
        )

        if result.returncode != 0:
            return False

        data = json.loads(result.stdout)
        duration = data.get("duration", 0)

        return duration and duration <= 60

    except:
        return False


# -----------------------------
# FETCH CHANNEL RSS
# -----------------------------
def fetch_channel(channel_id):

    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"

    r = requests.get(url, timeout=10)

    if r.status_code != 200:
        return []

    root = ET.fromstring(r.text)

    videos = []

    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):

        video_id = entry.find(
            "{http://www.youtube.com/xml/schemas/2015}videoId"
        ).text

        link_elem = entry.find("{http://www.w3.org/2005/Atom}link")
        link = link_elem.attrib.get("href")

        videos.append({
            "id": video_id,
            "link": link
        })

    return videos


# -----------------------------
# MAIN DETECT
# -----------------------------
def detect():

    print("\n🚀 DETECT START")

    channels = load_channels()
    seen = existing_ids()

    new_count = 0

    for ch in channels:

        print(f"🔎 Checking channel → {ch}")

        try:
            videos = fetch_channel(ch)
        except Exception as e:
            print("⚠ Fetch failed:", e)
            continue

        # ⭐ FLOOD PROTECTION
        videos = videos[:LATEST_CHECK_LIMIT]

        for v in videos:

            vid = v["id"]
            link = v["link"]

            if vid in seen:
                continue

            # FAST SHORT CHECK
            if "/shorts/" in link:
                valid_short = True
            else:
                valid_short = is_short(vid)

            if not valid_short:
                continue

            with open(VIDEO_FILE, "a", encoding="utf-8") as f:
                f.write(f"NEW_VIDEO::{vid}\n")

            print(f"✅ NEW SHORT FOUND → {link}")

            seen.add(vid)
            new_count += 1

    if new_count == 0:
        print("No new Shorts found")

    print("✅ DETECT COMPLETE\n")


# -----------------------------
if __name__ == "__main__":
    detect()