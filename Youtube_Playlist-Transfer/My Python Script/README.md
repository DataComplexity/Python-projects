# YouTube Playlist Transfer (Original Version)

The foundational version of the YouTube playlist transfer script. This script provides a straightforward implementation of transferring playlists between accounts.

## Features

- Simple OAuth2 authentication flow.
- Automatic creation of private playlists in the destination account.
- Bulk video transfer.

## Prerequisites

- Python 3.7+
- Google Cloud Project with YouTube Data API v3 enabled.
- `client_secrets.json` file in the same directory.

## Setup

1. Create a project in [Google Cloud Console](https://console.cloud.google.com/).
2. Enable **YouTube Data API v3**.
3. Create **OAuth 2.0 Client ID** (Desktop App) and download the JSON.
4. Name the file `client_secrets.json` and place it here.
5. Install requirements:

   ```bash
   pip install -r requirements.txt
   ```

## How to Use

```bash
python YoutubePlaylistTransfer.py
```

Log in to both accounts when prompted in your browser.
