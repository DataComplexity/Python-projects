import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/youtube"]

def authenticate(account_name):
    creds = None
    token_file = f"token_{account_name}.pickle"

    if os.path.exists(token_file):
        with open(token_file, "rb") as token:
            creds = pickle.load(token)

    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file(
            "client_secrets.json", SCOPES
        )
        creds = flow.run_local_server(port=0)

        with open(token_file, "wb") as token:
            pickle.dump(creds, token)

    return build("youtube", "v3", credentials=creds)


def get_all_playlists(youtube):
    playlists = []

    request = youtube.playlists().list(
        part="snippet,contentDetails",
        mine=True,
        maxResults=50
    )

    while request:
        response = request.execute()
        playlists.extend(response["items"])
        request = youtube.playlists().list_next(request, response)

    return playlists


def get_playlist_items(youtube, playlist_id):
    videos = []

    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=50
    )

    while request:
        response = request.execute()
        for item in response["items"]:
            videos.append(item["snippet"]["resourceId"]["videoId"])
        request = youtube.playlistItems().list_next(request, response)

    return videos


def create_playlist(youtube, title, description):
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description
            },
            "status": {
                "privacyStatus": "private"
            }
        }
    )
    response = request.execute()
    return response["id"]


def add_video_to_playlist(youtube, playlist_id, video_id):
    youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }
    ).execute()


def transfer_playlists(source, destination):
    playlists = get_all_playlists(source)

    for playlist in playlists:
        title = playlist["snippet"]["title"]
        description = playlist["snippet"].get("description", "")
        playlist_id = playlist["id"]

        print(f"Copying playlist: {title}")

        videos = get_playlist_items(source, playlist_id)

        new_playlist_id = create_playlist(destination, title, description)

        for video_id in videos:
            try:
                add_video_to_playlist(destination, new_playlist_id, video_id)
            except Exception as e:
                print(f"Skipping video {video_id}: {e}")

        print(f"Finished: {title}")


if __name__ == "__main__":
    print("Login to SOURCE account")
    source_youtube = authenticate("source")

    print("Login to DESTINATION account")
    dest_youtube = authenticate("destination")

    transfer_playlists(source_youtube, dest_youtube)

    print("Transfer Complete!")