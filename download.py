import subprocess
import os

VIDEO_URL_FILE = "detect.log"
OUTPUT = "output.mp4"


def get_video_url():
    with open(VIDEO_URL_FILE) as f:
        return f.read().strip()


def download_video():

    url = get_video_url()

    command = [
        "yt-dlp",
        "--cookies", "cookies.txt",
        "-f", "mp4",
        "-o", OUTPUT,
        url
    ]

    subprocess.run(command, check=True)


if __name__ == "__main__":
    download_video()
