from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

youtube = build(
    "youtube",
    "v3",
    developerKey=os.environ["YT_API"]
)

request = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet":{
            "title":"Auto Viral Short 🔥",
            "description":"Automated upload",
            "categoryId":"22"
        },
        "status":{"privacyStatus":"public"}
    },
    media_body=MediaFileUpload("output.mp4")
)

request.execute()
