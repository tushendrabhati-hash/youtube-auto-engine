import subprocess
import os

INPUT = "output.mp4"
OUTPUT = "final.mp4"


def edit_video():

    if not os.path.exists(INPUT):
        print("No video to edit.")
        return

    print("Editing video...")

    command = [
        "ffmpeg",
        "-i", INPUT,
        "-filter_complex",
        "setpts=0.97*PTS,scale=1080:1920,drawtext=text='🔥 Watch till end':fontcolor=white:fontsize=60:x=(w-text_w)/2:y=h-200",
        "-an",
        OUTPUT
    ]

    subprocess.run(command, check=True)


if __name__ == "__main__":
    edit_video()
