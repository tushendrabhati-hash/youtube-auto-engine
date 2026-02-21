import os
import json
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

# Load credentials
creds_json = os.environ["YT_CREDENTIALS"]
creds_dict = json.loads(creds_json)

creds = Credentials.from_authorized_user_info(creds_dict)

youtube = build("youtube", "v3", credentials=creds)

# Load metadata
with open("metadata.json") as f:
    meta = json.load(f)

request = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {
            "title": meta["title"],
            "description": meta["description"],
            "categoryId": "22"
        },
        "status": {"privacyStatus": "public"}
    },
    media_body=MediaFileUpload("final.mp4")
)

response = request.execute()

print("UPLOAD SUCCESS:", response["id"])
