import json
import os
import random

OUTPUT_FILE = "metadata.json"

TITLES = [
    "🔥 You Won't Believe This Moment!",
    "😱 Watch Till The End!",
    "💥 Internet Is Shocked By This!",
    "🔥 Most Viral Clip Today!",
    "😲 This Changed Everything!"
]

DESCRIPTIONS = [
    "Watch this insane moment that everyone is talking about!",
    "This viral clip is trending everywhere right now.",
    "Stay till the end for the unexpected twist!",
    "One of the most viral moments on the internet.",
]

HASHTAGS = [
    "#shorts #viral #trending",
    "#shortvideo #viralvideo #explore",
    "#ytshorts #fyp #viralshorts"
]


def generate_metadata():

    data = {
        "title": random.choice(TITLES),
        "description": random.choice(DESCRIPTIONS) + "\n\n" + random.choice(HASHTAGS)
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f)

    print("Metadata generated.")


if __name__ == "__main__":
    generate_metadata()
