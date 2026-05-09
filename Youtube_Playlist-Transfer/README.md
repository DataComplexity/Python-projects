# YouTube Playlist Transfer Collection

This repository contains two versions of a YouTube Playlist Transfer tool, designed to migrate your saved music, tutorials, and videos from one Google account to another.

## Folder Structure

### 1. [Original Python Script](./My%20Python%20Script/)

- The initial implementation.
- Simple, direct, and functional.
- Best for understanding the core logic of the YouTube API.

### 2. [Refined AI-Assisted Script](./My%20Python%20Script%20(Debugged%20&%20Refined%20By%20AI)/)

- **Recommended version.**
- Enhanced with better error handling and progress UI.
- Throttles API requests to prevent "Quota Exceeded" errors.
- Includes token caching to avoid repeated logins.

## General Setup

Both versions require a `client_secrets.json` from the [Google Cloud Console](https://console.cloud.google.com/).

1. Enable **YouTube Data API v3**.
2. Create **OAuth Client ID** (Desktop App).
3. Download and place the JSON in the specific script's folder.
