import json
import os
import time

STATE_FILE = "state.json"

COOLDOWN_HOURS = 48


# ---------- LOAD ----------
def load_state():

    if not os.path.exists(STATE_FILE):
        return {}

    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


# ---------- SAVE ----------
def save_state(state):

    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


# ---------- START COOLDOWN ----------
def start_cooldown(channel):

    state = load_state()

    state.setdefault("cooldowns", {})

    now = int(time.time())

    state["cooldowns"][channel] = {
        "start": now,
        "end": now + (COOLDOWN_HOURS * 3600)
    }

    save_state(state)

    print(f"🧊 Cooldown started → {channel}")


# ---------- CHECK COOLDOWN ----------
def is_channel_resting(channel):

    state = load_state()

    cooldowns = state.setdefault("cooldowns", {})

    data = cooldowns.get(channel)

    if not data:
        return False

    end_time = data.get("end")

    if not end_time:
        # corrupted entry remove
        cooldowns.pop(channel, None)
        save_state(state)
        return False

    now = int(time.time())

    # cooldown finished
    if now >= end_time:
        print(f"✅ Cooldown finished → {channel}")
        cooldowns.pop(channel, None)
        save_state(state)
        return False

    remaining = int((end_time - now) / 3600)

    print(f"⏸ Channel resting ({remaining}h left) → {channel}")

    return True