import subprocess
import sys

LOG_FILE = "detect.log"
OUTPUT_FILE = "output.mp4"


def extract_video_id():
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        line = f.readline().strip()

    parts = line.split("::")
    return parts[1]


def download_video():
    video_id = extract_video_id()

    url = f"https://www.youtube.com/watch?v={video_id}"
    print("Downloading:", url)

    # ✅ use current python executable
    python_exec = sys.executable

    command = [
        python_exec,
        "-m",
        "yt_dlp",
        "-f",
        "bv*+ba/b",
        "--merge-output-format",
        "mp4",
        "-o",
        OUTPUT_FILE,
        url,
    ]

    subprocess.run(command, check=True)


if __name__ == "__main__":
    download_video()
