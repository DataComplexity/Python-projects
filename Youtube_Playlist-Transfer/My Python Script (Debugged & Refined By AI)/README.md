# YouTube Playlist Transfer (Refined Version)

An advanced Python tool to transfer YouTube playlists from one Google account to another using the YouTube Data API v3. This version includes better error handling, progress tracking, and API quota management.

## Key Features

- **Bilateral Authentication**: Authenticate both source and destination accounts in one session.

- **Token Caching**: Remembers your login so you don't have to re-authenticate every time.

- **Quota Protection**: Optimized to respect YouTube API rate limits.
- **Bilingual Interface**: Simple and clear console output.

## Prerequisites

- Python 3.7+
- A Google Cloud Project with the **YouTube Data API v3** enabled.
- OAuth 2.0 Credentials (`client_secrets.json`).

## Setup

1. **Enable YouTube API**: Go to the [Google Cloud Console](https://console.cloud.google.com/), create a project, and enable "YouTube Data API v3".
2. **Credentials**: Go to "Credentials" -> "Create Credentials" -> "OAuth Client ID" (Select "Desktop App").
3. **Download JSON**: Download the client secret JSON and rename it to `client_secrets.json`. Place it in this folder.
4. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## How to Use

Run the script:

```bash
python youtube_playlist_transfer.py
```

1. A browser window will open for the **Source** account login.
2. A second window will open for the **Destination** account login.
3. The script will list your playlists. Confirm the transfer by typing `yes`.

---
