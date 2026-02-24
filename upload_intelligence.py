import json
import os
import random
import time

STATE_FILE = "state.json"

MAX_SAMPLES_PER_HOUR = 20


# ---------------- LOAD ----------------
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


# ---------------- RECORD PERFORMANCE ----------------
def record_upload(channel, score=None):

    state = load_state()

    hour = int(time.strftime("%H"))

    state.setdefault("upload_stats", {})
    state["upload_stats"].setdefault(channel, {})
    state["upload_stats"][channel].setdefault(str(hour), [])

    # fallback synthetic score (until analytics updates real value)
    if score is None:
        score = random.randint(1500, 3000)

    bucket = state["upload_stats"][channel][str(hour)]

    bucket.append(score)

    # ✅ prevent infinite growth
    if len(bucket) > MAX_SAMPLES_PER_HOUR:
        bucket.pop(0)

    save_state(state)


# ---------------- PICK BEST HOUR ----------------
def get_best_hour(channel):

    state = load_state()

    stats = state.get("upload_stats", {}).get(channel, {})

    # fallback schedule
    if not stats:
        return random.choice([6, 18, 23])

    avg_scores = {}

    for hour, values in stats.items():

        if not values:
            continue

        # recent-weight average
        avg_scores[int(hour)] = sum(values) / len(values)

    if not avg_scores:
        return random.choice([6, 18, 23])

    best = max(avg_scores, key=avg_scores.get)

    return best