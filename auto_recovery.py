import time
import json
import os
import random

STATE_FILE = "state.json"

MAX_RETRIES = 5


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

    temp_file = STATE_FILE + ".tmp"

    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

    # ✅ atomic replace (prevents corruption)
    os.replace(temp_file, STATE_FILE)


# ---------- SAFE EXECUTOR ----------
def safe_run(step_name, func, *args, **kwargs):

    while True:

        state = load_state()
        state.setdefault("retries", {})

        retries = state["retries"].get(step_name, 0)

        if retries >= MAX_RETRIES:
            raise Exception(
                f"{step_name} failed after {MAX_RETRIES} retries"
            )

        try:
            print(f"▶ Running {step_name} (try {retries + 1})")

            result = func(*args, **kwargs)

            # reset retry count
            state["retries"][step_name] = 0
            save_state(state)

            return result

        # except Exception as e:

        #     retries += 1
        #     state["retries"][step_name] = retries
        #     save_state(state)

        #     # exponential + jitter
        #     wait = min(600, retries * 60)
        #     wait += random.randint(5, 25)

        #     print(f"⚠ {step_name} failed:", str(e)[:120])
        #     print(f"⏳ retrying in {wait} seconds...\n")

        #     time.sleep(wait)

        except Exception as e:

            import traceback

            retries += 1
            state["retries"][step_name] = retries
            save_state(state)

            print(f"\n❌ {step_name} FAILED — FULL ERROR:\n")
            traceback.print_exc()

            # exponential + jitter
            wait = min(600, retries * 60)
            wait += random.randint(5, 25)

            print(f"\n⏳ retrying in {wait} seconds...\n")

            time.sleep(wait)