import json
import random

def get_random_channel():
    with open("upload_channels.json", "r") as f:
        channels = json.load(f)

    return random.choice(channels)
