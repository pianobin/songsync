# songsync (WIP)

Convert YT playlists to Spotify playlists

## Installation

Install poetry: https://python-poetry.org/docs/#installation

Setup and activate virtual environment

```
python3 -m venv .venv && source .venv/bin/activate
```

Install poetry dependencies

```
poetry install
```

Set the YouTube playlist ID of the songs you want to transfer to Spotify to YT_PLAYLIST_ID (to be cleaned up)

Create a Spotify app by following the instructions in the Spotify Web API documentation: https://developer.spotify.com/documentation/web-api

Set the following environment variables

```
export SPOTIPY_CLIENT_ID='your-spotify-client-id'
export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
export SPOTIPY_REDIRECT_URI='your-app-redirect-url'
```

## Run

Run the script

```
python3 app.py
```
