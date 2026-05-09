"""
YouTube Playlist Transfer Tool
================================
Transfers all (or selected) playlists from one YouTube/Google account to another.

Requirements:
    pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

Setup:
    1. Go to https://console.cloud.google.com/
    2. Create a project → Enable "YouTube Data API v3"
    3. Go to "Credentials" → Create OAuth 2.0 Client ID (Desktop App)
    4. Download the JSON and save as: client_secrets.json (in same folder as this script)
    5. Run: python youtube_playlist_transfer.py
"""

import os
import json
import time
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# ─── CONFIG ─────────────────────────────────────────────────────────────────

CLIENT_SECRETS_FILE = "client_secrets.json"   # Your OAuth credentials JSON
SCOPES = ["https://www.googleapis.com/auth/youtube"]

# Token cache files — keeps you from re-logging in every run
SOURCE_TOKEN_FILE      = "token_source.pkl"
DESTINATION_TOKEN_FILE = "token_destination.pkl"

# Set to None to transfer ALL playlists, or provide a list of playlist IDs:
# e.g. PLAYLIST_FILTER = ["PLxxxxxxx", "PLyyyyyyy"]
PLAYLIST_FILTER = None

# How long to wait (seconds) between API writes to avoid quota errors
WRITE_DELAY = 0.5

# ─── AUTH ────────────────────────────────────────────────────────────────────

def authenticate(token_file: str, account_label: str):
    """
    Authenticates a Google account via OAuth2 and returns a YouTube API client.
    Re-uses a saved token if available.
    """
    creds = None

    if os.path.exists(token_file):
        with open(token_file, "rb") as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print(f"  🔄 Refreshing token for {account_label}...")
            creds.refresh(Request())
        else:
            print(f"\n🔐 Please log in with your {account_label} Google account.")
            print("   A browser window will open. Complete the sign-in there.\n")
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_file, "wb") as f:
            pickle.dump(creds, f)
        print(f"  ✅ Token saved for {account_label}.\n")

    return build("youtube", "v3", credentials=creds)

# ─── FETCH ───────────────────────────────────────────────────────────────────

def get_all_playlists(youtube) -> list[dict]:
    """Fetches all playlists owned by the authenticated user."""
    playlists = []
    next_page_token = None

    while True:
        response = youtube.playlists().list(
            part="snippet,status",
            mine=True,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        for item in response.get("items", []):
            playlists.append({
                "id":          item["id"],
                "title":       item["snippet"]["title"],
                "description": item["snippet"].get("description", ""),
                "privacy":     item["status"]["privacyStatus"],
            })

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return playlists


def get_playlist_videos(youtube, playlist_id: str) -> list[str]:
    """Returns an ordered list of video IDs in a given playlist."""
    video_ids = []
    next_page_token = None

    while True:
        response = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        for item in response.get("items", []):
            video_ids.append(item["contentDetails"]["videoId"])

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return video_ids

# ─── CREATE / INSERT ─────────────────────────────────────────────────────────

def create_playlist(youtube, title: str, description: str, privacy: str) -> str:
    """Creates a new playlist in the destination account and returns its ID."""
    response = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title":       title,
                "description": description,
            },
            "status": {
                "privacyStatus": privacy,
            }
        }
    ).execute()
    return response["id"]


def add_video_to_playlist(youtube, playlist_id: str, video_id: str):
    """Adds a single video to a playlist."""
    youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind":    "youtube#video",
                    "videoId": video_id,
                }
            }
        }
    ).execute()

# ─── MAIN TRANSFER ───────────────────────────────────────────────────────────

def transfer_playlists():
    print("=" * 60)
    print("   🎬  YouTube Playlist Transfer Tool")
    print("=" * 60)

    # Step 1 — Authenticate both accounts
    print("\n[Step 1/4] Authenticating SOURCE account...")
    src_yt = authenticate(SOURCE_TOKEN_FILE, "SOURCE")

    print("[Step 2/4] Authenticating DESTINATION account...")
    dst_yt = authenticate(DESTINATION_TOKEN_FILE, "DESTINATION")

    # Step 2 — Fetch source playlists
    print("[Step 3/4] Fetching playlists from source account...\n")
    all_playlists = get_all_playlists(src_yt)

    if not all_playlists:
        print("  ⚠️  No playlists found in source account. Exiting.")
        return

    # Apply filter if set
    if PLAYLIST_FILTER:
        playlists = [p for p in all_playlists if p["id"] in PLAYLIST_FILTER]
        print(f"  🎯 Filter applied — {len(playlists)} of {len(all_playlists)} playlists selected.")
    else:
        playlists = all_playlists
        print(f"  📋 Found {len(playlists)} playlist(s) to transfer:")

    for i, pl in enumerate(playlists, 1):
        print(f"     {i:>2}. [{pl['privacy'][:3].upper()}] {pl['title']}  (id: {pl['id']})")

    print()
    confirm = input("▶  Proceed with transfer? (yes/no): ").strip().lower()
    if confirm not in ("yes", "y"):
        print("Transfer cancelled.")
        return

    # Step 3 — Transfer each playlist
    print(f"\n[Step 4/4] Transferring {len(playlists)} playlist(s)...\n")

    summary = []  # (title, videos_ok, videos_failed, new_id)

    for idx, pl in enumerate(playlists, 1):
        print(f"  ── Playlist {idx}/{len(playlists)}: \"{pl['title']}\"")

        # Fetch videos from source
        video_ids = get_playlist_videos(src_yt, pl["id"])
        print(f"     📼  {len(video_ids)} video(s) found.")

        # Create matching playlist in destination
        try:
            new_pl_id = create_playlist(dst_yt, pl["title"], pl["description"], pl["privacy"])
            print(f"     ✅  Created playlist in destination (id: {new_pl_id})")
        except HttpError as e:
            print(f"     ❌  Failed to create playlist: {e}")
            summary.append((pl["title"], 0, len(video_ids), "ERROR"))
            continue

        # Add each video
        ok, failed = 0, 0
        for vid_id in video_ids:
            try:
                add_video_to_playlist(dst_yt, new_pl_id, vid_id)
                ok += 1
                print(f"        ➕ Added video {vid_id}  ({ok}/{len(video_ids)})")
            except HttpError as e:
                failed += 1
                err_reason = json.loads(e.content).get("error", {}).get("errors", [{}])[0].get("reason", str(e))
                print(f"        ⚠️  Skipped {vid_id} — {err_reason}")
            time.sleep(WRITE_DELAY)   # Throttle writes

        summary.append((pl["title"], ok, failed, new_pl_id))
        print()

    # ─── Summary ─────────────────────────────────────────────────────────────
    print("=" * 60)
    print("   ✅  TRANSFER COMPLETE — Summary")
    print("=" * 60)
    total_ok, total_fail = 0, 0
    for title, ok, fail, new_id in summary:
        status = "✅" if fail == 0 else "⚠️ "
        print(f"  {status}  {title}")
        print(f"        Videos transferred: {ok}   Skipped: {fail}")
        if new_id != "ERROR":
            print(f"        New playlist ID: {new_id}")
        total_ok   += ok
        total_fail += fail
    print("-" * 60)
    print(f"  Total videos transferred : {total_ok}")
    print(f"  Total videos skipped     : {total_fail}")
    print("=" * 60)
    print("\n  💡 Skipped videos are usually private/deleted videos")
    print("     that can't be added to another account's playlist.\n")


if __name__ == "__main__":
    transfer_playlists()
