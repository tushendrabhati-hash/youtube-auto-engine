import subprocess
import sys
import os

# ✅ Windows UTF-8 safety
sys.stdout.reconfigure(encoding="utf-8")


# -----------------------------
# EXTRACT VIDEO ID
# -----------------------------
def extract_video_id(url):

    if "v=" in url:
        return url.split("v=")[-1].split("&")[0]

    if "youtu.be/" in url:
        return url.split("youtu.be/")[-1].split("?")[0]

    if "/shorts/" in url:
        return url.split("/shorts/")[-1].split("?")[0]

    return "video"


# -----------------------------
# DOWNLOAD VIDEO INTO JOB
# -----------------------------
def download_video(url, job_folder):

    os.makedirs(job_folder, exist_ok=True)

    vid = extract_video_id(url)

    # ordered filename
    output_template = os.path.join(
        job_folder,
        f"001_{vid}.%(ext)s"
    )

    print(f"\n⬇ DOWNLOAD → {vid}")
    print(f"📁 Folder → {job_folder}\n")

    command = [
        sys.executable,
        "-m",
        "yt_dlp",
        "-f",
        "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
        "--merge-output-format", "mp4",
        "--no-playlist",
        "--print", "after_move:filename",
        "-o",
        output_template,
        url
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True
        )
    except subprocess.CalledProcessError as e:
        print("❌ yt-dlp failed:")
        print(e.stderr)
        sys.exit(1)

    # yt-dlp returns final filename
    filename = result.stdout.strip().splitlines()[-1]

    if not os.path.exists(filename):
        print("❌ Download finished but file missing")
        sys.exit(1)

    print(f"✅ Download Complete → {filename}")

    # IMPORTANT: queue_manager reads this
    print(filename)


# -----------------------------
if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("❌ Usage: download.py <url> <job_folder>")
        sys.exit(1)

    url = sys.argv[1]
    job_folder = sys.argv[2]

    download_video(url, job_folder)