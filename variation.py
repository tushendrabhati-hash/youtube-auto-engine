import subprocess
import random
import os

INPUT = "output.mp4"

VARIATIONS = [
    ("final1.mp4", "0.96", "🔥 Wait For It"),
    ("final2.mp4", "0.98", "😱 Unbelievable"),
    ("final3.mp4", "1.02", "💥 Viral Moment"),
    ("final4.mp4", "1.04", "⚡ Must Watch")
]


def create_variation(output, speed, text):

    if not os.path.exists(INPUT):
        print("No input video.")
        return

    print("Creating variation:", output)

    cmd = [
        "ffmpeg",
        "-y",
        "-i", INPUT,
        "-filter_complex",
        f"setpts={speed}*PTS,"
        f"scale=1080:1920,"
        f"drawtext=text='{text}':fontcolor=white:"
        f"fontsize=60:x=(w-text_w)/2:y=h-150",
        output
    ]

    subprocess.run(cmd, check=True)


def main():

    for v in VARIATIONS:
        create_variation(*v)

    print("All variations created.")


if __name__ == "__main__":
    main()
