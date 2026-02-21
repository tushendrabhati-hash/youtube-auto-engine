import subprocess

LOG_FILE = "detect.log"
OUTPUT = "output.mp4"


def extract_video_id():

    with open(LOG_FILE) as f:
        lines = f.readlines()

    for line in lines:
        if "NEW_VIDEO::" in line:
            parts = line.strip().split("::")
            return parts[1]

    raise Exception("No video found")


def download_video():

    video_id = extract_video_id()
    url = f"https://www.youtube.com/watch?v={video_id}"

    print("Downloading:", url)

    command = [
        "yt-dlp",
        "--cookies", "cookies.txt",
        "-f", "bv*+ba/b",
        "--merge-output-format", "mp4",
        "-o", OUTPUT,
        url
    ]

    subprocess.run(command, check=True)


if __name__ == "__main__":
    download_video()
