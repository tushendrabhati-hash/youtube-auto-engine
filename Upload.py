import os
import json
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

creds_json = os.environ["YT_CREDENTIALS"]
creds_dict = json.loads(creds_json)

creds = Credentials.from_authorized_user_info(creds_dict)

youtube = build("youtube", "v3", credentials=creds)

VIDEOS = [
    "final1.mp4",
    "final2.mp4",
    "final3.mp4",
    "final4.mp4"
]

TITLES = [
    "🔥 Viral Clip You Must See",
    "😱 Internet Can't Believe This",
    "💥 Trending Everywhere Now",
    "⚡ Watch Till End"
]


def upload(video, title):

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": "Auto network upload #shorts #viral",
                "categoryId": "22"
            },
            "status": {"privacyStatus": "public"}
        },
        media_body=MediaFileUpload(video)
    )

    response = request.execute()
    print("Uploaded:", response["id"])


def main():

    for v, t in zip(VIDEOS, TITLES):
        if os.path.exists(v):
            upload(v, t)


if __name__ == "__main__":
    main()
