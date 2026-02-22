import json
import random

def get_random_channel():
    with open("channels.json") as f:
        data = json.load(f)

    return random.choice(data["channels"])
