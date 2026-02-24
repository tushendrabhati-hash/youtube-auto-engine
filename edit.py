import subprocess
import json
import os
import sys


# -----------------------------
# FIND INPUT VIDEO
# -----------------------------
def find_input_video(job_folder):

    for f in os.listdir(job_folder):
        if f.startswith("001_") and f.endswith(".mp4"):
            return os.path.join(job_folder, f)

    print("❌ No input video found in job folder")
    return None


# -----------------------------
# LOAD HOOK TIME (JOB LOCAL)
# -----------------------------
def load_hook_time(job_folder):

    hook_file = os.path.join(job_folder, "hook.json")

    if not os.path.exists(hook_file):
        return 1.5

    try:
        with open(hook_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("hook_time", 1.5)
    except:
        return 1.5


# -----------------------------
# EDIT VIDEO
# -----------------------------
def edit_video(job_folder):

    INPUT = find_input_video(job_folder)

    if not INPUT:
        sys.exit(1)

    OUTPUT = os.path.join(job_folder, "002_edit.mp4")

    hook_time = load_hook_time(job_folder)

    print(f"🔥 Editing → {INPUT}")
    print(f"📁 Output → {OUTPUT}")

    filter_complex = (
        "[0:v]"
        "scale=1080:-2,"
        "crop=1080:1920,"
        "eq=contrast=1.06:saturation=1.15:brightness=0.02,"
        f"drawtext=text='DON''T BLINK':"
        "fontcolor=white:"
        "fontsize=72:"
        "x=(w-text_w)/2:"
        "y=h-250:"
        "box=1:"
        "boxcolor=black@0.55:"
        "boxborderw=25:"
        f"enable='gte(t,{hook_time})'"
        "[v];"
        "[0:a]"
        "volume=1.15,"
        "acompressor=threshold=-18dB:ratio=2"
        "[a]"
    )

    command = [
        "ffmpeg",
        "-y",
        "-i", INPUT,
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-map", "[a]",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "27",
        "-c:a", "aac",
        "-b:a", "128k",
        "-movflags", "+faststart",
        OUTPUT
    ]

    subprocess.run(command, check=True)

    print("✅ Edit Complete")


# -----------------------------
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("❌ Usage: edit.py <job_folder>")
        sys.exit(1)

    job_folder = sys.argv[1]

    edit_video(job_folder)