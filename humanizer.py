import time
import random


# ---------------- HUMAN DELAY ----------------
def human_delay(min_s=5, max_s=25):

    delay = random.uniform(min_s, max_s)

    print(f"🧍 Human pause {round(delay,1)}s")
    time.sleep(delay)


# ---------------- THINK TIME ----------------
def thinking_pause():

    delay = random.uniform(30, 120)

    print(f"🤔 Thinking pause {int(delay)}s")
    time.sleep(delay)


# ---------------- SESSION BREAK ----------------
def session_break():

    delay = random.uniform(5*60, 15*60)

    print(f"☕ Session break {int(delay/60)} min")
    time.sleep(delay)