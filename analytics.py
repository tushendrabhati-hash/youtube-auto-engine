import json
import os
import random

LEARNING_DB = "learning.json"


def load_db():
    if os.path.exists(LEARNING_DB):
        with open(LEARNING_DB) as f:
            return json.load(f)
    return []


def save_db(data):
    with open(LEARNING_DB, "w") as f:
        json.dump(data, f)


def simulate_stats():
    """
    (Real API later — abhi safe simulation)
    """
    return {
        "views": random.randint(100, 10000),
        "likes": random.randint(10, 1000),
        "watch_time": random.randint(20, 100)
    }


def score(stats):
    return (
        stats["views"] * 0.5
        + stats["likes"] * 2
        + stats["watch_time"] * 3
    )


def main():

    db = load_db()

    stats = simulate_stats()
    performance = score(stats)

    record = {
        "stats": stats,
        "score": performance
    }

    db.append(record)
    db = db[-30:]  # keep last 30 uploads

    save_db(db)

    print("Learning updated:", performance)


if __name__ == "__main__":
    main()
