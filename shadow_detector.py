import json
import os
from auto_heal import start_cooldown

STATE_FILE = "state.json"


# ---------------- LOAD ----------------
def load_state():
    if not os.path.exists(STATE_FILE):
        return {}

    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


# ---------------- DETECT SHADOW DROP ----------------
def check_shadow_status(channel):

    state = load_state()

    stats = (
        state
        .get("upload_stats", {})
        .get(channel, {})
    )

    all_views = []

    for hour in stats:
        all_views.extend(stats[hour])

    # not enough data
    if len(all_views) < 6:
        return False

    normal_avg = sum(all_views[:-3]) / len(all_views[:-3])
    recent_avg = sum(all_views[-3:]) / 3

    print(f"📊 Normal avg: {int(normal_avg)}")
    print(f"📉 Recent avg: {int(recent_avg)}")

    shadow = recent_avg < (normal_avg * 0.4)

    # ✅ FIXED INDENTATION
    if shadow:
        start_cooldown(channel)

    state.setdefault("shadow_status", {})
    state["shadow_status"][channel] = shadow

    save_state(state)

    return shadow	