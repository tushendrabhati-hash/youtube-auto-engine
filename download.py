import subprocess
import re

LOG_FILE = "detect.log"


def get_video_id():
    """
    Reads detect.py output and extracts video id
    """
    try:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()

        for line in reversed(lines):
            if "NEW_VIDEO::" in line:
                return line.split("::")[1].strip()

    except:
        pass

    return None


def download_video(video_id):

    url = f"https://www.youtube.com/watch?v={video_id}"

    print("Downloading:", url)

    command = [
        "yt-dlp",
        "-f", "mp4",
        "-o", "output.mp4",
        url
    ]

    subprocess.run(command, check=True)


def main():

    vid = get_video_id()

    if not vid:
        print("No new video detected.")
        return

    download_video(vid)


if __name__ == "__main__":
    main()
  
