import subprocess
import os

VIDEO_FILE = "videos.txt"
OUTPUT_FILE = "output.mp4"


def get_video_url():
    if not os.path.exists(VIDEO_FILE):
        print("videos.txt not found")
        return None

    with open(VIDEO_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("http"):
                return line

    return None


def download_video():

    url = get_video_url()

    if not url:
        print("No video URL found")
        return

    print("Downloading:", url)

    # ✅ IMPORTANT: use python module instead of yt-dlp exe
    command = [
        "python",
        "-m",
        "yt_dlp",
        "-f",
        "bv*+ba/b",
        "--merge-output-format",
        "mp4",
        "-o",
        OUTPUT_FILE,
        url
    ]

    subprocess.run(command, check=True)


if __name__ == "__main__":
    download_video()
