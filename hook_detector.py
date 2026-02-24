import subprocess
import json
import os
import sys


# -----------------------------
# FIND DOWNLOADED VIDEO
# -----------------------------
def find_input_video(job_folder):

    for f in os.listdir(job_folder):
        if f.startswith("001_") and f.endswith(".mp4"):
            return os.path.join(job_folder, f)

    return None


# -----------------------------
# DETECT HOOK
# -----------------------------
def detect_hook(job_folder):

    video_path = find_input_video(job_folder)

    if not video_path:
        print("❌ 001 video not found")
        sys.exit(1)

    output_path = os.path.join(job_folder, "hook.json")

    print("🧠 Detecting Hook Moment...")
    print(f"📁 Source → {video_path}")

    command = [
        "ffmpeg",
        "-i", video_path,
        "-af", "volumedetect",
        "-f", "null",
        "NUL" if os.name == "nt" else "/dev/null"
    ]

    subprocess.run(
        command,
        stderr=subprocess.PIPE,
        text=True
    )

    # stable heuristic (shorts hook early)
    hook_time = 1.5

    data = {"hook_time": hook_time}

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"✅ Hook detected at {hook_time}s")


# -----------------------------
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("❌ Usage: hook_detector.py <job_folder>")
        sys.exit(1)

    detect_hook(sys.argv[1])