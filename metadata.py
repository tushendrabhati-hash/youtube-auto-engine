import json
import random
import os
import sys


# ================= TITLE HOOKS =================
HOOKS = [
    "Wait For It",
    "You Won't Believe This",
    "Instant Regret Moment",
    "This Went Viral",
    "Everyone Watching This",
    "Perfect Bite Moment",
    "Unexpected Ending",
    "Most Satisfying Bite",
    "Internet Can't Stop Watching",
    "One Bite Challenge",
    "Watch Till The End",
    "This Is Crazy",
]

EMOJIS = ["🔥","😱","🤯","👀","🍗","🍔","🍜","🦀","🍕","🌶️","🥵","😋"]


# ================= HASHTAGS =================
HASHTAGS_POOL = [
"#shorts","#viral","#food","#asmr","#mukbang","#streetfood","#trending",
"#foodie","#reels","#foodlover","#yummy","#delicious","#foodvideo",
"#eating","#tasty","#foodshorts","#viralshorts","#chef","#cooking",
"#foodchallenge","#spicy","#satisfying","#foodporn","#snack","#dinner",
"#lunch","#breakfast","#fastfood","#indianfood","#koreanfood",
"#seafood","#meat","#bbq","#fried","#cheese","#sauce","#crunchy",
"#eatingshow","#foodblog","#dailyshorts","#explore","#reelsviral"
]


# ================= FOOD CONTEXT =================
FOOD_KEYWORDS = {
"crab":"Spicy Crab Feast",
"lobster":"Butter Lobster Bite",
"shrimp":"Garlic Shrimp Mukbang",
"seafood":"Seafood Feast",
"fish":"Grilled Fish Bite",
"chicken":"Crispy Chicken",
"fried":"Fried Food Moment",
"burger":"Juicy Burger",
"pizza":"Cheesy Pizza Slice",
"noodle":"Spicy Noodles",
"ramen":"Hot Ramen Bowl",
"rice":"Street Food Rice Bowl",
"bbq":"Smoky BBQ Meat",
"steak":"Juicy Steak Cut",
"egg":"Egg Street Food",
"cheese":"Cheesy Explosion",
"paneer":"Paneer Street Bite",
"biryani":"Spicy Biryani Bite",
"shawarma":"Chicken Shawarma",
"kebab":"Grilled Kebab",
"taco":"Loaded Taco Bite",
"hotdog":"Street Hotdog",
"sushi":"Fresh Sushi Roll",
"dessert":"Sweet Dessert Bite",
"cake":"Chocolate Cake Slice",
"icecream":"Ice Cream Treat"
}


# ================= FIND VIDEO =================
def find_video(job_folder):

    for f in os.listdir(job_folder):
        if f.startswith("001_") and f.endswith(".mp4"):
            return f

    return ""


# ================= CONTEXT =================
def detect_context(filename):

    name = filename.lower()

    for key, val in FOOD_KEYWORDS.items():
        if key in name:
            return val

    return "Ultimate Food Bite"


# ================= TITLE =================
def generate_title(context):

    hook = random.choice(HOOKS)
    emoji = random.choice(EMOJIS)

    hashtags = random.sample(["#shorts","#viral","#food","#trending"],2)

    title = f"{hook} {emoji} | {context} {' '.join(hashtags)}"

    return title[:100]


# ================= DESCRIPTION =================
def generate_description(title, hashtags):

    desc = f"""{title}

Watch till the end for the best moment 🤯
This satisfying food short is trending right now and people can't stop watching it.

If you enjoy food videos, mukbang, ASMR eating and viral shorts — you're in the right place 🔥

👉 Follow for daily viral food shorts.

{' '.join(hashtags)}
"""

    return desc


# ================= TAGS =================
def generate_tags():

    tags_pool = [h.replace("#","") for h in HASHTAGS_POOL]
    return random.sample(tags_pool, random.randint(5,10))


# ================= MAIN =================
def generate_metadata(job_folder):

    video_name = find_video(job_folder)

    if not video_name:
        print("❌ No video found for metadata")
        sys.exit(1)

    context = detect_context(video_name)

    title = generate_title(context)

    hashtags = random.sample(HASHTAGS_POOL, random.randint(5,10))

    description = generate_description(title, hashtags)

    tags = generate_tags()

    data = {
        "title": title,
        "description": description,
        "tags": tags
    }

    meta_path = os.path.join(job_folder, "metadata.json")

    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"🧠 Smart Metadata Generated → {context}")


# ================= ENTRY =================
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("❌ Usage: metadata.py <job_folder>")
        sys.exit(1)

    generate_metadata(sys.argv[1])