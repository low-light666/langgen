#!/usr/bin/python3
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import pickle

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/youtube']

def authenticate():
    creds = None

    # The file token.pickle stores the user's access and refresh tokens, and is created automatically when the authorization flow completes for the first time
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds

# Authenticate and get credentials
credentials = authenticate()
youtube = build('youtube', 'v3', credentials=credentials)

# Load your JSON data
with open('francais.json', 'r') as file:
    json_data = json.load(file)

# Create a playlist to add all videos
playlist_title = "Machine generated playlist: French Grammar from A1 to B2"
playlist_description = "Topics suggested by chatgpt3.5 and parsed using google dorks"

# Create the playlist
request = youtube.playlists().insert(
    part='snippet',
    body={
        'snippet': {
            'title': playlist_title,
            'description': playlist_description
        }
    }
)
response = request.execute()
playlist_id = response['id']

# Iterate through the levels (A1, A2, B1, B2) in your JSON data
for level, topics in json_data.items():
    for topic_id, topic_info in topics.items():
        # Extract relevant data for video addition
        link = topic_info['link']
        video_id = link.split('=')[-1]  # Extract the video ID from the YouTube link

        # Add video to the created playlist
        youtube.playlistItems().insert(
            part='snippet',
            body={
                'snippet': {
                    'playlistId': playlist_id,
                    'resourceId': {
                        'kind': 'youtube#video',
                        'videoId': video_id
                    }
                }
            }
        ).execute()

print(f"All videos added to the '{playlist_title}' playlist.")
