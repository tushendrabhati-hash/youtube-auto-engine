import os
import json
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

# Load credentials from GitHub Secret
creds_json = os.environ["YT_CREDENTIALS"]
creds_dict = json.loads(creds_json)

creds = Credentials.from_authorized_user_info(creds_dict)

youtube = build("youtube", "v3", credentials=creds)

request = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {
            "title": "🔥 Auto Upload Working!",
            "description": "First automated upload from GitHub Actions",
            "categoryId": "22"
        },
        "status": {"privacyStatus": "public"}
    },
    media_body=MediaFileUpload("output.mp4")
)

response = request.execute()

print("UPLOAD SUCCESS:", response["id"])
